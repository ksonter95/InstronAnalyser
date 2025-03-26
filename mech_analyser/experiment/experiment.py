import argparse
import dataclasses
import pandas as pd

from PySide6.QtWidgets import QStackedWidget, QWidget
from pathlib import Path
from typing import Optional, Protocol

# === Data frames ============================================================ #


class Frame:
    """
    Base class for all data frames.

    Args:
        frame: Underlying pd.DataFrame representation of the data.
        sheet_name: The name of the Excel sheet to which the data will be
            written.
    """

    def __init__(self, frame: pd.DataFrame, sheet_name: str) -> None:

        self._frame: pd.DataFrame = frame.copy(deep=True)
        self._frame.reset_index(drop=True, inplace=True)

        self.sheet_name: str = sheet_name

    @property
    def columns(self) -> list[str]:
        return [i for i in self._frame.columns]

    @property
    def frame(self) -> pd.DataFrame:
        return self._frame

    def write_to_excel(self, writer: pd.ExcelWriter) -> None:
        """
        Writes the underlying pd.DataFrame representation of the data frame to
        and Excel file.

        Args:
            writer: Excel writer used to write the data frame to an Excel file.
        """

        self._frame.to_excel(writer, sheet_name=self.sheet_name, index=False)  # type: ignore

        # Autofit the column size
        writer.sheets[self.sheet_name].autofit()


class RawFrame(Frame):
    """
    Base class for all raw data frames.

    Args:
        frame: Underlying pd.DataFrame representation of the data.
    """

    def __init__(self, frame: pd.DataFrame) -> None:
        super().__init__(frame, "Raw Data")

    @classmethod
    def load(cls, csv: Path) -> "Frame":
        """
        Loads the CSV file into a frame and validates its contents.

        NOTE: this is an abstract method that will be overwritten in the child
              classes.

        Args:
            csv: The path to the CSV file containing the output.
        """

        raise NotImplementedError


class ProcessedFrame(Frame):
    """
    Base class for all processed data frames.

    Args:
        frame: Underlying pd.DataFrame representation of the data.
        sheet_name: The name of the Excel sheet to which the data will be
            written.
    """

    pass


# === Parameters ============================================================= #


@dataclasses.dataclass
class DataParameters:
    """
    Base class for all data parameters.
    """

    pass


@dataclasses.dataclass
class AnalyserParameters:
    """
    Base class for all analyser parameters.
    """

    pass


# === Data =================================================================== #


class Data:
    """
    Base class for all data.

    Args:
        raw_frame: The raw data frame from which the processed data frame is
            created.
        processed_frame: The processed data frame.
    """

    def __init__(self, raw_frame: RawFrame, processed_frame: ProcessedFrame) -> None:

        self._raw_frame: RawFrame = raw_frame
        self._processed_frame: ProcessedFrame

        self.processed_frame = processed_frame

    @property
    def processed_frame(self) -> ProcessedFrame:
        return self._processed_frame

    @processed_frame.setter
    def processed_frame(self, value: ProcessedFrame) -> None:
        self._processed_frame = value

    @property
    def raw_frame(self) -> RawFrame:
        return self._raw_frame

    def process(self, parameters: DataParameters) -> None:
        """
        Processes the raw data frame.  This could include populating additional
        columns or calculating summary parameters of the dataset.

        NOTE: this is an abstract method that will be overwritten in the child
              classes.

        Args:
            parameters: The parameters to use when processing the data.
        """

        raise NotImplementedError


# === Results ================================================================ #


