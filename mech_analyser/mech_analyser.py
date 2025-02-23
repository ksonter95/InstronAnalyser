import argparse
import experiment.experiment as experiment
import experiment.instron_68tm.experiment as instron_68tm
import experiment.instron_68tm.failure.experiment as failure
import experiment.instron_68tm.stepwise.experiment as stepwise


if __name__ == "__main__":
    parser: argparse.ArgumentParser = experiment.Parser.create_parser()
    subparser: argparse._SubParsersAction = (  # type: ignore
        experiment.Parser.create_subparser(parser)  # type: ignore
    )

    # Add the instrument-specific parsers
    instron_68tm_parser: argparse.ArgumentParser = instron_68tm.Parser.add_parser(  # type: ignore
        subparser
    )
    instron_68tm_subparser: argparse._SubParsersAction = (  # type: ignore
        instron_68tm.Parser.create_subparser(instron_68tm_parser)  # type: ignore
    )

    # Add the Instron 68TM-specific parsers
    stepwise.Parser.add_parser(instron_68tm_subparser)  # type: ignore
    failure.Parser.add_parser(instron_68tm_subparser)  # type: ignore

    # Parse the arguments
    parsed_arguments: argparse.Namespace = parser.parse_args()

    analysers: list[experiment.Analyser]
    match str(parsed_arguments.instrument):
        case "Instron-68TM":
            match str(parsed_arguments.experiment):
                case "stepwise":
                    analysers = stepwise.Parser(parsed_arguments).create_analysers()  # type: ignore
                case "failure":
                    analysers = failure.Parser(parsed_arguments).create_analysers()  # type: ignore
                case _:
                    pass
        case _:
            pass

    for i in range(len(analysers)):  # type: ignore
        print(f"{i + 1}/{len(analysers)}: {analysers[i].output_xlsx.name}")  # type: ignore

        analysers[i].analyse()  # type: ignore
        analysers[i].save()  # type: ignore
