import numpy as np
import pandas as pd
import warnings

from pathlib import Path
from scipy.integrate import cumulative_trapezoid  # type: ignore
from scipy.optimize import curve_fit  # type: ignore
from typing import Any, Optional


class DataFrame:
    """
    Wrapper for pd.DataFrame that allows the class to be interacted with like a
    standard pd.DataFrame.

    Args:
        data_frame: pd.DataFrame to wrap.
    """

    def __init__(self, data_frame: pd.DataFrame) -> None:

        self._data_frame: pd.DataFrame = data_frame.copy(deep=True)
        self._data_frame.reset_index(drop=True, inplace=True)

    def __str__(self) -> str:
        return str(self._data_frame)

    @property
    def displacement(self) -> "pd.Series[float]":
        return self._data_frame["Displacement (mm)"]  # type: ignore

    @property
    def e_modulus(self) -> "pd.Series[float]":
        return self._data_frame["E-modulus (MPa)"]  # type: ignore

    @property
    def force(self) -> "pd.Series[float]":
        return self._data_frame["Force (N)"]  # type: ignore

    @property
    def frame(self) -> pd.DataFrame:
        return self._data_frame

    @property
    def initial_time_s(self) -> float:
        return self.time[0]

    @property
    def strain(self) -> "pd.Series[float]":
        return self._data_frame["Strain (%)"]  # type: ignore

    @property
    def stress(self) -> "pd.Series[float]":
        return self._data_frame["Compressive stress (MPa)"]  # type: ignore

    @property
    def time(self) -> "pd.Series[float]":
        return self._data_frame["Time (s)"]  # type: ignore

    @staticmethod
    def load(csv: Path) -> "DataFrame":
        """
        Loads the CSV file into a DataFrame and validates its contents.

        Args:
            csv: The path to the CSV file containing the data set.
        """

        try:
            # Read the CSV file
            # NOTE: the column headings are split across two rows and formatted
            #       weirdly such that all units are on the second row except the
            #       strain.  Therefore, the two rows are combined into one
            data_frame: pd.DataFrame = pd.read_csv(  # type: ignore
                csv, skiprows=19, header=[0, 1]
            ).iloc[:, :5]
            data_frame.columns = [
                (
                    " ".join(map(str, c)).strip()
                    if not c[1].startswith("Unnamed")
                    else str(c[0])
                )
                for c in data_frame.columns
            ]

            # Validate the CSV file
            #  - Data headings must be in rows 19-20, columns 0-4 (0-indexed) and
            #    must be:
            #       Time, Displacement, Force, Strain (%), Compressive stress
            #       (s), (mm),          (N),   ,           (MPa)
            #  - Data must be in rows 21-... (0-indexed) and must be all floating
            #    point numbers
            headings: list[str] = [
                "Time (s)",
                "Displacement (mm)",
                "Force (N)",
                "Strain (%)",
                "Compressive stress (MPa)",
            ]
            if (
                data_frame.columns.tolist() != headings
                or not data_frame.notna().all().all()  # type: ignore
            ):
                raise ValueError

        except:
            raise ValueError(f"Invalid CSV file: {csv}")

        # Add the Young's modulus column
        # E = σ / ε
        #   - E = Young's modulus (in Pa)
        #   - σ = stress (in Pa)
        #   - ε = strain (unitless)
        # NOTE: handling divide by zero runtime warning
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            data_frame["E-modulus (MPa)"] = data_frame["Compressive stress (MPa)"] / (
                data_frame["Strain (%)"] / 100
            )

        return DataFrame(data_frame)


