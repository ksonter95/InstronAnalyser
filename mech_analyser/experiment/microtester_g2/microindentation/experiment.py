import argparse
import dataclasses
import experiment.experiment as experiment
import experiment.microtester_g2.experiment as microtester_g2
import experiment.microtester_g2.microindentation.view as view


import pandas as pd

from pathlib import Path

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
        # TODO


# === Parameters ============================================================= #


@dataclasses.dataclass
class DataParameters(experiment.DataParameters):
    """
    Parameters of a microindentation experiment using a MicroTester G2.

    Args:
        TODO
    """

    # TODO


@dataclasses.dataclass
class AnalyserParameters(microtester_g2.experiment.AnalyserParameters):
    """
    Parameters of an analyser of a microindentation experiment using a
    MicroTester G2.

    Args:
        TODO
    """

    # TODO


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

    def process(self, parameters: DataParameters) -> None:  # type: ignore
        """
        Processes the raw data from the microindentation experiment using a
        MicroTester G2.

        Dataset filtering:
            - TODO

        Columns that are populated:
            - TODO

        Summary parameters that are calculated:
            - TODO

        Args:
            parameters: The parameters to use when processing the microindentation
                MicroTester G2 experiment data.
        """

        # Filter the raw data
        self.processed_frame = Frame(
            self.raw_frame.frame,  # TODO
            f"Microindentation",
        )

        # Add the additional columns
        # TODO

        # Calculate the remaining summary parameters
        # TODO


# === Results ================================================================ #


class Summary(microtester_g2.Summary):
    """
    Summary of the microindentation MicroTester G2 experiment.
    """

    def __init__(self) -> None:

        super().__init__(
            pd.DataFrame(
                columns=[
                    # TODO
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
            # TODO
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

        for _ in range(1):  # TODO
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

        self.summary.clear_all_rows()

        for i in range(len(self.data)):
            parameters = DataParameters(
                # TODO
            )
            self.data[i].process(parameters)
            self.summary.append_row(self.data[i], parameters)


# === Command-line parsers =================================================== #


class Parser(microtester_g2.Parser):
    """
    Parser for the microindentation MicroTester G2 experiment.

    Args:
        parsed_arguments: The parsed command-line arguments.
    """

    def __init__(self, parsed_arguments: argparse.Namespace) -> None:

        super().__init__(parsed_arguments)

        self._parameters = AnalyserParameters(
            # TODO
        )

    def create_analysers(self) -> list[Analyser]:  # type: ignore
        """
        Creates the microindentation MicroTester G2 experiment analysers from
        the parsed command-line arguments.

        Returns:
            list[Analyser]: List of all microindentation MicroTester G2
                experiment analysers.
        """

        return [
            Analyser(input_csv, output_xlsx, self._parameters)
            for input_csv, output_xlsx in self._files
        ]

    @staticmethod
    def add_parser(subparser: argparse._SubParsersAction) -> None:  # type: ignore
        """
        Adds the microindentation MicroTester G2 experiment parser to the
        MicroTester G2 experiment subparser.

        Args:
            subparser: MicroTester G2 experiment subparser to which to add the
                microindentation MicroTester G2 experiment parser.
        """

        parser: argparse.ArgumentParser = subparser.add_parser(  # type: ignore
            Path(__file__).parent.name,
            description="Analyses the data from a microindentation MicroTester G2 "
            " experiment",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )

        # TODO: parser.add_argument()


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
        # TODO

        # Connect signals with slots
        # TODO

        # Set initial views
        # TODO

    def sync_parameters(self) -> None:
        """
        Synchronise the parameters to use when analysing the experiment with the
        widget input fields.
        """

        # TODO
