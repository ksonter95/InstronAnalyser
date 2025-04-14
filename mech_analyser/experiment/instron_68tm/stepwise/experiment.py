import dataclasses
import experiment.experiment as experiment
import experiment.instron_68tm.experiment as instron_68tm
import experiment.instron_68tm.stepwise.view as view
import pyqtgraph as pg  # type: ignore
import util.utils as utils

import numpy as np
import pandas as pd

from pathlib import Path
from scipy.optimize import curve_fit  # type: ignore
from typing import Any, Optional

# === Data frames ============================================================ #


class Frame(instron_68tm.ProcessedFrame):
    """
    Processed output of a stepwise compression experiment using an Instron 68TM.

    Args:
        frame: Underlying pd.DataFrame representation of the data.
        sheet_name: The name of the Excel sheet to which the data will be
            written.
    """

    def __init__(self, frame: pd.DataFrame, sheet_name: str) -> None:

        super().__init__(frame, sheet_name)

        # Initially populate the processed data columns with default values
        self.relative_time = pd.Series([0.0] * self._frame.index.size)  # type: ignore
        self.regression_stress = pd.Series([0] * self._frame.index.size)  # type: ignore

    @property
    def initial_time_s(self) -> float:
        return self.time[0]

    @property
    def regression_stress(self) -> "pd.Series[float]":
        return self._frame["Regression Stress [MPa]"]  # type: ignore

    @regression_stress.setter
    def regression_stress(self, value: "pd.Series[float]") -> None:
        self._frame["Regression Stress [MPa]"] = value

    @property
    def relative_time(self) -> "pd.Series[float]":
        return self._frame["Relative Time [s]"]  # type: ignore

    @relative_time.setter
    def relative_time(self, value: "pd.Series[float]") -> None:
        self._frame["Relative Time [s]"] = value

        # Move the relative time column to be directly after the time column
        column: pd.Series = self._frame.pop("Relative Time [s]")  # type: ignore
        self._frame.insert(  # type: ignore
            self._frame.columns.get_loc("Time [s]") + 1,  # type: ignore
            "Relative Time [s]",
            column,
        )

    def generate_plot(self, **kwargs: dict[str, Any]) -> None:
        """
        Generates a plot of the data.

        Args:
            regression_data_points: Maximum number of data points to be included
                in the regression analysis.
            tau_r2: Reduced modulus of the exponential decay regression.
        """

        regression_data_points: Optional[int] = kwargs.get("regression_data_points")  # type: ignore
        tau_r2: float = kwargs.get("tau_r2")  # type: ignore

        # Plot the data
        self._plot.getPlotItem().setTitle("Exponential decay stress-time regression")  # type: ignore
        self._plot.getPlotItem().setLabel("bottom", self.relative_time.name)  # type: ignore
        self._plot.getPlotItem().setLabel("left", self.stress.name)  # type: ignore
        self._plot.getPlotItem().addLegend()  # type: ignore
        self._plot.getPlotItem().plot(  # type: ignore
            self.relative_time.values, self.stress.values, name=self.stress.name
        )
        self._plot.getPlotItem().plot(  # type: ignore
            self.relative_time.values,
            self.regression_stress.values,
            name=self.regression_stress.name,
            pen=pg.mkPen("r"),  # type: ignore
        )

        # Add the regression domain
        self._plot.getPlotItem().plot(  # type: ignore
            [0, self.relative_time[regression_data_points or self.frame.index.size]],
            [self.stress[0]] * 2,  # type: ignore
            name="Regression domain",
            pen=None,
            fillLevel=self.stress[regression_data_points or self.frame.index.size],  # type: ignore
            brush=pg.mkBrush(200, 200, 255, 100),  # type: ignore
        )

        # Add the regression coefficient of determination
        self._plot.getPlotItem().plot(  # type: ignore
            [], [], name=f"R^2 = {round(tau_r2, 4)}", pen=None  # type: ignore
        )


# === Parameters ============================================================= #


@dataclasses.dataclass
class DataParameters(experiment.DataParameters):
    """
    Parameters of a stepwise compression experiment using an Instron 68TM.

    Args:
        relaxation_strain_pct: The strain at which the sample is maintained
            while the sample relaxes.
        epsilon_pct: Tolerance for the strain within which it is considered to
            be within the relaxation phase.
        regression_data_points: Maximum number of data points to be included in
            the regression analysis.
    """

    relaxation_strain_pct: float = 5.0
    epsilon_pct: float = 0.1
    regression_data_points: Optional[int] = None


