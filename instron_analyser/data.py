import numpy as np
import pandas as pd
import warnings

from pathlib import Path
from scipy.optimize import curve_fit  # type: ignore
from typing import Any, Optional


class DataFrame(pd.DataFrame):
    """
    Wrapper for pd.DataFrame that allows the class to be interacted with like a
    standard pd.DataFrame.

    Args:
        data_frame: pd.DataFrame to wrap.
    """

    def __init__(self, data_frame: pd.DataFrame) -> None:

        self._data_frame: pd.DataFrame = data_frame.copy(deep=True)
        self._data_frame.reset_index(drop=True, inplace=True)

    def __getattr__(self, attribute: str) -> Any:
        return getattr(self._data_frame, attribute)

    def __setattr__(self, name: str, value: Any) -> None:
        if name == "_data_frame":
            object.__setattr__(self, name, value)  # prevent recursion
        else:
            setattr(self._data_frame, name, value)

    def __getitem__(self, key: Any) -> Any:
        return self._data_frame[key]  # type: ignore

    def __setitem__(self, key: Any, value: Any) -> None:
        self._data_frame[key] = value

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
    def initial_time_s(self) -> float:
        return self.time[0]

    @property
    def strain(self) -> "pd.Series[float]":
        return self._data_frame["Strain (%)"]  # type: ignore

    @property
    def stress(self) -> "pd.Series[float]":
        return self._data_frame["Compressive Stress (MPa)"]  # type: ignore

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
        self.relative_time = pd.Series([0.0] * self.index.size)  # type: ignore
        self.regression_force = pd.Series([0] * self.index.size)  # type: ignore

    def __setattr__(self, name: str, value: Any) -> None:
        if name in ["regression_force", "relative_time"]:
            object.__setattr__(self, name, value)
        else:
            super().__setattr__(name, value)

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

        self.raw_data_frame: DataFrame = raw_data_frame
        self.processed_data_frame: DataFrame = self.raw_data_frame
        self.sheet_name: str = sheet_name

    def __str__(self) -> str:
        return str(self.processed_data_frame)

    def write_to_excel(self, writer: pd.ExcelWriter) -> None:
        self.processed_data_frame.to_excel(  # type: ignore
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

    def __init__(
        self,
        raw_data_frame: DataFrame,
    ) -> None:

        super().__init__(raw_data_frame, "Strain = ?%")

        # Regression equation parameters for equation y = a * e^(-t / tau) + b
        self.a: float = 0.0
        self.b: float = 0.0
        self.tau: float = 1.0

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
            self.raw_data_frame[
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
                or self.processed_data_frame.index.size  # type: ignore
            ),
            self.processed_data_frame.force.head(  # type: ignore
                regression_data_points
                or self.processed_data_frame.index.size  # type: ignore
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