class Summary:
    """
    Base class for all summaries.

    Args:
        frame: Underlying pd.DataFrame representation of the summary.
    """

    def __init__(self, frame: pd.DataFrame) -> None:

        self._frame: pd.DataFrame = frame.copy(deep=True)
        self._frame.reset_index(drop=True, inplace=True)

    @property
    def collate_vertical(self) -> bool:
        return len(self._frame) == 1

    @property
    def frame(self) -> pd.DataFrame:
        return self._frame

    def append_row(self, data: Data, parameters: DataParameters) -> None:
        """
        Append a row to the summary frame.

        Args:
            data: The data to append.
            parameters: The parameters used when processing the data.

        NOTE: this is an abstract method that will be overwritten in the child
              classes.
        """

        raise NotImplementedError

    def clear_all_rows(self) -> None:
        """
        Clears all rows in the underlying pd.DataFrame representation of the
        summary.
        """

        self._frame.drop(self._frame.index, inplace=True)  # type: ignore

    def write_to_excel(self, writer: pd.ExcelWriter) -> None:
        """
        Writes the underlying pd.DataFrame representation of the summary to an
        Excel file.

        Args:
            writer: Excel writer used to write the summary to an Excel file.
        """

        self._frame.to_excel(writer, sheet_name="Summary", index=False)  # type: ignore

        # Autofit the column size
        writer.sheets["Summary"].autofit()


# === Collations ============================================================= #


class Collation:
    """
    Base class for all collations.

    Args:
        sheet_name: The name of the Excel sheet to which the data will be
            written.
    """

    def __init__(self, sheet_name: str) -> None:

        self._frame: pd.DataFrame = pd.DataFrame()

        self.sheet_name: str = sheet_name

    @property
    def frame(self) -> pd.DataFrame:
        return self._frame

    def write_to_excel(self, writer: pd.ExcelWriter) -> None:
        """
        Writes the underlying pd.DataFrame representation of the collations to
        an Excel file.

        Args:
            writer: Excel writer used to write the collations to an Excel file.
        """

        # NOTE: Header and data written separately to avoid blank row between
        #       them
        self._frame.drop(self.frame.index).to_excel(  # type: ignore
            writer, sheet_name=self.sheet_name
        )
        self._frame.to_excel(  # type: ignore
            writer, startrow=1, header=False, sheet_name=self.sheet_name
        )

        # Autofit the column size
        writer.sheets[self.sheet_name].autofit()


class RawCollation(Collation):
    """
    Base class of all raw data frame collations.

    Args:
        - columns: The columns from the raw data frame to collate.
    """

    def __init__(self, columns: list[str]) -> None:
        super().__init__("Raw Data")

        self._columns: list[str] = columns

    def append(self, raw_frame: RawFrame, sample_name: str) -> None:
        """
        Appends the raw data frame to the collated raw data frame.

        Args:
            raw_frame: The raw data frame to append.
            sample_name: The name of the sample to which the raw data applies.
        """

        subset_frame: pd.DataFrame = raw_frame.frame[self._columns].copy()
        subset_frame.columns = pd.MultiIndex.from_tuples(  # type: ignore
            [(sample_name, c) for c in subset_frame.columns]
        )
        self._frame = pd.concat([self._frame, subset_frame], axis=1)


class SummaryCollation(Collation):
    """
    Base class of all summary collations.
    """

    def append(self, summary: Summary, sample_name: str) -> None:
        """
        Appends the summary to the collated summary.

        Args:
            summary: The summary to append.
            sample_name: The name of the sample to which the summary applies.
        """

        if summary.collate_vertical:
            self._append_vertical(summary, sample_name)
        else:
            self._append_horizontal(summary, sample_name)

    def _append_horizontal(self, summary: Summary, sample_name: str) -> None:
        """
        Appends the summary to the collated summary by horizontally
        concatenating the summary.

        Args:
            summary: The summary to append.
            sample_name: The name of the sample to which the summary applies.
        """

        subset_frame: pd.DataFrame = summary.frame.copy()
        subset_frame.columns = pd.MultiIndex.from_tuples(  # type: ignore
            [(sample_name, c) for c in subset_frame.columns]
        )
        self._frame = pd.concat([self._frame, subset_frame], axis=1)

    def _append_vertical(self, summary: Summary, sample_name: str) -> None:
        """
        Appends the summary to the collated summary by vertically concatenating
        the summary.

        Args:
            summary: The summary to append.
            sample_name: The name of the sample to which the summary applies.
        """

        subset_frame: pd.DataFrame = summary.frame.copy()
        subset_frame.insert(0, "Sample", sample_name)  # type: ignore
        self._frame = pd.concat([self._frame, subset_frame], ignore_index=True)


