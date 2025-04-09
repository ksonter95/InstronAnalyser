import dataclasses
import pandas as pd

from PySide6.QtWidgets import QStackedWidget, QWidget
from pathlib import Path
from typing import Any, Protocol

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
    def load(cls, csv: Path, **kwargs: dict[str, Any]) -> "Frame":
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

        # First column is shared across all summaries
        if self._frame.empty:
            self._frame = (
                summary.frame.iloc[:, [0]]
                .copy()
                .set_axis(  # type: ignore
                    pd.MultiIndex.from_tuples([(summary.frame.columns[0], "")]),  # type: ignore
                    axis=1,
                )
            )

        # Append the summaries, skipping the first column
        subset_frame: pd.DataFrame = summary.frame.iloc[:, 1:].copy()
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
    """

    def __init__(self, view: ViewBase) -> None:
        super().__init__()

        self._view: ViewBase = view

        self.view.setupUi(self)

    @property
    def view(self) -> ViewBase:
        return self._view

    def activate(self, viewer: QStackedWidget) -> None:
        """
        Activates and displays the widget within the viewer.

        Args:
            viewer: The viewer in which to display the widget.
        """

        viewer.setCurrentWidget(self)


class ConfigWidget(Widget):
    """
    Base class for all user interface configuration widgets.

    Args:
        view: Generated user interface configuration widget.
        parameters: The parameters to use when analysing the experiment.
    """

    def __init__(self, view: ViewBase, parameters: AnalyserParameters) -> None:
        super().__init__(view)

        self._parameters: AnalyserParameters = parameters

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
