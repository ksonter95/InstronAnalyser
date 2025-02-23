import argparse
import experiment.experiment as experiment
import pandas as pd

from pathlib import Path


# === Data frames ============================================================ #


class Frame:
    """
    Base class for all Instron 68TM data frames.
    """

    @property
    def displacement(self) -> "pd.Series[float]":
        return self._frame["Displacement [mm]"]  # type: ignore

    @property
    def force(self) -> "pd.Series[float]":
        return self._frame["Force [N]"]  # type: ignore

    @property
    def strain(self) -> "pd.Series[float]":
        return self._frame["Strain [%]"]  # type: ignore

    @property
    def stress(self) -> "pd.Series[float]":
        return self._frame["Compressive stress [MPa]"]  # type: ignore

    @property
    def time(self) -> "pd.Series[float]":
        return self._frame["Time [s]"]  # type: ignore


class RawFrame(experiment.RawFrame, Frame):
    """
    Raw output of an Instron 68TM experiment.

    Args:
        frame: Underlying pd.DataFrame representation of the data.
    """

    @classmethod
    def load(cls, csv: Path) -> "RawFrame":
        """
        Loads the CSV file into a frame and validates its contents.

        Args:
            csv: The path to the CSV file containing the Instron 68TM output.
        """

        try:
            # Read the CSV file
            # NOTE: the column headings are split across two rows and formatted
            #       weirdly such that all units are on the second row except the
            #       strain.  Therefore, the two rows are combined into one
            frame: pd.DataFrame = pd.read_csv(  # type: ignore
                csv, skiprows=19, header=[0, 1]
            ).iloc[:, :5]
            frame.columns = [
                (
                    " ".join(map(str, c)).strip()
                    if not c[1].startswith("Unnamed")
                    else str(c[0])
                )
                for c in frame.columns
            ]
            # NOTE: replace parenthesis with square brackets
            frame.columns = [
                c.translate(str.maketrans("()", "[]")) for c in frame.columns
            ]

            # Validate the CSV file
            #  - Data headings must be in rows 19-20, columns 0-4 (0-indexed) and
            #    must be:
            #       Time, Displacement, Force, Strain (%), Compressive stress
            #       (s), (mm),          (N),   ,           (MPa)
            #  - Data must be in rows 21-... (0-indexed) and must be all floating
            #    point numbers
            headings: list[str] = [
                "Time [s]",
                "Displacement [mm]",
                "Force [N]",
                "Strain [%]",
                "Compressive stress [MPa]",
            ]
            if (
                frame.columns.tolist() != headings
                or not frame.notna().all().all()  # type: ignore
            ):
                raise ValueError

        except:
            raise ValueError(f"Invalid CSV file: {csv}")

        return RawFrame(frame)


class ProcessedFrame(experiment.ProcessedFrame, Frame):
    """
    Base class for all processed outputs of an Instron 68TM experiment.

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
    Base class for all data of an Instron 68TM experiment.

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
    Base class for all Instron 68TM summaries.

    Args:
        frame: Underlying pd.DataFrame representation of the summary.
    """

    pass


# === Analysers ============================================================== #


class Analyser(experiment.Analyser):
    """
    Base class for all Instron 68TM analysers.

    Args:
        input_csv: The path to the CSV file containing the output of the Instron
            68TM experiment.
        output_xlsx: The path to the Excel file which will contain the analysis
            results.
        parameters: The parameters to use when analysing the Instron 68TM
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
    Base class for all Instron 68TM command-line parsers.

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
        Adds the Instron 68TM command-line parser to the instrument subparser.

        Args:
            subparser: The instrument subparser to which to add the Instron 68TM
                parser.

        Returns:
            argparse.ArgumentParser: Created Instron 68TM command-line parser.
        """

        parser: argparse.ArgumentParser = subparser.add_parser(  # type: ignore
            "Instron-68TM",
            description="Analyses the data from an Instron 68TM",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )

        return parser  # type: ignore

    @staticmethod
    def create_subparser(  # type: ignore
        parser: argparse.ArgumentParser,
    ) -> argparse._SubParsersAction:  # type: ignore
        """
        Creates the Instron 68TM experiment subparser.

        Args:
            parser: Instron 68TM parser to which the experiment subparser is to
                be added.

        Returns:
            argparse._SubParsersAction: Created experiment subparser.
        """

        return parser.add_subparsers(
            dest="experiment",
            required=True,
            help="Instron 68TM experiment for which the data is to be analysed",
        )


# === User Interface Widgets ================================================= #


class Widget(experiment.Widget):
    """
    Base class for all Instron 68TM user interface widgets.

    Args:
        view: Generated user interface widget.
        parameters: The parameters to use when analysing the experiment.
    """

    @property
    def instrument(self) -> str:
        return "Instron 68TM"
