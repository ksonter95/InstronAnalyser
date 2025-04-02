import argparse
import experiment.experiment as experiment
import pandas as pd
import re

from pathlib import Path


# === Data frames ============================================================ #


class Frame:
    """
    Base class for all MicroTester G2 data frames.
    """

    @property
    def base_displacement(self) -> "pd.Series[float]":
        return self._frame["Base Displacement [um]"]  # type: ignore

    @property
    def current_size(self) -> "pd.Series[float]":
        return self._frame["Current Size [um]"]  # type: ignore

    @property
    def cycle(self) -> "pd.Series[str]":
        return self._frame["Cycle"]  # type: ignore

    @property
    def force(self) -> "pd.Series[float]":
        return self._frame["Force [uN]"]  # type: ignore

    @property
    def name(self) -> "pd.Series[str]":
        return self._frame["Set Name"]  # type: ignore

    @property
    def temperature(self) -> "pd.Series[float]":
        return self._frame["Temperature [°C]"]  # type: ignore

    @property
    def time(self) -> "pd.Series[int]":
        return self._frame["Time [ms]"]  # type: ignore

    @property
    def tip_displacement(self) -> "pd.Series[float]":
        return self._frame["Tip Displacement [um]"]  # type: ignore


class RawFrame(experiment.RawFrame, Frame):
    """
    Raw output of a MicroTester G2 experiment.

    Args:
        frame: Underlying pd.DataFrame representation of the data.
    """

    @classmethod
    def load(cls, csv: Path) -> "RawFrame":  # type: ignore
        """
        Loads the CSV file into a frame and validates its contents.

        Args:
            csv: The path to the CSV file containing the MicroTester G2 output.
        """

        try:
            # Read the CSV file
            frame: pd.DataFrame = pd.read_csv(csv, header=0, encoding="cp1252")  # type: ignore
            # NOTE: add a space between parameter and units
            frame.columns = [" (".join(c.split("(")) for c in frame.columns]
            # NOTE: remove excess spaces
            frame.columns = [re.sub(r"\s+", " ", c) for c in frame.columns]
            # NOTE: replace parenthesis with square brackets
            frame.columns = [
                c.translate(str.maketrans("()", "[]")) for c in frame.columns
            ]

            # Validate the CSV file
            #  - Data headings must be in row 0, columns 0-7 (0-indexed) and
            #    must be:
            #       Set Name, Cycle, Time(ms), Force(uN),Tip Displacement(um),
            #       Base Displacement(um),Current Size (um), Temperature (°C)
            #  - Data must be in rows 1-... (0-indexed) and must be all strings
            #    for columns 0-1, integers for columns 2, and floating point
            #    numbers for columns 3-7 (0-indexed)
            headings: list[str] = [
                "Set Name",
                "Cycle",
                "Time [ms]",
                "Force [uN]",
                "Tip Displacement [um]",
                "Base Displacement [um]",
                "Current Size [um]",
                "Temperature [°C]",
            ]
            if (
                frame.columns.tolist() != headings
                # NOTE: further checking could be done here
                or not frame.notna().all().all()  # type: ignore
            ):
                raise ValueError

        except:
            raise ValueError(f"Invalid CSV file: {csv}")

        return RawFrame(frame)


class ProcessedFrame(experiment.ProcessedFrame, Frame):
    """
    Base class for all processed outputs of a MicroTester G2 experiment.
    Args:
        frame: Underlying pd.DataFrame representation of the data.
        sheet_name: The name of the Excel sheet to which the data will be
            written.
    """

    pass


# === Parameters ============================================================= #


# === Data =================================================================== #


class Data(experiment.Data):
    """
    Base class for all data of a MicroTester G2 experiment.

    Args:
        raw_frame: The raw data frame from which the processed data frame is
            created.
        processed_frame: The processed data frame.
    """

    def __init__(self, raw_frame: RawFrame, processed_frame: ProcessedFrame) -> None:

        super().__init__(raw_frame, processed_frame)

    @property
    def processed_frame(self) -> ProcessedFrame:
        return super().processed_frame  # type: ignore

    @processed_frame.setter
    def processed_frame(self, value: ProcessedFrame) -> None:  # type: ignore
        super(Data, Data).processed_frame.__set__(self, value)  # type: ignore

    @property
    def raw_frame(self) -> RawFrame:
        return super().raw_frame  # type: ignore


# === Results ================================================================ #


class Summary(experiment.Summary):
    """
    Base class for all MicroTester G2 summaries.

    Args:
        frame: Underlying pd.DataFrame representation of the summary.
    """

    pass


# === Analysers ============================================================== #


class Analyser(experiment.Analyser):
    """
    Base class for all MicroTester G2 analysers.

    Args:
        input_csv: The path to the CSV file containing the output of the
            MicroTester G2 experiment.
        output_xlsx: The path to the Excel file which will contain the analysis
            results.
        parameters: The parameters to use when analysing the MicroTester G2
            experiment.
        summary: The summary of the analysis.
    """

    def __init__(
        self,
        input_csv: Path,
        output_xlsx: Path,
        parameters: experiment.AnalyserParameters,
        summary: Summary,
    ) -> None:

        super().__init__(
            output_xlsx,
            RawFrame.load(input_csv),
            parameters,
            summary,
        )

    @property
    def data(self) -> list[Data]:  # type: ignore
        return super().data  # type: ignore

    @property
    def raw_frame(self) -> RawFrame:
        return super().raw_frame  # type: ignore

    @property
    def summary(self) -> Summary:
        return super().summary  # type: ignore


# === Command-line parsers =================================================== #


class Parser(experiment.Parser):
    """
    Base class for all MicroTester G2 command-line parsers.

    Args:
        parsed_arguments: The parsed command-line arguments.
    """

    def __init__(self, parsed_arguments: argparse.Namespace) -> None:

        super().__init__(parsed_arguments)

    @staticmethod
    def add_parser(  # type: ignore
        subparser: argparse._SubParsersAction,  # type: ignore
    ) -> argparse.ArgumentParser:
        """
        Adds the MicroTester G2 command-line parser to the instrument subparser.

        Args:
            subparser: The instrument subparser to which to add the MicroTester
                G2 parser.

        Returns:
            argparse.ArgumentParser: Created MicroTester G2 command-line parser.
        """

        parser: argparse.ArgumentParser = subparser.add_parser(  # type: ignore
            Path(__file__).parent.name,
            description="Analyses the data from a MicroTester G2",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )

        return parser  # type: ignore

    @staticmethod
    def create_subparser(  # type: ignore
        parser: argparse.ArgumentParser,
    ) -> argparse._SubParsersAction:  # type: ignore
        """
        Creates the MicroTester G2 experiment subparser.

        Args:
            parser: MicroTester G2 parser to which the experiment subparser is
                to be added.

        Returns:
            argparse._SubParsersAction: Created experiment subparser.
        """

        return parser.add_subparsers(
            dest="experiment",
            required=True,
            help="MicroTester G2 experiment for which the data is to be analysed",
        )


# === User Interface Widgets ================================================= #


class Widget(experiment.Widget):
    """
    Base class for all MicroTester G2 user interface widgets.

    Args:
        view: Generated user interface widget.
        parameters: The parameters to use when analysing the experiment.
    """

    @property
    def columns(self) -> list[str]:
        return [
            "Set Name",
            "Cycle",
            "Time [ms]",
            "Force [uN]",
            "Tip Displacement [um]",
            "Base Displacement [um]",
            "Current Size [um]",
            "Temperature [°C]",
        ]

    @property
    def instrument(self) -> str:
        return "MicroTester G2"
