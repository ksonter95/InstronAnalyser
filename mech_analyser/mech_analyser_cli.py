import argparse
import experiment.experiment as experiment
import importlib
import os

from types import ModuleType

_EXPERIMENTS_DIR: str = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "experiment")
)
_EXPERIMENTS: dict[str, dict[str, dict[str, ModuleType] | ModuleType]] = {
    d1: {
        "module": importlib.import_module(f"experiment.{d1}.experiment"),
        "experiments": {
            d2: importlib.import_module(f"experiment.{d1}.{d2}.experiment")
            for d2 in os.listdir(os.path.join(_EXPERIMENTS_DIR, d1))
            if os.path.isdir(os.path.join(_EXPERIMENTS_DIR, d1, d2))
            and not d2.startswith("_")
            and os.path.exists(os.path.join(_EXPERIMENTS_DIR, d1, d2, "experiment.py"))
        },
    }
    for d1 in os.listdir(_EXPERIMENTS_DIR)
    if os.path.isdir(os.path.join(_EXPERIMENTS_DIR, d1)) and not d1.startswith("_")
}

if __name__ == "__main__":
    parser: argparse.ArgumentParser = experiment.Parser.create_parser()
    subparser: argparse._SubParsersAction = experiment.Parser.create_subparser(parser)  # type: ignore

    # Dynamically add instruments and their experiment parsers
    for _, instrument_imports in _EXPERIMENTS.items():
        if not hasattr(instrument_imports["module"], "Parser"):
            continue
        instrument_parser: argparse.ArgumentParser = getattr(
            instrument_imports["module"], "Parser"
        ).add_parser(subparser)
        instrument_subparser: argparse._SubParsersAction = getattr(  # type: ignore
            instrument_imports["module"], "Parser"
        ).create_subparser(instrument_parser)

        for _, experiment_imports in instrument_imports["experiments"].items():
            if not hasattr(experiment_imports, "Parser"):
                continue

            getattr(experiment_imports, "Parser").add_parser(instrument_subparser)

    # Parse the arguments
    parsed_arguments: argparse.Namespace = parser.parse_args()

    # Create the experiment analysers
    analysers: list[experiment.Analyser] = []
    for instrument_name, instrument_imports in _EXPERIMENTS.items():
        if str(parsed_arguments.instrument) != instrument_name:
            continue

        for experiment_name, experiment_imports in instrument_imports[
            "experiments"
        ].items():
            if str(parsed_arguments.experiment) != experiment_name:
                continue

            analysers = getattr(experiment_imports, "Parser")(
                parsed_arguments
            ).create_analysers()

    # Analyse the experiments
    for i in range(len(analysers)):
        print(f"{i + 1}/{len(analysers)}: {analysers[i].output_xlsx.name}")

        analysers[i].analyse()
        analysers[i].save()
