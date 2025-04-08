import dataclasses
import experiment.experiment as experiment
import experiment.microtester_g2.experiment as microtester_g2
import experiment.microtester_g2.microindentation.view as view
import numpy as np
import pandas as pd
import util.utils as utils

from numpy.typing import NDArray
from pathlib import Path
from scipy.optimize import curve_fit  # type: ignore
from typing import Optional


# === Data frames ============================================================ #


class Frame(microtester_g2.ProcessedFrame):
    """
    Processed output of a microindentation experiment using a MicroTester G2.

    Args:
        frame: Underlying pd.DataFrame representation of the data.
        sheet_name: The name of the Excel sheet to which the data will be
            written.
    """

    def __init__(self, frame: pd.DataFrame, sheet_name: str) -> None:

        super().__init__(frame, sheet_name)

        # Initially populate the processed data columns with default values
        self.indentation_force = pd.Series([0.0] * self._frame.index.size)  # type: ignore
        self.regression_force = pd.Series([0.0] * self._frame.index.size)  # type: ignore
        self.indentation_depth = pd.Series([0.0] * self._frame.index.size)  # type: ignore
        self.h_R = pd.Series([0.0] * self._frame.index.size)  # type: ignore

    @property
    def h_R(self) -> "pd.Series[float]":
        return self._frame["h/R [um/um]"]  # type: ignore

    @h_R.setter
    def h_R(self, value: "pd.Series[float]") -> None:
        self._frame["h/R [um/um]"] = value

        # Move the h/R column to be directly after the indentation depth column
        column: pd.Series = self._frame.pop("h/R [um/um]")  # type: ignore
        self._frame.insert(  # type: ignore
            self._frame.columns.get_loc("Indentation Depth [um]") + 1,  # type: ignore
            "h/R [um/um]",
            column,
        )

    @property
    def indentation_depth(self) -> "pd.Series[float]":
        return self._frame["Indentation Depth [um]"]  # type: ignore

    @indentation_depth.setter
    def indentation_depth(self, value: "pd.Series[float]") -> None:
        self._frame["Indentation Depth [um]"] = value

        # Move the indentation depth column to be directly after the tip
        # displacement column
        column: pd.Series = self._frame.pop("Indentation Depth [um]")  # type: ignore
        self._frame.insert(  # type: ignore
            self._frame.columns.get_loc("Tip Displacement [um]") + 1,  # type: ignore
            "Indentation Depth [um]",
            column,
        )

    @property
    def indentation_force(self) -> "pd.Series[float]":
        return self._frame["Indentation Force [uN]"]  # type: ignore

    @indentation_force.setter
    def indentation_force(self, value: "pd.Series[float]") -> None:
        self._frame["Indentation Force [uN]"] = value

        # Move the indentation force column to be directly after the force column
        column: pd.Series = self._frame.pop("Indentation Force [uN]")  # type: ignore
        self._frame.insert(  # type: ignore
            self._frame.columns.get_loc("Force [uN]") + 1,  # type: ignore
            "Indentation Force [uN]",
            column,
        )

    @property
    def regression_force(self) -> "pd.Series[float]":
        return self._frame["Regression Force [uN]"]  # type: ignore

    @regression_force.setter
    def regression_force(self, value: "pd.Series[float]") -> None:
        self._frame["Regression Force [uN]"] = value

        # Move the regression force column to be directly after the indentation
        # force column
        column: pd.Series = self._frame.pop("Regression Force [uN]")  # type: ignore
        self._frame.insert(  # type: ignore
            self._frame.columns.get_loc("Indentation Force [uN]") + 1,  # type: ignore
            "Regression Force [uN]",
            column,
        )


# === Parameters ============================================================= #