class RelaxationDataFrame(DataFrame):
    """
    Wrapper for pd.DataFrame that allows the class to be interacted with like a
    standard pd.DataFrame.  It contains all the data from a relaxation test.

    Args:
        data_frame: pd.DataFrame to wrap.
    """

    def __init__(self, data_frame: pd.DataFrame) -> None:

        super().__init__(data_frame)

        # Initially populate the processed data columns with default values
        self.relative_time = pd.Series([0.0] * self._data_frame.index.size)  # type: ignore
        self.regression_force = pd.Series([0] * self._data_frame.index.size)  # type: ignore

    @property
    def regression_force(self) -> "pd.Series[float]":
        return self._data_frame["Regression Force (N)"]  # type: ignore

    @regression_force.setter
    def regression_force(self, value: "pd.Series[float]") -> None:
        self._data_frame["Regression Force (N)"] = value

        # Move the regression force column to be directly after the force column
        column: pd.Series = self._data_frame.pop("Regression Force (N)")  # type: ignore
        self._data_frame.insert(  # type: ignore
            self._data_frame.columns.get_loc("Force (N)") + 1,  # type: ignore
            "Regression Force (N)",
            column,
        )

    @property
    def relative_time(self) -> "pd.Series[float]":
        return self._data_frame["Relative Time (s)"]  # type: ignore

    @relative_time.setter
    def relative_time(self, value: "pd.Series[float]") -> None:
        self._data_frame["Relative Time (s)"] = value

        # Move the relative time column to be directly after the time column
        column: pd.Series = self._data_frame.pop("Relative Time (s)")  # type: ignore
        self._data_frame.insert(  # type: ignore
            self._data_frame.columns.get_loc("Time (s)") + 1,  # type: ignore
            "Relative Time (s)",
            column,
        )


class FailureDataFrame(DataFrame):
    """
    Wrapper for pd.DataFrame that allows the class to be interacted with like a
    standard pd.DataFrame.  It contains all the data from a compression to
    failure test.

    Args:
        data_frame: pd.DataFrame to wrap.
    """

    def __init__(self, data_frame: pd.DataFrame) -> None:

        super().__init__(data_frame)

        # Initially populate the processed data columns with default values
        self.toughness = pd.Series([0.0] * self._data_frame.index.size)  # type: ignore

    @property
    def toughness(self) -> "pd.Series[float]":
        return self._data_frame["Toughness (MPa)"]  # type: ignore

    @toughness.setter
    def toughness(self, value: "pd.Series[float]") -> None:
        self._data_frame["Toughness (MPa)"] = value


class SummaryFrame:
    """
    Wrapper for pd.DataFrame that allows the class to be interacted with like a
    standard pd.DataFrame.

    Args:
        summary_frame: pd.DataFrame to wrap.
    """

    def __init__(self, summary_frame: pd.DataFrame) -> None:

        self._summary_frame: pd.DataFrame = summary_frame.copy(deep=True)
        self._summary_frame.reset_index(drop=True, inplace=True)

    def __str__(self) -> str:
        return str(self._summary_frame)

    @property
    def frame(self) -> pd.DataFrame:
        return self._summary_frame


class RelaxationSummaryFrame(SummaryFrame):
    """
    Wrapper for pd.DataFrame that allows the class to be interacted with like a
    standard pd.DataFrame.  It contains the summary from a relaxation test.
    """

    def __init__(self) -> None:

        super().__init__(
            pd.DataFrame(
                columns=[
                    "Strain (%)",
                    "Min force (N)",
                    "Max force (N)",
                    "Min stress (MPa)",
                    "Max stress (MPa)",
                    "Min E-modulus (MPa)",
                    "Max E-modulus (MPa)",
                    "a",
                    "b",
                    "tau",
                ]
            )
        )

    def append_row(
        self,
        strain_pct: float,
        min_force_N: float,
        max_force_N: float,
        min_stress_MPa: float,
        max_stress_MPa: float,
        min_e_modulus_MPa: float,
        max_e_modulus_MPa: float,
        a: float,
        b: float,
        tau: float,
    ) -> None:
        """
        Append a row to the summary frame.

        Args:
            strain_pct: The relaxation strain.
            min_force_N: The minimum force during relaxation.
            max_force_N: The maximum force during relaxation.
            min_stress_MPa: The minimum stress during relaxation.
            max_stress_MPa: The maximum stress during relaxation.
            min_e_modulus_MPa: The minimum E-modulus during relaxation.
            max_e_modulus_MPa: The maximum E-modulus during relaxation.
            a: The exponential decay equation coefficient a
                (y = a * e^(-t / tau) + b)
            b: The exponential decay equation coefficient b
                (y = a * e^(-t / tau) + b)
            tau: The exponential decay equation coefficient tau
                (y = a * e^(-t / tau) + b)
        """

        self._summary_frame.loc[len(self._summary_frame)] = [
            strain_pct,
            min_force_N,
            max_force_N,
            min_stress_MPa,
            max_stress_MPa,
            min_e_modulus_MPa,
            max_e_modulus_MPa,
            a,
            b,
            tau,
        ]