@dataclasses.dataclass
class AnalyserParameters(instron_68tm.AnalyserParameters):
    """
    Parameters of an analyser of a stepwise compression experiment using an
    Instron 68TM.

    Args:
        relaxation_strain_intervals: The number of intervals at which the sample
            has been configured to relax.  This in combination with the first
            strain gives the relaxation strains.  For instance, if the first
            strain is 5%, and the number of intervals is 6, then the experiment
            will relax the sample at 5%, 10%, 15%, 20%, 25%, 30%.
        relaxation_strain_start_pct: The first strain at which the sample has
            been configured to relax.  This in combination with the number of
            intervals gives the relaxation strains.  For instance, if the first
            strain is 5%, and the number of intervals is 6, then the experiment
            will relax the sample at 5%, 10%, 15%, 20%, 25%, 30%.
        epsilon_pct: Tolerance for the strain within which it is considered to
            be within the relaxation phase.
        regression_data_points: Maximum number of data points to be included in
            the regression analysis.
    """

    relaxation_strain_intervals: int = 6
    relaxation_strain_start_pct: float = 5.0
    epsilon_pct: float = 0.1
    regression_data_points: Optional[int] = None


# === Data =================================================================== #


class Data(instron_68tm.Data):
    """
    Data of a stepwise compression experiment using an Instron 68TM.

    Args:
        raw_frame: The raw data frame from which the processed data frame is
            created.
    """

    def __init__(self, raw_frame: instron_68tm.RawFrame) -> None:

        super().__init__(
            raw_frame,
            Frame(pd.DataFrame(columns=raw_frame.frame.columns), "Strain = ?%"),
        )

        self._a_MPa: float = 0.0
        self._b_MPa: float = 0.0
        self._max_id: int = 0
        self._min_id: int = 0
        self._tau_s: float = 1.0
        self._tau_r2: float = 0.0

    @property
    def a_MPa(self) -> float:
        return self._a_MPa

    @property
    def b_MPa(self) -> float:
        return self._b_MPa

    @property
    def max_force_N(self) -> float:
        return self.processed_frame.force.loc[self._max_id]

    @property
    def max_stress_MPa(self) -> float:
        return self.processed_frame.stress.loc[self._max_id]

    @property
    def min_force_N(self) -> float:
        return self.processed_frame.force.loc[self._min_id]

    @property
    def min_stress_MPa(self) -> float:
        return self.processed_frame.stress.loc[self._min_id]

    @property
    def processed_frame(self) -> Frame:
        return super().processed_frame  # type: ignore

    @processed_frame.setter
    def processed_frame(self, value: Frame) -> None:  # type: ignore
        super(Data, Data).processed_frame.__set__(self, value)  # type: ignore

    @property
    def tau_s(self) -> float:
        return self._tau_s

    @property
    def tau_r2(self) -> float:
        return self._tau_r2

    def process(self, parameters: DataParameters) -> None:  # type: ignore
        """
        Processes the raw data from the stepwise compression experiment using an
        Instron 68TM.

        Dataset filtering:
            - Relaxation phase of the sample at the specified strain.

        Columns that are populated:
            - Relative Time: Time elapsed since the start of the relaxation
                phase.
            - Regression stress: Stress at each relative time point as
                calculated by the exponential decay regression equation of the
                stress.

        Summary parameters that are calculated:
            - Exponential decay regression equation parameters (a, b, and tau in
                y = a * e^(-t / tau) + b)
            - Maximum and minimum force and stress values within the dataset.

        Args:
            parameters: The parameters to use when processing the stepwise
                compression Instron 68TM experiment data.
        """

        # Filter the raw data to only obtain the data within the relation phase
        # of the sample for the specified strain
        self.processed_frame = Frame(
            self.raw_frame.frame[
                (
                    self.raw_frame.strain
                    > (parameters.relaxation_strain_pct - parameters.epsilon_pct)
                )
                & (
                    self.raw_frame.strain
                    < (parameters.relaxation_strain_pct + parameters.epsilon_pct)
                )
            ],
            f"Strain = {round(parameters.relaxation_strain_pct, 1)}%",
        )

        # Add the relative time column
        self.processed_frame.relative_time = (
            self.processed_frame.time - self.processed_frame.initial_time_s
        )

        # Calculate the parameters of the exponential decay equation that best
        # fits the data points
        self._a_MPa, self._b_MPa, self._tau_s, self._tau_r2 = self._execute_regression(
            parameters.regression_data_points
        )

        # Add the regression stress column directly after the stress column
        self.processed_frame.regression_stress = pd.Series(
            [
                self.y(t, self.a_MPa, self.b_MPa, self.tau_s)  # type: ignore
                for t in self.processed_frame.relative_time  # type: ignore
            ]
        )

        # Calculate the remaining summary parameters
        self._max_id = self.processed_frame.force.idxmax()  # type: ignore
        self._min_id = self.processed_frame.force.idxmin()  # type: ignore

        # Generate the processed data plot
        self.processed_frame.generate_plot(
            regression_data_points=parameters.regression_data_points,  # type: ignore
            tau_r2=self.tau_r2,  # type: ignore
        )

    def _execute_regression(
        self, regression_data_points: Optional[int]
    ) -> tuple[float, float, float, float]:
        """
        Executes the regression to determine the exponential decay regression
        equation parameters and the corresponding coefficient of determination.

        Args:
            regression_data_points: Maximum number of data points to be included
                in the regression.  If None is specified, the entire data set is
                included in the regression.

        Returns:
            Tuple of a, b, and tau (the exponential decay regression equation
            parameters) and their corresponding coefficient of determination.
        """

        x: "pd.Series[float]" = self.processed_frame.relative_time.head(
            regression_data_points or self.processed_frame.frame.index.size
        )
        y: "pd.Series[float]" = self.processed_frame.stress.head(
            regression_data_points or self.processed_frame.frame.index.size
        )

        # Ensure that the regression has more data points that the number of
        # parameters to be regressed
        if len(x) < 4:
            return 0.0, 0.0, 1.0, 0.0

        [a_MPa, b_MPa, tau_s], _ = curve_fit(self.y, x, y)  # type: ignore

        tau_r2: float = utils.calculate_r2(
            list(y), [self.y(time_s, a_MPa, b_MPa, tau_s) for time_s in x]  # type: ignore
        )

        return a_MPa, b_MPa, tau_s, tau_r2  # type: ignore

    @staticmethod
    def y(t: float, a_MPa: float, b_MPa: float, tau_s: float) -> float:
        """
        Calculates the stress according to the following equation:
        y = a * e^(-t / tau) + b

        Args:
            t: Time at which the stress is to be calculated.
            a_MPa: Amplitude of the exponential decay.
            b_MPa: Baseline value of the function.
            tau_s: Time constant of the exponential decay.

        Returns:
            Stress at time t.
        """

        return a_MPa * np.exp(-t / tau_s) + b_MPa


