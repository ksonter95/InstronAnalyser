import argparse
import instrument.instrument as instrument
import instrument.instron_68tm.instron_68tm as instron_68tm


import numpy as np
import pandas as pd

from pathlib import Path
from scipy.optimize import curve_fit  # type: ignore
from typing import Optional

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

        # Regression equation parameters for equation y = a * e^(-t / tau) + b
        self._a: float = 0.0
        self._b: float = 0.0
        self._tau: float = 1.0

    @property
    def a(self) -> float:
        return self._a

    @property
    def b(self) -> float:
        return self._b

    @property
    def max_force_N(self) -> float:
        return self.processed_frame.force.max()  # type: ignore

    @property
    def max_stress_MPa(self) -> float:
        return self.processed_frame.stress.max()  # type: ignore

    @property
    def min_force_N(self) -> float:
        return self.processed_frame.force.min()  # type: ignore

    @property
    def min_stress_MPa(self) -> float:
        return self.processed_frame.stress.min()  # type: ignore

    @property
    def processed_frame(self) -> Frame:
        return super().processed_frame  # type: ignore

    @processed_frame.setter
    def processed_frame(self, value: Frame) -> None:  # type: ignore
        super(Data, Data).processed_frame.__set__(self, value)  # type: ignore

    @property
    def tau(self) -> float:
        return self._tau

    def process(  # type: ignore
        self,
        relaxation_strain_pct: float,
        epsilon_pct: float,
        regression_data_points: Optional[int],
    ) -> None:
        """
        Processes the raw data from the stepwise compression experiment using an
        Instron 68TM.

        Dataset filtering:
            - Relaxation phase of the sample at the specified strain.

        Columns that are populated:
            - Relative Time: Time elapsed since the start of the relaxation
                phase.
            - Stress Regression: Stress at each relative time point as
                calculated by the exponential decay regression equation of the
                stress.

        Summary parameters that are calculated:
            - Exponential decay regression equation parameters (a, b, and tau in
                y = a * e^(-t / tau) + b)

        Args:
            relaxation_strain_pct: The strain at which the sample is maintained
                while the sample relaxes.
            epsilon_pct: Tolerance for the strain within which it is considered
                to be within the relaxation phase.
            regression_data_points: Maximum number of data points to be included
                in the regression analysis.
        """

        # Filter the raw data to only obtain the data within the relation phase
        # of the sample for the specified strain
        self.processed_frame = Frame(
            self.raw_frame.frame[
                (self.raw_frame.strain > (relaxation_strain_pct - epsilon_pct))
                & (self.raw_frame.strain < (relaxation_strain_pct + epsilon_pct))
            ],
            f"Strain = {round(relaxation_strain_pct, 1)}%",
        )

        # Add the relative time column
        self.processed_frame.relative_time = (
            self.processed_frame.time - self.processed_frame.initial_time_s
        )

        # Calculate the parameters of the exponential decay equation that best
        # fits the data points
        [self._a, self._b, self._tau], _ = curve_fit(  # type: ignore
            self.y,
            self.processed_frame.relative_time.head(  # type: ignore
                regression_data_points
                or self.processed_frame.frame.index.size  # type: ignore
            ),
            self.processed_frame.stress.head(  # type: ignore
                regression_data_points
                or self.processed_frame.frame.index.size  # type: ignore
            ),
        )

        # Add the regression stress column directly after the stress column
        self.processed_frame.regression_stress = pd.Series(
            [
                self.y(t, self.a, self.b, self.tau)  # type: ignore
                for t in self.processed_frame.relative_time  # type: ignore
            ]
        )

    @staticmethod
    def y(t: float, a: float, b: float, tau: float) -> float:
        """
        Calculates the stress according to the following equation:
        y = a * e^(-t / tau) + b

        Args:
            t: Time at which the stress is to be calculated.
            a: Amplitude of the exponential decay.
            b: Baseline value of the function.
            tau: Time constant of the exponential decay.

        Returns:
            Stress at time t.
        """

        return a * np.exp(-t / tau) + b


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
                    "a",
                    "b",
                    "tau",
                ]
            )
        )

    def append_row(  # type: ignore
        self,
        strain_pct: float,
        min_stress_MPa: float,
        max_stress_MPa: float,
        min_force_N: float,
        max_force_N: float,
        a: float,
        b: float,
        tau: float,
    ) -> None:
        """
        Append a row to the underlying pd.DataFrame representation of the
        summary.

        Args:
            strain_pct: The relaxation strain.
            min_stress_MPa: The minimum stress during relaxation.
            max_stress_MPa: The maximum stress during relaxation.
            min_force_N: The minimum force during relaxation.
            max_force_N: The maximum force during relaxation.
            a: The exponential decay equation coefficient a
                (y = a * e^(-t / tau) + b)
            b: The exponential decay equation coefficient b
                (y = a * e^(-t / tau) + b)
            tau: The exponential decay equation coefficient tau
                (y = a * e^(-t / tau) + b)
        """

        self._frame.loc[len(self._frame)] = [
            strain_pct,
            min_stress_MPa,
            max_stress_MPa,
            min_force_N,
            max_force_N,
            a,
            b,
            tau,
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
        relaxation_strains_pct: The strains at which the sample has been
            configured to relax.
        epsilon_pct: Tolerance for the strain within which it is considered to
            be maintained for each relaxation interval.
        regression_data_points: Maximum number of data points to be included in
            the regression analysis.
    """

    def __init__(
        self,
        input_csv: Path,
        output_xlsx: Path,
        relaxation_strains_pct: list[float],
        epsilon_pct: float,
        regression_data_points: Optional[int],
    ) -> None:

        super().__init__(input_csv, output_xlsx, Summary())

        self._regression_data_points: Optional[int]
        self._relaxation_strains_pct: list[float]
        self._epsilon_pct: float

        self.epsilon_pct = epsilon_pct
        self.regression_data_points = regression_data_points
        self.relaxation_strains_pct = relaxation_strains_pct

    @property
    def data(self) -> list[Data]:  # type: ignore
        return super().data  # type: ignore

    @data.setter
    def data(self, value: list[Data]) -> None:  # type: ignore
        super(Analyser, Analyser).data.__set__(self, value)  # type: ignore

    @property
    def epsilon_pct(self) -> float:
        return self._epsilon_pct

    @epsilon_pct.setter
    def epsilon_pct(self, value: float) -> None:
        self._epsilon_pct = value

    @property
    def regression_data_points(self) -> Optional[int]:
        return self._regression_data_points

    @regression_data_points.setter
    def regression_data_points(self, value: Optional[int]) -> None:
        self._regression_data_points = value

    @property
    def relaxation_strains_pct(self) -> list[float]:
        return self._relaxation_strains_pct

    @relaxation_strains_pct.setter
    def relaxation_strains_pct(self, value: list[float]) -> None:
        self._relaxation_strains_pct = value

        # Resize the processed data based on the number of relaxation intervals
        if len(self.data) > len(self._relaxation_strains_pct):
            del self.data[len(self._relaxation_strains_pct) :]
        else:
            self.data.extend(
                [
                    Data(self.raw_frame)
                    for _ in range(len(self._relaxation_strains_pct) - len(self.data))
                ]
            )

    @property
    def summary(self) -> Summary:
        return super().summary  # type: ignore

    def analyse(self) -> None:
        """
        Analyses the output of the stepwise compression Instron 68TM experiment.
        """

        self.summary.clear_all_rows()

        for i in range(len(self._relaxation_strains_pct)):
            self.data[i].process(
                self._relaxation_strains_pct[i],
                self._epsilon_pct,
                self._regression_data_points,
            )

            self.summary.append_row(
                self._relaxation_strains_pct[i],
                self.data[i].min_stress_MPa,
                self.data[i].max_stress_MPa,
                self.data[i].min_force_N,
                self.data[i].max_force_N,
                self.data[i].a,
                self.data[i].b,
                self.data[i].tau,
            )


# === Command-line parsers =================================================== #


class Parser(instron_68tm.Parser):
    """
    Parser for the stepwise compression Instron 68TM experiment.

    Args:
        parsed_arguments: The parsed command-line arguments.
    """

    def __init__(self, parsed_arguments: argparse.Namespace) -> None:

        super().__init__(parsed_arguments)

        self._epsilon_pct: float = parsed_arguments.epsilon
        self._regression_data_points: int = parsed_arguments.regression_data_points
        self._relaxation_strains_pct: list[float] = parsed_arguments.relaxation_strains

    def create_analysers(self) -> list[Analyser]:
        """
        Creates the stepwise compression Instron 68TM experiment analysers from
        the parsed command-line arguments.

        Returns:
            list[Analyser]: List of all stepwise compression Instron 68Tm
                experiment analysers.
        """

        return [
            Analyser(
                input_csv,
                output_xlsx,
                self._relaxation_strains_pct,
                self._epsilon_pct,
                self._regression_data_points,
            )
            for input_csv, output_xlsx in self._files
        ]

    @staticmethod
    def add_parser(subparser: argparse._SubParsersAction) -> None:  # type: ignore
        """
        Adds the stepwise compression Instron 68TM experiment parser to the
        Instron 68TM experiment subparser.

        Args:
            subparser: Instron 68TM experiment subparser to which to add the
                stepwise compression Instron 68TM experiment parser.
        """

        parser: argparse.ArgumentParser = subparser.add_parser(  # type: ignore
            "stepwise",
            description="Analyses the data from a stepwise compression Instron "
            "68TM experiment",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )

        parser.add_argument(  # type: ignore
            "-r",
            "--relaxation-strains",
            help="The strains at which the sample has been configured to relax",
            type=instrument.ArgparseTypes.list_percentage_float,
            default="[5, 10, 15, 20, 25, 30]",
        )
        parser.add_argument(  # type: ignore
            "-e",
            "--epsilon",
            help="Allowable percentage tolerance on the specified strain for "
            "creating the dataset at the required strain",
            type=instrument.ArgparseTypes.percentage_float,
            default=0.01,
        )
        parser.add_argument(  # type: ignore
            "-n",
            "--regression-data-points",
            help="Number of data points to include in the regression analysis",
            type=instrument.ArgparseTypes.positive_non_zero_integer,
        )
