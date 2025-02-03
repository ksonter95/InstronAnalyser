import argparse
from typing import Optional
import analyser

from pathlib import Path


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

        print(Path(value).resolve(), flush=True)

        if not Path(value).is_dir():
            raise argparse.ArgumentTypeError(f"Directory '{value}' does not exist")

        return Path(value)

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


class AnalyserParser:
    """
    Base class for all analyser parsers.

    Args:
        parsed_arguments: The parsed command line arguments.
    """

    def __init__(self, parsed_arguments: argparse.Namespace) -> None:

        input_csv: Optional[Path] = parsed_arguments.csv
        input_directory: Optional[Path] = parsed_arguments.directory
        output_directory: Optional[Path] = parsed_arguments.output_directory

        self.files: list[tuple[Path, Path]] = []
        if input_csv is not None:
            self.files.append(
                (input_csv, self._create_output_xlsx(input_csv, output_directory))
            )

        elif input_directory is not None:
            for input_csv in input_directory.iterdir():
                if not input_csv.is_file() or not input_csv.suffix == ".csv":
                    continue

                self.files.append(
                    (input_csv, self._create_output_xlsx(input_csv, output_directory))
                )

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
        """Creates the analyser parser.

        Returns:
            argparse.ArgumentParser: Created analyser parser.
        """

        parser = argparse.ArgumentParser(
            "Instron Analyser",
            description="Analyses the data output from the Instron",
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
            help="Path to the directory into which the generated CSV files will be "
            "saved",
            type=ArgparseTypes.directory,
        )

        return parser

    @staticmethod
    def create_test_subparser(  # type: ignore
        parser: argparse.ArgumentParser,
    ) -> argparse._SubParsersAction:  # type: ignore
        """
        Creates the test subparser.

        Args:
            parser: Analyser parser to which the test subparser is to be added.

        Returns:
            argparse._SubParsersAction: Created test subparser.
        """

        return parser.add_subparsers(dest="test", required=True)


class RelaxationAnalyserParser(AnalyserParser):
    """
    Parser for the RelaxationAnalyser.

    Args:
        parsed_arguments: The parsed command line arguments.
    """

    def __init__(self, parsed_arguments: argparse.Namespace) -> None:

        super().__init__(parsed_arguments)

        self.relaxation_intervals: int = parsed_arguments.relaxation_intervals
        self.relaxation_step_pct: float = parsed_arguments.relaxation_step
        self.epsilon_pct: float = parsed_arguments.epsilon
        self.regression_data_points: int = parsed_arguments.regression_data_points

    def create_analysers(self) -> list[analyser.RelaxationAnalyser]:
        """
        Creates the RelaxationAnalysers from the parsed command line arguments.

        Returns:
            list[analyser.RelaxationAnalyser]: List of all RelaxationAnalysers to be used
                for analysis.
        """

        return [
            analyser.RelaxationAnalyser(
                input_csv,
                output_xlsx,
                self.relaxation_intervals,
                self.relaxation_step_pct,
                self.epsilon_pct,
                self.regression_data_points,
            )
            for input_csv, output_xlsx in self.files
        ]

    @staticmethod
    def add_parser(subparser: argparse._SubParsersAction) -> None:  # type: ignore
        """Adds a parser to the analyser subparser.

        Args:
            subparser: Analyser subparser to which to add the relaxation
                analyser parser.
        """

        parser: argparse.ArgumentParser = subparser.add_parser(  # type: ignore
            "relaxation",
            description="Analyses the data assuming it contains relaxation data",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )

        parser.add_argument(  # type: ignore
            "-i",
            "--relaxation-intervals",
            help="The number of relaxation intervals within the raw data to "
            "include in the analysis.  This is used in combination with "
            "--relaxation-step to determine the relaxation strains to include "
            "in the analysis.  For instance, for --relaxation-intervals 6 and "
            "--relaxation-step 5.0, the analysis will include the strains "
            "[5, 10, 15, 20, 25, 30]",
            type=ArgparseTypes.positive_non_zero_integer,
            default=6,
        )
        parser.add_argument(  # type: ignore
            "-s",
            "--relaxation-step",
            help="The difference between consecutive relaxation strains to use "
            "in the analysis.  This is used in combination with "
            "--relaxation-intervals to determine the relaxation strains to "
            "include in the analysis.  For instance, for "
            "--relaxation-intervals 6 and --relaxation-step 5.0, the analysis "
            "will include the strains [5, 10, 15, 20, 25, 30]",
            type=ArgparseTypes.positive_non_zero_float,
            default=5.0,
        )
        parser.add_argument(  # type: ignore
            "-e",
            "--epsilon",
            help="Allowable percentage tolerance on the specified strain for "
            "creating the dataset at the required strain",
            type=ArgparseTypes.positive_non_zero_float,
            default=0.01,
        )
        parser.add_argument(  # type: ignore
            "-n",
            "--regression-data-points",
            help="Number of data points to include in the regression analysis",
            type=ArgparseTypes.positive_non_zero_integer,
        )