class Collator:
    """
    Base class for all collators.

    Args:
        output_xlsx: The path to the Excel file which will contain the collation
            of all raw data and summaries.
        raw_collation: The raw data frame collation.
        summary_collations: The list of all summary collations.
    """

    def __init__(
        self,
        output_xlsx: Path,
        raw_collation: RawCollation,
        summary_collations: list[SummaryCollation],
    ) -> None:

        self._output_xlsx: Path = output_xlsx
        self._raw_collation: RawCollation = raw_collation
        self._summary_collations: list[SummaryCollation] = summary_collations

    @property
    def output_xlsx(self) -> Path:
        return self._output_xlsx

    @property
    def raw_collation(self) -> RawCollation:
        return self._raw_collation

    @property
    def summary_collations(self) -> list[SummaryCollation]:
        return self._summary_collations

    def save(self) -> None:
        """
        Saves the collation to an Excel file.  This includes the raw data and
        all summaries.
        """

        with pd.ExcelWriter(self._output_xlsx, engine="xlsxwriter") as writer:
            self._raw_collation.write_to_excel(writer)
            for s in self._summary_collations:
                s.write_to_excel(writer)


# === Analysers ============================================================== #


class Analyser:
    """
    Base class for all analysers.

    Args:
        output_xlsx: The path to the Excel file which will contain the analysis
            results.
        raw_frame: The raw experiment data frame.
        parameters: The parameters to use when analysing the experiment.
        summary: The summary of the analysis.
    """

    def __init__(
        self,
        output_xlsx: Path,
        raw_frame: RawFrame,
        parameters: AnalyserParameters,
        summary: Summary,
    ) -> None:

        self._data: list[Data] = []
        self._output_xlsx: Path
        self._parameters: AnalyserParameters = parameters
        self._raw_frame: RawFrame = raw_frame
        self._summary: Summary = summary

        self.output_xlsx = output_xlsx

    @property
    def data(self) -> list[Data]:
        return self._data

    @property
    def output_xlsx(self) -> Path:
        return self._output_xlsx

    @output_xlsx.setter
    def output_xlsx(self, value: Path) -> None:
        self._output_xlsx = value

    @property
    def parameters(self) -> AnalyserParameters:
        return self._parameters

    @property
    def raw_frame(self) -> RawFrame:
        return self._raw_frame

    @property
    def summary(self) -> Summary:
        return self._summary

    def analyse(self) -> None:
        """
        Analyses the output of the experiment.

        NOTE: this is an abstract method that will be overwritten in the child
              classes.
        """

        raise NotImplementedError

    def save(self) -> None:
        """
        Saves the analysis to an Excel file.  This includes the raw data,
        analysis summary, and all processed data.
        """

        with pd.ExcelWriter(self.output_xlsx, engine="xlsxwriter") as writer:
            self._raw_frame.write_to_excel(writer)
            self._summary.write_to_excel(writer)
            for d in self._data:
                d.processed_frame.write_to_excel(writer)


# === Command-line parsers =================================================== #