@dataclasses.dataclass
class DataParameters(experiment.DataParameters):
    """
    Parameters of a microindentation experiment using a MicroTester G2.

    Args:
        cycle: Compression/recover cycle number to which the data belongs.
        samples_to_skip: Number of samples at the beginning of the sample data
            to skip.
        R_um: Radius of the spherical indenter.
        v: Poisson's ratio of the sample.  See Bas, Onur, et al. "Rational
            design and fabrication of multiphasic soft network composites for
            tissue engineering articular cartilage: A numerical model-based
            approach." Chemical Engineering Journal 340 (2018): 15-23.
        h_R_threshold: Threshold for the ratio of the indentation depth to the
            radius of the indenter.  If the ratio is greater than this value,
            then the Hertz model is not a valid approximation of the
            indentation response.
        use_regression_offsets: Include the indentation depth and force offsets
            as regression parameters.  They allow the model to fit the data
            more accurately for cases where the tip displacement does not equal
            the indentation depth and the measured force does not equal the
            indentation force.
        a_max_um: Upper bound for the tip displacement to indentation depth
            offset regression parameter.  If None, `a` can take any value.
        b_max_um: Upper bound for the measured force to indentation force offset
            regression parameter.  If None, `b` can take any value.
    """

    cycle: int = 1
    samples_to_skip: int = 0
    R_um: float = 500.0
    v: float = 0.484
    h_R_threshold: float = 0.1
    use_regression_offsets: bool = False
    a_max_um: Optional[float] = None
    b_max_uN: Optional[float] = None


@dataclasses.dataclass
class AnalyserParameters(microtester_g2.experiment.AnalyserParameters):
    """
    Parameters of an analyser of a microindentation experiment using a
    MicroTester G2.

    Args:
        cycles: Number of compression/recover cycles in the experiment.
        samples_to_skip: Number of samples at the beginning of the sample data
            to skip.
        R_um: Radius of the spherical indenter.
        v: Poisson's ratio of the sample.  See Bas, Onur, et al. "Rational
            design and fabrication of multiphasic soft network composites for
            tissue engineering articular cartilage: A numerical model-based
            approach." Chemical Engineering Journal 340 (2018): 15-23.
        h_R_threshold: Threshold for the ratio of the indentation depth to the
            radius of the indenter.  If the ratio is greater than this value,
            then the Hertz model is not a valid approximation of the
            indentation response.
        use_regression_offsets: Include the indentation depth and force offsets
            as regression parameters.  They allow the model to fit the data
            more accurately for cases where the tip displacement does not equal
            the indentation depth and the measured force does not equal the
            indentation force.
        a_max_um: Upper bound for the tip displacement to indentation depth
            offset regression parameter.  If None, `a` can take any value.
        b_max_um: Upper bound for the measured force to indentation force offset
            regression parameter.  If None, `b` can take any value.
    """

    cycles: int = 3
    samples_to_skip: int = 0
    R_um: float = 500.0
    v: float = 0.484
    h_R_threshold: float = 0.1
    use_regression_offsets: bool = False
    a_max_um: Optional[float] = None
    b_max_uN: Optional[float] = None


# === Data =================================================================== #