class FailureSummaryFrame(SummaryFrame):
    """
    Wrapper for pd.DataFrame that allows the class to be interacted with like a
    standard pd.DataFrame.  It contains the summary from a compression to
    failure test.
    """

    def __init__(self) -> None:

        super().__init__(
            pd.DataFrame(
                columns=[
                    "Ultimate strain (%)",
                    "Ultimate force (N)",
                    "Ultimate strength (MPa)",
                    "Aborted?",
                    "Slipped?",
                    "Yield strain (%)",
                    "Yield force (N)",
                    "Yield strength (MPa)",
                    "Toughness strain (%)",
                    "Toughness (MPa)",
                    "Stiffness strain (%)",
                    "Stiffness (MPa)",
                ]
            )
        )

    def append_row(
        self,
        ultimate_strain_pct: float,
        ultimate_force_N: float,
        ultimate_strength_MPa: float,
        aborted: float,
        slipped: float,
        yield_strain_pct: float,
        yield_force_N: float,
        yield_strength_MPa: float,
        toughness_strain_pct: float,
        toughness_MPa: float,
        stiffness_strain_pct: float,
        stiffness_MPa: float,
    ) -> None:
        """
        Append a row to the summary frame.

        Args:
            ultimate_strain_pct: The strain at which the sample broke or the
                test was aborted.
            ultimate_force_N: The force at which the sample broke or the test
                was aborted.
            ultimate_strength_MPa: The stress at which the sample broke or the
                test was aborted.
            aborted: Flag indicating whether the test was aborted or if the
                sample broke.  This flag is used to interpret the meaning of the
                ultimate values.
            slipped: Flag indicating whether the sample slipped during the test.
                Slipped is defined as it partially breaking before continuing
                on the achieve a greater ultimate strength.
            yield_strain_pct: The strain at which the sample deformation changes
                from elastic to plastic.
            yield_force_N: The force at which the sample deformation changes
                from elastic to plastic.
            yield_strength_MPa: The stress at which the sample deformation
                changes from elastic to plastic.
            toughness_strain_pct: The strain at which the toughness was
                calculated.
            toughness_MPa: The toughness of the sample, which is defined as the
                area under the stress-strain curve up until a specified strain.
            stiffness_strain_pct: The strain at which the stiffness was
                calculated.
            stiffness_MPa: The stiffness of the sample, which is defined as the
                stress at a specified strain.
        """

        self._summary_frame.loc[len(self._summary_frame)] = [
            ultimate_strain_pct,
            ultimate_force_N,
            ultimate_strength_MPa,
            aborted,
            slipped,
            yield_strain_pct,
            yield_force_N,
            yield_strength_MPa,
            toughness_strain_pct,
            toughness_MPa,
            stiffness_strain_pct,
            stiffness_MPa,
        ]


class Data:
    """
    Base class for all data.

    Args:
        raw_data_frame: The raw data frame which will be used to create the
            processed data.
        sheet_name: The name of the Excel sheet to which the processed data will
            be written.
    """

    def __init__(self, raw_data_frame: DataFrame, sheet_name: str) -> None:

        self._processed_data_frame: DataFrame

        self.raw_data_frame: DataFrame = raw_data_frame
        self.processed_data_frame = self.raw_data_frame
        self.sheet_name: str = sheet_name

    @property
    def processed_data_frame(self) -> DataFrame:
        return self._processed_data_frame

    @processed_data_frame.setter
    def processed_data_frame(self, value: DataFrame) -> None:
        self._processed_data_frame = value

    def write_to_excel(self, writer: pd.ExcelWriter) -> None:
        self.processed_data_frame.frame.to_excel(  # type: ignore
            writer,
            sheet_name=self.sheet_name,
            index=False,
        )

    def process_raw_data(self, *args: list[Any], **kwargs: dict[str, Any]) -> None:
        """
        Processes the raw data read from the CSV output of the Instron.  This
        could include populating additional columns or calculating summary
        parameters of the dataset.
        """

        pass


class RawData(Data):
    """
    Data storage class for the raw data obtained from the output of the Instron.

    Args:
        input_csv: The path to the CSV file containing the output of the
            Instron.
    """

    def __init__(self, input_csv: Path) -> None:

        super().__init__(DataFrame.load(input_csv), "Raw Data")