class FailureAnalyserParser(AnalyserParser):
    """
    Parser for the FailureAnalyser.

    Args:
        parsed_arguments: The parsed command line arguments.
    """

    def __init__(self, parsed_arguments: argparse.Namespace) -> None:

        super().__init__(parsed_arguments)

        self.abort_strain_pct: float = parsed_arguments.abort_strain
        self.toughness_strain_pct: float = parsed_arguments.toughness_strain
        self.stiffness_strain_pct: float = parsed_arguments.stiffness_strain

    def create_analysers(self) -> list[analyser.FailureAnalyser]:
        """
        Creates the RelaxationAnalysers from the parsed command line arguments.

        Returns:
            list[analyser.RelaxationAnalyser]: List of all RelaxationAnalysers to be used
                for analysis.
        """

        return [
            analyser.FailureAnalyser(
                input_csv,
                output_xlsx,
                self.abort_strain_pct,
                self.toughness_strain_pct,
                self.stiffness_strain_pct,
            )
            for input_csv, output_xlsx in self.files
        ]

    @staticmethod
    def add_parser(subparser: argparse._SubParsersAction) -> None:  # type: ignore
        """Adds a parser to the analyser subparser.

        Args:
            subparser: Analyser subparser to which to add the compression to
                failure analyser parser.
        """

        parser: argparse.ArgumentParser = subparser.add_parser(  # type: ignore
            "failure",
            description="Analyses the data assuming it contains compression "
            "to failure data",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )

        parser.add_argument(  # type: ignore
            "-a",
            "--abort-strain",
            help="The strain at which the test aborts even if the sample has "
            "not yet failed",
            type=ArgparseTypes.positive_non_zero_float,
            default=95.0,
        )
        parser.add_argument(  # type: ignore
            "-t",
            "--toughness-strain",
            help="The strain at which the toughness is calculated",
            type=ArgparseTypes.positive_non_zero_float,
            default=4.0,
        )
        parser.add_argument(  # type: ignore
            "-s",
            "--stiffness-strain",
            help="The strain at which the stiffness is calculated",
            type=ArgparseTypes.positive_non_zero_float,
            default=4.0,
        )


if __name__ == "__main__":
    parser: argparse.ArgumentParser = AnalyserParser.create_parser()
    subparser: argparse._SubParsersAction = (  # type: ignore
        AnalyserParser.create_test_subparser(parser)  # type: ignore
    )

    # Add the test-specific subparsers
    RelaxationAnalyserParser.add_parser(subparser)  # type: ignore
    FailureAnalyserParser.add_parser(subparser)  # type: ignore

    # Parse the arguments
    parsed_arguments: argparse.Namespace = parser.parse_args()

    analysers: list[analyser.Analyser]
    match str(parsed_arguments.test):
        case "relaxation":
            analysers = RelaxationAnalyserParser(parsed_arguments).create_analysers() # type: ignore
        case "failure":
            analysers = FailureAnalyserParser(parsed_arguments).create_analysers() # type: ignore
        case _:
            pass

    for a in analysers: # type: ignore
        a.analyse()
        a.save()

        print(a)