# === Results ================================================================ #


class Summary(instron_68tm.Summary):
    """
    Summary of the stepwise compression Instron 68TM experiment.
    """

    def __init__(self) -> None:

        super().__init__(
            pd.DataFrame(
                columns=[
                    "Strain [%]",
                    "Min stress [MPa]",
                    "Max stress [MPa]",
                    "Min force [N]",
                    "Max force [N]",
                    "a [MPa]",
                    "b [MPa]",
                    "tau [s]",
                    "tau R^2 [MPa^2/MPa^2]",
                ]
            )
        )

    def append_row(self, data: Data, parameters: DataParameters) -> None:  # type: ignore
        """
        Append a row to the underlying pd.DataFrame representation of the
        summary.

        Args:
            data: The data of a stepwise compression Instron 68TM experiment
                to be appended.
            parameters: The parameters of a stepwise compression experiment
                using an Instron 68TM used to process the data.
        """

        self._frame.loc[len(self._frame)] = [
            parameters.relaxation_strain_pct,
            data.min_stress_MPa,
            data.max_stress_MPa,
            data.min_force_N,
            data.max_force_N,
            data.a_MPa,
            data.b_MPa,
            data.tau_s,
            data.tau_r2,
        ]


# === Analysers ============================================================== #


class Analyser(instron_68tm.Analyser):
    """
    Analyser of the stepwise compression Instron 68TM experiment.

    Args:
        input_csv: The path to the CSV file containing the output of the
            stepwise compression Instron 68TM experiment.
        output_xlsx: The path to the Excel file which will contain the analysis
            results.
        parameters: The parameters to use when analysing the stepwise
            compression Instron 68TM experiment.
    """

    def __init__(
        self,
        input_csv: Path,
        output_xlsx: Path,
        parameters: AnalyserParameters,
    ) -> None:

        super().__init__(input_csv, output_xlsx, parameters, Summary())

        for _ in range(parameters.relaxation_strain_intervals):
            self.data.append(Data(self.raw_frame))

    @property
    def data(self) -> list[Data]:  # type: ignore
        return super().data  # type: ignore

    @property
    def parameters(self) -> AnalyserParameters:  # type: ignore
        return super().parameters  # type: ignore

    @property
    def summary(self) -> Summary:
        return super().summary  # type: ignore

    def analyse(self) -> None:
        """
        Analyses the output of the stepwise compression Instron 68TM experiment.
        """

        # Resize the processed data based on the number of relaxation intervals
        if len(self.data) > self.parameters.relaxation_strain_intervals:
            del self.data[self.parameters.relaxation_strain_intervals :]
        else:
            self.data.extend(
                [
                    Data(self.raw_frame)
                    for _ in range(
                        self.parameters.relaxation_strain_intervals - len(self.data)
                    )
                ]
            )

        self.summary.clear_all_rows()

        for i in range(len(self.data)):
            parameters = DataParameters(
                self.parameters.relaxation_strain_start_pct * (i + 1),
                self.parameters.epsilon_pct,
                self.parameters.regression_data_points,
            )
            self.data[i].process(parameters)
            self.summary.append_row(self.data[i], parameters)