class ProcessedData(Data):
    """
    Base class for all processed data.

    Args:
        raw_data_frame: The raw data frame which will be used to create the
            processed data.
        sheet_name: The name of the Excel sheet to which the processed data will
            be written.
    """

    pass


class RelaxationData(ProcessedData):
    """
    Data storage class for the data where the strain is maintained while the
    sample relaxes.  Columns containing the relative time and force regression
    are also calculated and added to the data.

    Args:
        raw_data_frame: The raw data frame which will be used to create the
            processed data.
    """

    def __init__(self, raw_data_frame: DataFrame) -> None:

        super().__init__(raw_data_frame, "Strain = ?%")

        # Regression equation parameters for equation y = a * e^(-t / tau) + b
        self.a: float = 0.0
        self.b: float = 0.0
        self.tau: float = 1.0

    @property
    def max_e_modulus_MPa(self) -> float:
        return self.processed_data_frame.e_modulus.max()  # type: ignore

    @property
    def max_force_N(self) -> float:
        return self.processed_data_frame.force.max()  # type: ignore

    @property
    def max_stress_MPa(self) -> float:
        return self.processed_data_frame.stress.max()  # type: ignore

    @property
    def min_e_modulus_MPa(self) -> float:
        return self.processed_data_frame.e_modulus.min()  # type: ignore

    @property
    def min_force_N(self) -> float:
        return self.processed_data_frame.force.min()  # type: ignore

    @property
    def min_stress_MPa(self) -> float:
        return self.processed_data_frame.stress.min()  # type: ignore

    @property
    def processed_data_frame(self) -> RelaxationDataFrame:
        return super().processed_data_frame  # type: ignore

    @processed_data_frame.setter
    def processed_data_frame(self, value: RelaxationDataFrame) -> None:  # type: ignore
        super(RelaxationData, RelaxationData).processed_data_frame.__set__(self, value)  # type: ignore

    def process_raw_data(  # type: ignore
        self,
        relaxation_strain_pct: float,
        epsilon_pct: float,
        regression_data_points: Optional[int],
    ) -> None:
        """
        Processes the raw data read from the CSV output of the Instron.

        Dataset filtering:
            - Relaxation phase of the sample at the specified strain.

        Columns that are populated:
            - Relative Time: Time elapsed since the start of the relaxation
                phase.
            - Force Regression: Force at each relative time point as calculated
                by the exponential decay regression equation of the force.

        Summary parameters that are calculated:
            - Exponential decay regression equation parameters (a, b, and tau in
                y = a * e^(-t / tau) + b)

        Args:
            relaxation_strain_pct: The strain at which the sample is maintained
                while the sample relaxes.
            epsilon_pct: Tolerance for the strain within which it is considered
                to be maintained.
            regression_data_points: Maximum number of data points to be included
                in the regression analysis.
        """

        self.sheet_name = f"Strain = {round(relaxation_strain_pct, 1)}%"

        # Filter the raw data to only obtain the data within the relation phase
        # of the sample for the specified strain
        self.processed_data_frame = RelaxationDataFrame(
            self.raw_data_frame.frame[
                (self.raw_data_frame.strain > (relaxation_strain_pct - epsilon_pct))
                & (self.raw_data_frame.strain < (relaxation_strain_pct + epsilon_pct))
            ]
        )

        # Add the relative time column
        self.processed_data_frame.relative_time = (
            self.processed_data_frame.time - self.processed_data_frame.initial_time_s
        )

        # Calculate the parameters of the exponential decay equation that best
        # fits the data points
        [self.a, self.b, self.tau], _ = curve_fit(  # type: ignore
            self.y,
            self.processed_data_frame.relative_time.head(  # type: ignore
                regression_data_points
                or self.processed_data_frame.frame.index.size  # type: ignore
            ),
            self.processed_data_frame.force.head(  # type: ignore
                regression_data_points
                or self.processed_data_frame.frame.index.size  # type: ignore
            ),
        )

        # Add the regression force column directly after the force column
        self.processed_data_frame.regression_force = pd.Series(
            [
                self.y(t, self.a, self.b, self.tau)  # type: ignore
                for t in self.processed_data_frame.relative_time  # type: ignore
            ]
        )

    @staticmethod
    def y(t: float, a: float, b: float, tau: float) -> float:
        """
        Calculates the value of following equation:
        y = a * e^(-t / tau) + b

        Args:
            t: Time at which the function is to be computed.
            a: Amplitude of the exponential decay.
            b: Baseline value of the function.
            tau: Time constant of the exponential decay.

        Returns:
            Value of the function at time t.
        """

        return a * np.exp(-t / tau) + b