class Data(microtester_g2.Data):
    """
    Data of a microindentation experiment using a MicroTester G2}.

    Args:
        raw_frame: The raw data frame from which the processed data frame is
            created.
    """

    def __init__(self, raw_frame: microtester_g2.RawFrame) -> None:

        super().__init__(
            raw_frame,
            Frame(pd.DataFrame(columns=raw_frame.frame.columns), "Microindentation"),
        )

        self._a_um: float = 0.0
        self._b_uN: float = 0.0
        self._e_modulus_MPa: float = 0.0
        self._e_modulus_r2: float = 0.0
        self._energy_dissipated_uJ: float = 0.0

    @property
    def a_um(self) -> float:
        return self._a_um

    @property
    def b_uN(self) -> float:
        return self._b_uN

    @property
    def energy_dissipated_uJ(self) -> float:
        return self._energy_dissipated_uJ

    @property
    def e_modulus_MPa(self) -> float:
        return self._e_modulus_MPa

    @property
    def e_modulus_r2(self) -> float:
        return self._e_modulus_r2

    @property
    def processed_frame(self) -> Frame:
        return super().processed_frame  # type: ignore

    @processed_frame.setter
    def processed_frame(self, value: Frame) -> None:  # type: ignore
        super(Data, Data).processed_frame.__set__(self, value)  # type: ignore

    def process(self, parameters: DataParameters) -> None:  # type: ignore
        """
        Processes the raw data from the microindentation experiment using a
        MicroTester G2.

        Dataset filtering:
            - Compression cycle number of the sample.

        Columns that are populated:
            - Indentation Force: The force applied to indent the sample.
            - Regression Force: Force at each tip displacement point as
                calculated by the Hertz model regression equation of the force.
            - Indentation Depth: The depth of the indentation.
            - h/R: The ratio of the indentation depth to the radius of the
                indenter.

        Summary parameters that are calculated:
            - Hertz model regression equation parameters (E, a, and b in
                F = 4/3 * E / (1 - v^2) * R^0.5 * (h - a)^1.5 + b, where E is
                the Young's modulus of the sample)
            - Energy dissipated by the sample between the compression and
                relaxation cycles.

        Args:
            parameters: The parameters to use when processing the
                microindentation MicroTester G2 experiment data.
        """

        # Filter the raw data
        self.processed_frame = Frame(
            self.raw_frame.frame[
                (self.raw_frame.cycle == f"{parameters.cycle}-Compress")
                & (
                    self.raw_frame.tip_displacement / parameters.R_um
                    < parameters.h_R_threshold
                )
            ].iloc[parameters.samples_to_skip :],
            f"Cycle = {parameters.cycle}",
        )

        # Calculate the parameters of the Hertz equation that best fits the data
        # points
        self._a_um, self._b_uN, self._e_modulus_MPa, self._e_modulus_r2 = (
            self._execute_regression(
                parameters.R_um,
                parameters.v,
                parameters.use_regression_offsets,
                parameters.a_max_um,
                parameters.b_max_uN,
            )
        )

        # Calculate the energy dissipated by the sample during the compression
        # and relaxation cycles
        self._energy_dissipated_uJ = self._calculate_energy_dissipated_uJ(
            parameters.cycle, parameters.samples_to_skip
        )

        # Add the indentation force column
        # NOTE: indentation force = force - b
        self.processed_frame.indentation_force = self.processed_frame.force - self.b_uN

        # Add the regression force column
        self.processed_frame.regression_force = pd.Series(
            [
                self.y(
                    x,
                    parameters.R_um,
                    parameters.v,
                    self.e_modulus_MPa,
                    self.a_um,
                    self.b_uN,
                ).real  # NOTE: ignore imaginary part
                for x in self.processed_frame.tip_displacement
            ]
        )

        # Add the indentation depth column
        # NOTE: indentation depth = tip displacement - a
        self.processed_frame.indentation_depth = (
            self.processed_frame.tip_displacement - self.a_um
        )

        # Add the h/R column
        self.processed_frame.h_R = (
            self.processed_frame.indentation_depth / parameters.R_um  # type: ignore
        )

    def _calculate_energy_dissipated_uJ(
        self, cycle: int, samples_to_skip: int
    ) -> float:
        """
        Calculates the energy dissipated by the sample between the compression
        and relaxation cycles, which is the area between the force-tip
        displacement curve.  It is calculated using the shoelace formula (Gauss'
        area formula), which is as follows:

        A = 0.5 * abs(
            x0*y1 + x1*y2 + ... + x_{n-1}*y0
            - y0*x1 - y1*x2 - ... - y_{n-1}*x0
        )

        Args:
            cycle: The cycle number for which the dissipated energy is to be
                calculated.
            samples_to_skip: Number of samples at the beginning of the sample
                data to skip.

        Returns:
            The energy dissipated by the sample between the compression and
            relaxation cycles (in uJ).
        """

        x: NDArray[np.float64] = (
            self.raw_frame.tip_displacement[
                (self.raw_frame.cycle == f"{cycle}-Compress")
                | (self.raw_frame.cycle == f"{cycle}-Recover")
            ]
            .iloc[samples_to_skip:]
            .to_numpy(dtype=np.float64)  # type: ignore
        )
        y: NDArray[np.float64] = (
            self.raw_frame.force[
                (self.raw_frame.cycle == f"{cycle}-Compress")
                | (self.raw_frame.cycle == f"{cycle}-Recover")
            ]
            .iloc[samples_to_skip:]
            .to_numpy(dtype=np.float64)  # type: ignore
        )

        # Close the curve
        if (x[0] != x[-1]) or (y[0] != y[-1]):
            x = np.append(x, x[0])
            y = np.append(y, y[0])

        # Calculate the area between the curves using the shoelace formula
        return (
            0.5
            * np.abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))
            / 1000000  # NOTE: convert from pJ to uJ
        )

    def _execute_regression(
        self,
        R_um: float,
        v: float,
        use_regression_offsets: bool,
        a_max_um: Optional[float],
        b_max_uN: Optional[float],
    ) -> tuple[float, float, float, float]:
        """
        Executes the regression to determine the Hertz model equation parameters
        and the corresponding coefficient of determination.

        Args:
            R_um: The radius of the indenter.
            v: The Poisson's ratio of the sample.
            use_regression_offsets: Include the indentation depth and force
                offsets  as regression parameters.  They allow the model to fit
                the data more accurately for cases where the tip displacement
                does not equal the indentation depth and the measured force does
                not equal the indentation force.
            a_max_um: Upper bound for the tip displacement to indentation depth
                offset regression parameter.  If None, `a` can take any value.
            b_max_um: Upper bound for the measured force to indentation force
                offset regression parameter.  If None, `b` can take any value.

        Returns:
            Tuple of a, b, and E-modulus (the Hertz model regression equation
            parameters) and their corresponding coefficient of determination.
        """

        x: "pd.Series[float]" = self.processed_frame.tip_displacement
        y: "pd.Series[float]" = self.processed_frame.force

        a_um: float
        b_uN: float
        e_modulus_MPa: float
        e_modulus_r2: float

        try:
            # Include offsets in the regression analysis
            if use_regression_offsets:
                a_max_um = a_max_um if a_max_um is not None else np.inf
                b_max_uN = b_max_uN if b_max_uN is not None else np.inf

                [e_modulus_MPa, a_um, b_uN], _ = curve_fit(  # type: ignore
                    lambda _x, e, a, b: self.y(_x, R_um, v, e, a, b),  # type: ignore
                    x,
                    y,
                    p0=[1.0, x.min(), y.min()],  # type: ignore
                    bounds=(
                        (0.0, -a_max_um, -b_max_uN),
                        (np.inf, x.min(), y.min()),
                    ),
                    maxfev=20000,
                )
            # Fix offsets at the minimum tip displacement
            else:
                a_um = x.min()
                b_uN = y.iloc[x.idxmin()]  # type: ignore

                [e_modulus_MPa], _ = curve_fit(  # type: ignore
                    lambda _x, e: self.y(_x, R_um, v, e, a_um, b_uN),  # type: ignore
                    x,
                    y,
                    p0=[1.0],
                    bounds=[
                        (0.0,),
                        (np.inf,),
                    ],
                    maxfev=20000,
                )

        except:
            # Solution could not converge
            print("Solution could not converge")
            return float("nan"), float("nan"), float("nan"), float("nan")

        e_modulus_r2 = utils.calculate_r2(
            list(y),
            [self.y(i, R_um, v, e_modulus_MPa, a_um, b_uN).real for i in x],  # type: ignore
        )

        return [a_um, b_uN, e_modulus_MPa, e_modulus_r2]  # type: ignore

    @staticmethod
    def y(x: float, R: float, v: float, e: float, a: float, b: float) -> float:
        """
        Calculates the force according to the following equation:
        y = 4/3 * e / (1 - v^2) * R^0.5 * x^1.5

        Args:
            x: The tip displacement.
            R: The radius of the indenter.
            v: The Poisson's ratio of the sample.
            e: The Young's modulus of the sample.
            a: The tip displacement to indentation depth offset.
            b: The measured force to indentation force offset.

        Returns:
            The force at tip displacement x.
        """

        return 4 / 3 * e / (1 - v**2) * (R**0.5) * ((x - a) ** 1.5) + b