class ArgparseTypes:
    """
    Class containing all the custom argparse types.
    """

    @staticmethod
    def csv_file(value: str) -> Path:
        """
        Checks the argument to determine if it is a path to an existing CSV
        file.

        Args:
            value: The path to the CSV which is to be checked.

        Raises:
            argparse.ArgumentTypeError: If the path is not a CSV file.

        Returns:
            Path: The path to the CSV file if it exists.
        """

        if not Path(value).exists() or Path(value).suffix != ".csv":
            raise argparse.ArgumentTypeError(f"'{value}' is not an existing CSV file")

        return Path(value)

    @staticmethod
    def directory(value: str) -> Path:
        """
        Checks the argument to determine if it is a path to an existing
        directory.

        Args:
            value: The path to the directory which is to be checked.

        Raises:
            argparse.ArgumentTypeError: If the path is not a directory.

        Returns:
            Path: The path to the directory if it exists.
        """

        if not Path(value).is_dir():
            raise argparse.ArgumentTypeError(f"Directory '{value}' does not exist")

        return Path(value)

    @staticmethod
    def percentage_float(value: str) -> float:
        """
        Checks the argument to determine if it is a percentage float (i.e. it
        can contain the values 0~100).

        Args:
            value: The number which is to be checked.

        Raises:
            argparse.ArgumentTypeError: If the number is not a percentage float.

        Returns:
            float: The number if it is valid.
        """

        try:
            float_value = float(value)
            if float_value < 0 or float_value > 100:
                raise ValueError
        except ValueError:
            raise argparse.ArgumentTypeError(f"'{value}' is not >=0 and <=100")

        return float(value)

    @staticmethod
    def poisson_float(value: str) -> float:
        """
        Checks the argument to determine if it is a Poisson's float
        (0 <= value <= 0.5).

        Args:
            value: The number which is to be checked.

        Raises:
            argparse.ArgumentTypeError: If the number is not a Poisson's float.

        Returns:
            float: The number if it is valid.
        """

        try:
            float_value = float(value)
            if float_value < 0 or float_value > 0.5:
                raise ValueError
        except ValueError:
            raise argparse.ArgumentTypeError(f"'{value}' is not a Poisson's float")

        return float(value)

    @staticmethod
    def positive_integer(value: str) -> int:
        """
        Checks the argument to determine if it is a positive integer.

        Args:
            value: The number which is to be checked.

        Raises:
            argparse.ArgumentTypeError: If the number is not a positive integer.

        Returns:
            float: The number if it is valid.
        """

        try:
            integer_value = int(value)
            if integer_value < 0:
                raise ValueError
        except ValueError:
            raise argparse.ArgumentTypeError(f"'{value}' is not a positive integer")

        return int(value)

    @staticmethod
    def positive_non_zero_float(value: str) -> float:
        """
        Checks the argument to determine if it is a non-zero positive float.

        Args:
            value: The number which is to be checked.

        Raises:
            argparse.ArgumentTypeError: If the number is not a non-zero positive
                float.

        Returns:
            float: The number if it is valid.
        """

        try:
            float_value = float(value)
            if float_value <= 0:
                raise ValueError
        except ValueError:
            raise argparse.ArgumentTypeError(
                f"'{value}' is not a positive non-zero float"
            )

        return float(value)

    @staticmethod
    def positive_non_zero_integer(value: str) -> int:
        """
        Checks the argument to determine if it is a non-zero positive integer.

        Args:
            value: The number which is to be checked.

        Raises:
            argparse.ArgumentTypeError: If the number is not a non-zero positive
                integer.

        Returns:
            float: The number if it is valid.
        """

        try:
            integer_value = int(value)
            if integer_value <= 0:
                raise ValueError
        except ValueError:
            raise argparse.ArgumentTypeError(
                f"'{value}' is not a positive non-zero integer"
            )

        return int(value)