class FailureData(ProcessedData):
    """
    Data storage class for the compression to failure test.  A column containing
    the toughness is also calculated and added to the data.

    Args:
        raw_data_frame: The raw data frame which will be used to create the
            processed data.
    """

    def __init__(self, raw_data_frame: DataFrame) -> None:

        super().__init__(raw_data_frame, "Toughness")

        self._abort_strain_pct: float = 0.0
        self._stiffness_strain_pct: float = 0.0
        self._toughness_strain_pct: float = 0.0
        self._yield_strain_pct: float = 0.0

    @property
    def aborted(self) -> bool:
        return self.ultimate_strain_pct >= self._abort_strain_pct

    @property
    def processed_data_frame(self) -> FailureDataFrame:
        return super().processed_data_frame  # type: ignore

    @processed_data_frame.setter
    def processed_data_frame(self, value: FailureDataFrame) -> None:  # type: ignore
        super(FailureData, FailureData).processed_data_frame.__set__(self, value)  # type: ignore

    @property
    def slipped(self) -> bool:
        return False  # TODO: implement

    @property
    def stiffness_MPa(self) -> float:
        return self.processed_data_frame.stress.loc[
            (self.processed_data_frame.strain - self._stiffness_strain_pct)
            .abs()
            .idxmin()  # type: ignore
        ]

    @property
    def stiffness_strain_pct(self) -> float:
        return self._stiffness_strain_pct

    @property
    def toughness_MPa(self) -> float:
        return self.processed_data_frame.toughness.loc[
            (self.processed_data_frame.strain - self._toughness_strain_pct)
            .abs()
            .idxmin()  # type: ignore
        ]

    @property
    def toughness_strain_pct(self) -> float:
        return self._toughness_strain_pct

    @property
    def ultimate_force_N(self) -> float:
        return self.processed_data_frame.force.loc[
            self.processed_data_frame.stress.idxmax()  # type: ignore
        ]

    @property
    def ultimate_strain_pct(self) -> float:
        return self.processed_data_frame.strain.loc[
            self.processed_data_frame.stress.idxmax()  # type: ignore
        ]

    @property
    def ultimate_strength_MPa(self) -> float:
        return self.processed_data_frame.stress.max()  # type: ignore

    @property
    def yield_force_N(self) -> float:
        return self.processed_data_frame.force.loc[
            (self.processed_data_frame.strain - self._yield_strain_pct)
            .abs()
            .idxmin()  # type: ignore
        ]

    @property
    def yield_strain_pct(self) -> float:
        return self._yield_strain_pct

    @property
    def yield_strength_MPa(self) -> float:
        return self.processed_data_frame.stress.loc[
            (self.processed_data_frame.strain - self._yield_strain_pct)
            .abs()
            .idxmin()  # type: ignore
        ]

    def process_raw_data(  # type: ignore
        self,
        abort_strain_pct: float,
        toughness_strain_pct: float,
        stiffness_strain_pct: float,
    ) -> None:
        """
        Processes the raw data read from the CSV output of the Instron.

        Dataset filtering:
            -

        Columns that are populated:
            - Toughness: The area under the stress-strain curve up until each
                data point.

        Summary parameters that are calculated:
            -


        Args:
            abort_strain_pct: The strain threshold at which the test is
                considered to be aborted.
            toughness_strain_pct: The strain at which the toughness is
                calculated.
            stiffness_strain_pct: The strain at which the stiffness is
                calculated.
        """

        self._abort_strain_pct = abort_strain_pct
        self._toughness_strain_pct = toughness_strain_pct
        self._stiffness_strain_pct = stiffness_strain_pct

        self.processed_data_frame = FailureDataFrame(self.raw_data_frame.frame)

        # Add the toughness column
        # NOTE: np.insert is required because the output of
        #       cumulative_trapezoid() is an array one less than the length of
        #       the data frame
        self.processed_data_frame.toughness = pd.Series(  # type: ignore
            np.insert(
                cumulative_trapezoid(
                    self.processed_data_frame.stress, self.processed_data_frame.strain
                ),
                0,
                0,
            )
        )