# === User Interface Widgets ================================================= #


class ConfigWidget(instron_68tm.ConfigWidget):
    """
    User interface configuration widget for the stepwise compression Instron
    68TM experiment.
    """

    def __init__(self) -> None:
        super().__init__(view.Ui_w_Stepwise(), AnalyserParameters())  # type: ignore

    @property
    def experiment(self) -> str:
        return "Stepwise compression"

    @property
    def parameters(self) -> AnalyserParameters:
        return super().parameters  # type: ignore

    @property
    def view(self) -> view.Ui_w_Stepwise:  # type: ignore
        return super().view  # type: ignore

    def create_analyser(  # type: ignore
        self, input_csv: Path, output_xlsx: Path, parameters: AnalyserParameters
    ) -> Analyser:
        """
        Creates the experiment analyser.

        Args:
            input_csv: The path to the CSV file containing the output of the
                stepwise compression Instron 68TM experiment.
            output_xlsx: The path to the Excel file which will contain the
                analysis results.
            parameters: The parameters to use when analysing the stepwise
                compression Instron 68TM experiment.
        """

        return Analyser(input_csv, output_xlsx, parameters)

    def init(self) -> None:
        """
        Initialises the configuration widget by setting the input fields to the
        defaults of the parameters to use when analysing the experiment and
        connecting any signals with an associated slot.
        """

        # Set the input fields to the defaults
        self.view.sb_RelaxationStrainsIntervals.setValue(
            self.parameters.relaxation_strain_intervals
        )
        self.view.sb_RelaxationStrainsStart.setValue(
            self.parameters.relaxation_strain_start_pct
        )
        self.view.sb_Epsilon.setValue(self.parameters.epsilon_pct)
        self.view.sb_RegressionPoints.setValue(
            self.parameters.regression_data_points or 0
        )
        self.view.cb_RegressionPoints.setChecked(
            self.parameters.regression_data_points is not None
        )

        # Connect signals with slots
        self.view.cb_RegressionPoints.checkStateChanged.connect(
            self._handle_cb_RegressionPoints_changed
        )

        # Set initial views
        self._handle_cb_RegressionPoints_changed()

    def sync_parameters(self) -> None:
        """
        Synchronise the parameters to use when analysing the experiment with the
        configuration widget input fields.
        """

        self.parameters.relaxation_strain_intervals = (
            self.view.sb_RelaxationStrainsIntervals.value()
        )
        self.parameters.relaxation_strain_start_pct = (
            self.view.sb_RelaxationStrainsStart.value()
        )
        self.parameters.epsilon_pct = self.view.sb_Epsilon.value()
        self.parameters.regression_data_points = (
            self.view.sb_RegressionPoints.value()
            if self.view.cb_RegressionPoints.isChecked()
            else None
        )

    def _handle_cb_RegressionPoints_changed(self) -> None:
        """
        Sets the visibility of sb_RegressionPoints to the state of
        cb_RegressionPoints.
        """

        self.view.sb_RegressionPoints.setDisabled(
            not self.view.cb_RegressionPoints.isChecked()
        )