class Parser:
    """
    Base class for all command-line parsers.

    Args:
        parsed_arguments: The parsed command-line arguments.
    """

    def __init__(self, parsed_arguments: argparse.Namespace) -> None:

        input_csv: Optional[Path] = parsed_arguments.csv
        input_directory: Optional[Path] = parsed_arguments.directory
        output_directory: Optional[Path] = parsed_arguments.output_directory

        self._files: list[tuple[Path, Path]] = []
        if input_csv is not None:
            self._files.append(
                (input_csv, self._create_output_xlsx(input_csv, output_directory))
            )

        elif input_directory is not None:
            for input_csv in input_directory.iterdir():
                if not input_csv.is_file() or not input_csv.suffix == ".csv":
                    continue

                self._files.append(
                    (input_csv, self._create_output_xlsx(input_csv, output_directory))
                )

    def create_analysers(self) -> list[Analyser]:
        """
        Creates the experiment analysers from the parsed command-line arguments.

        Returns:
            list[Analyser]: List of all compression-to-failure Instron 68TM
                experiment analysers.
        """

        raise NotImplementedError

    def _create_output_xlsx(
        self, input_csv: Path, output_directory: Optional[Path]
    ) -> Path:
        """
        Creates the Excel output file path from the CSV input file path.

        Args:
            input_csv: Path to the CSV input file.
            output_directory: Path to the directory in which the Excel output file should
                be located.

        Returns:
            Path: Path to the Excel output file.
        """

        output_xlsx: Path = input_csv.with_suffix(".xlsx")
        if output_directory is not None:
            output_xlsx = output_directory / output_xlsx.name

        return output_xlsx

    @staticmethod
    def create_parser() -> argparse.ArgumentParser:
        """
        Creates the command-line parser.

        Returns:
            argparse.ArgumentParser: Created command-line parser.
        """

        parser = argparse.ArgumentParser(
            "Mechanical Analyser",
            description="Analyses the data output from a mechanical instrument",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )
        group: argparse._MutuallyExclusiveGroup = (  # type: ignore
            parser.add_mutually_exclusive_group(required=True)
        )
        group.add_argument(
            "-c",
            "--csv",
            help="Path to the CSV file",
            type=ArgparseTypes.csv_file,
        )
        group.add_argument(
            "-d",
            "--directory",
            help="Path to the directory of CSV files",
            type=ArgparseTypes.directory,
        )
        parser.add_argument(
            "-o",
            "--output-directory",
            help="Path to the directory into which the generated CSV files "
            "will be saved",
            type=ArgparseTypes.directory,
        )

        return parser

    @staticmethod
    def create_subparser(  # type: ignore
        parser: argparse.ArgumentParser,
    ) -> argparse._SubParsersAction:  # type: ignore
        """
        Creates the instrument subparser.

        Args:
            parser: Command-line parser to which the instrument subparser is to
                be added.

        Returns:
            argparse._SubParsersAction: Created instrument subparser.
        """

        return parser.add_subparsers(
            dest="instrument",
            required=True,
            help="Mechanical instrument to which the data belongs",
        )


# === User Interface Widgets ================================================= #


class ViewBase(Protocol):
    """
    Structural subtype base class for generated user interface widgets.
    """

    def setupUi(self, parent: QWidget) -> None: ...
    def retranslateUi(self, parent: QWidget) -> None: ...


class Widget(QWidget):
    """
    Base class for all user interface widgets.

    Args:
        view: Generated user interface widget.
        parameters: The parameters to use when analysing the experiment.
    """

    def __init__(self, view: ViewBase, parameters: AnalyserParameters) -> None:
        super().__init__()

        self._parameters: AnalyserParameters = parameters
        self._view: ViewBase = view

        self.view.setupUi(self)

    @property
    def columns(self) -> list[str]:
        raise NotImplementedError

    @property
    def experiment(self) -> str:
        raise NotImplementedError

    @property
    def instrument(self) -> str:
        raise NotImplementedError

    @property
    def parameters(self) -> AnalyserParameters:
        return self._parameters

    @property
    def view(self) -> ViewBase:
        return self._view

    def activate(self, configuration_viewer: QStackedWidget) -> None:
        """
        Activates and displays the widget within the configuration viewer.

        Args:
            configuration_viewer: The configuration viewer in which to display
                the widget.
        """

        configuration_viewer.setCurrentWidget(self)

    def create_analyser(
        self, input_csv: Path, output_xlsx: Path, parameters: AnalyserParameters
    ) -> Analyser:
        """
        Creates the experiment analyser.

        Args:
            input_csv: The path to the CSV file containing the output of the
                experiment.
            output_xlsx: The path to the Excel file which will contain the
                analysis results.
            parameters: The parameters to use when analysing the experiment.
        """

        raise NotImplementedError

    def init(self) -> None:
        """
        Initialises the widget by setting the input fields to the defaults of
        the parameters to use when analysing the experiment and connecting any
        signals with an associated slot.

        NOTE: this is an abstract method that will be overwritten in the child
              classes.
        """

        raise NotImplementedError

    def sync_parameters(self) -> None:
        """
        Synchronise the parameters to use when analysing the experiment with the
        widget input fields.

        NOTE: this is an abstract method that will be overwritten in the child
              classes.
        """

        raise NotImplementedError