class Summary:
    """
    Base class for all summaries.
    """

    def __init__(self) -> None:

        self.summary_frame: SummaryFrame
        self.sheet_name: str = "Summary"

    def __str__(self) -> str:
        return str(self.summary_frame.frame)

    def clear_all_rows(self) -> None:
        self.summary_frame.frame.drop(self.summary_frame.frame.index, inplace=True)  # type: ignore

    def write_to_excel(self, writer: pd.ExcelWriter) -> None:
        self.summary_frame.frame.to_excel(  # type: ignore
            writer,
            sheet_name=self.sheet_name,
            index=False,
        )


class RelaxationSummary(Summary):
    """
    Data storage class for the summary of the relaxation test.
    """

    def __init__(self) -> None:

        super().__init__()

        self.summary_frame: RelaxationSummaryFrame = RelaxationSummaryFrame()  # type: ignore

    def append_row(
        self,
        strain_pct: float,
        min_force_N: float,
        max_force_N: float,
        min_stress_MPa: float,
        max_stress_MPa: float,
        min_e_modulus_MPa: float,
        max_e_modulus_MPa: float,
        a: float,
        b: float,
        tau: float,
    ) -> None:
        """
        Append a row to the summary frame.

        Args:
            strain_pct: The relaxation strain.
            min_force_N: The minimum force during relaxation.
            max_force_N: The maximum force during relaxation.
            min_stress_MPa: The minimum stress during relaxation.
            max_stress_MPa: The maximum stress during relaxation.
            min_e_modulus_MPa: The minimum E-modulus during relaxation.
            max_e_modulus_MPa: The maximum E-modulus during relaxation.
            a: The exponential decay equation coefficient a
                (y = a * e^(-t / tau) + b)
            b: The exponential decay equation coefficient b
                (y = a * e^(-t / tau) + b)
            tau: The exponential decay equation coefficient tau
                (y = a * e^(-t / tau) + b)
        """

        self.summary_frame.append_row(
            strain_pct,
            min_force_N,
            max_force_N,
            min_stress_MPa,
            max_stress_MPa,
            min_e_modulus_MPa,
            max_e_modulus_MPa,
            a,
            b,
            tau,
        )


class FailureSummary(Summary):
    """
    Data storage class for the summary of the compression to failure test.
    """

    def __init__(self) -> None:

        super().__init__()

        self.summary_frame: FailureSummaryFrame = FailureSummaryFrame()  # type: ignore

    def append_row(
        self,
        ultimate_strain_pct: float,
        ultimate_force_N: float,
        ultimate_strength_MPa: float,
        aborted: float,
        slipped: float,
        yield_strain_pct: float,
        yield_force_N: float,
        yield_strength_MPa: float,
        toughness_strain_pct: float,
        toughness_MPa: float,
        stiffness_strain_pct: float,
        stiffness_MPa: float,
    ) -> None:
        """
        Append a row to the summary frame.

        Args:
            ultimate_strain_pct: The strain at which the sample broke or the
                test was aborted.
            ultimate_force_N: The force at which the sample broke or the test
                was aborted.
            ultimate_strength_MPa: The stress at which the sample broke or the
                test was aborted.
            aborted: Flag indicating whether the test was aborted or if the
                sample broke.  This flag is used to interpret the meaning of the
                ultimate values.
            slipped: Flag indicating whether the sample slipped during the test.
                Slipped is defined as it partially breaking before continuing
                on the achieve a greater ultimate strength.
            yield_strain_pct: The strain at which the sample deformation changes
                from elastic to plastic.
            yield_force_N: The force at which the sample deformation changes
                from elastic to plastic.
            yield_strength_MPa: The stress at which the sample deformation
                changes from elastic to plastic.
            toughness_strain_pct: The strain at which the toughness was
                calculated.
            toughness_MPa: The toughness of the sample, which is defined as the
                area under the stress-strain curve up until a specified strain.
            stiffness_strain_pct: The strain at which the stiffness was
                calculated.
            stiffness_MPa: The stiffness of the sample, which is defined as the
                stress at a specified strain.
        """

        self.summary_frame.append_row(
            ultimate_strain_pct,
            ultimate_force_N,
            ultimate_strength_MPa,
            aborted,
            slipped,
            yield_strain_pct,
            yield_force_N,
            yield_strength_MPa,
            toughness_strain_pct,
            toughness_MPa,
            stiffness_strain_pct,
            stiffness_MPa,
        )