# === Results ================================================================ #


class Summary(microtester_g2.Summary):
    """
    Summary of the microindentation MicroTester G2 experiment.
    """

    def __init__(self) -> None:

        super().__init__(
            pd.DataFrame(
                columns=[
                    "Cycle",
                    "a [um]",
                    "b [uN]",
                    "E-modulus [MPa]",
                    "E-modulus R^2 [MPa^2/MPa^2]",
                    "Energy dissipated [uJ]",
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
            parameters: The parameters of a microindentation experiment
                using a MicroTester G2 used to process the data.
        """

        self._frame.loc[len(self._frame)] = [
            parameters.cycle,
            data.a_um,
            data.b_uN,
            data.e_modulus_MPa,
            data.e_modulus_r2,
            data.energy_dissipated_uJ,
        ]


# === Analysers ============================================================== #


class Analyser(microtester_g2.Analyser):
    """
    Analyser of the microindentation MicroTester G2 experiment.

    Args:
        input_csv: The path to the CSV file containing the output of the
            microindentation MicroTester G2 experiment.
        output_xlsx: The path to the Excel file which will contain the analysis
            results.
        parameters: The parameters to use when analysing the microindentation
            MicroTester G2 experiment.
    """

    def __init__(
        self,
        input_csv: Path,
        output_xlsx: Path,
        parameters: AnalyserParameters,
    ) -> None:

        super().__init__(input_csv, output_xlsx, parameters, Summary())

        for _ in range(parameters.cycles):
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
        Analyses the output of the microindentation MicroTester G2 experiment.
        """

        # Resize the processed data based on the number of cycles
        if len(self.data) > self.parameters.cycles:
            del self.data[self.parameters.cycles :]
        else:
            self.data.extend(
                [
                    Data(self.raw_frame)
                    for _ in range(self.parameters.cycles - len(self.data))
                ]
            )

        self.summary.clear_all_rows()

        for i in range(len(self.data)):
            parameters = DataParameters(
                i + 1,
                self.parameters.samples_to_skip,
                self.parameters.R_um,
                self.parameters.v,
                self.parameters.h_R_threshold,
                self.parameters.use_regression_offsets,
                self.parameters.a_max_um,
                self.parameters.b_max_uN,
            )
            self.data[i].process(parameters)
            self.summary.append_row(self.data[i], parameters)


# === User Interface Widgets ================================================= #


class Widget(microtester_g2.Widget):
    """
    User interface widget for the microindentation MicroTester G2 experiment.
    """

    def __init__(self) -> None:
        super().__init__(view.Ui_w_Microindentation(), AnalyserParameters())  # type: ignore

    @property
    def experiment(self) -> str:
        return "Microindentation"

    @property
    def parameters(self) -> AnalyserParameters:
        return super().parameters  # type: ignore

    @property
    def view(self) -> view.Ui_w_Microindentation:  # type: ignore
        return super().view  # type: ignore

    def create_analyser(  # type: ignore
        self, input_csv: Path, output_xlsx: Path, parameters: AnalyserParameters
    ) -> Analyser:
        """
        Creates the experiment analyser.

        Args:
            input_csv: The path to the CSV file containing the output of the
                microindentation MicroTester G2 experiment.
            output_xlsx: The path to the Excel file which will contain the
                analysis results.
            parameters: The parameters to use when analysing the microindentation
                MicroTester G2 experiment.
        """

        return Analyser(input_csv, output_xlsx, parameters)

    def init(self) -> None:
        """
        Initialises the widget by setting the input fields to the defaults of
        the parameters to use when analysing the experiment and connecting any
        signals with an associated slot.
        """

        # Set the input fields to the defaults
        self.view.sb_Cycles.setValue(self.parameters.cycles)
        self.view.sb_SamplesToSkip.setValue(self.parameters.samples_to_skip)
        self.view.sb_IndenterRadius.setValue(self.parameters.R_um)
        self.view.sb_PoissonsRatio.setValue(self.parameters.v)
        self.view.sb_HRThreshold.setValue(self.parameters.h_R_threshold)
        self.view.cb_RegressionOffsets.setChecked(
            self.parameters.use_regression_offsets
        )
        self.view.cb_OffsetBounds.setChecked(
            self.parameters.use_regression_offsets
            and self.parameters.a_max_um is not None
            and self.parameters.b_max_uN is not None
        )
        self.view.sb_OffsetTipDisplacement.setValue(self.parameters.a_max_um or 0.0)
        self.view.sb_OffsetForce.setValue(self.parameters.b_max_uN or 0.0)

        # Connect signals with slots
        self.view.cb_RegressionOffsets.checkStateChanged.connect(
            self._handle_cb_RegressionOffsets_changed
        )
        self.view.cb_OffsetBounds.checkStateChanged.connect(
            self._handle_cb_OffsetBounds_changed
        )

        # Set initial views
        self._handle_cb_RegressionOffsets_changed()
        self._handle_cb_OffsetBounds_changed()

    def sync_parameters(self) -> None:
        """
        Synchronise the parameters to use when analysing the experiment with the
        widget input fields.
        """

        self.parameters.cycles = self.view.sb_Cycles.value()
        self.parameters.samples_to_skip = self.view.sb_SamplesToSkip.value()
        self.parameters.R_um = self.view.sb_IndenterRadius.value()
        self.parameters.v = self.view.sb_PoissonsRatio.value()
        self.parameters.h_R_threshold = self.view.sb_HRThreshold.value()
        self.parameters.use_regression_offsets = (
            self.view.cb_RegressionOffsets.isChecked()
        )
        self.parameters.a_max_um = (
            self.view.sb_OffsetTipDisplacement.value()
            if self.view.cb_RegressionOffsets.isChecked()
            and self.view.cb_OffsetBounds.isChecked()
            else None
        )
        self.parameters.b_max_uN = (
            self.view.sb_OffsetForce.value()
            if self.view.cb_RegressionOffsets.isChecked()
            and self.view.cb_OffsetBounds.isChecked()
            else None
        )

    def _handle_cb_OffsetBounds_changed(self) -> None:
        """
        Sets the visibility of sb_OffsetTipDisplacement and sb_OffsetForce to
        the state of cb_RegressionOffsets and cb_OffsetBounds.
        """

        self.view.l_OffsetTipDisplacement.setDisabled(
            not self.view.cb_RegressionOffsets.isChecked()
            or not self.view.cb_OffsetBounds.isChecked()
        )
        self.view.l_OffsetForce.setDisabled(
            not self.view.cb_RegressionOffsets.isChecked()
            or not self.view.cb_OffsetBounds.isChecked()
        )
        self.view.sb_OffsetTipDisplacement.setDisabled(
            not self.view.cb_RegressionOffsets.isChecked()
            or not self.view.cb_OffsetBounds.isChecked()
        )
        self.view.sb_OffsetForce.setDisabled(
            not self.view.cb_RegressionOffsets.isChecked()
            or not self.view.cb_OffsetBounds.isChecked()
        )

    def _handle_cb_RegressionOffsets_changed(self) -> None:
        """
        Sets the visibility of cb_OffsetBounds to the state of
        cb_RegressionOffsets and sets the visibility of sb_OffsetTipDisplacement
        and sb_OffsetForce to the state of cb_RegressionOffsets and
        cb_OffsetBounds.
        """

        self.view.cb_OffsetBounds.setDisabled(
            not self.view.cb_RegressionOffsets.isChecked()
        )
        self.view.l_OffsetTipDisplacement.setDisabled(
            not self.view.cb_RegressionOffsets.isChecked()
            or not self.view.cb_OffsetBounds.isChecked()
        )
        self.view.l_OffsetForce.setDisabled(
            not self.view.cb_RegressionOffsets.isChecked()
            or not self.view.cb_OffsetBounds.isChecked()
        )
        self.view.sb_OffsetTipDisplacement.setDisabled(
            not self.view.cb_RegressionOffsets.isChecked()
            or not self.view.cb_OffsetBounds.isChecked()
        )
        self.view.sb_OffsetForce.setDisabled(
            not self.view.cb_RegressionOffsets.isChecked()
            or not self.view.cb_OffsetBounds.isChecked()
        )
