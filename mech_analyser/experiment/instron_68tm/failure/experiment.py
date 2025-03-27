import argparse
import dataclasses
import experiment.experiment as experiment
import experiment.instron_68tm.experiment as instron_68tm
import experiment.instron_68tm.failure.view as view

import numpy as np
import pandas as pd

from pathlib import Path
from scipy.integrate import cumulative_trapezoid  # type: ignore
from scipy.optimize import curve_fit  # type: ignore
from typing import Optional

# === Data frames ============================================================ #


class Frame(instron_68tm.ProcessedFrame):
    """
    Processed output of a compression-to-failure experiment using an Instron
    68TM.

    Args:
        frame: Underlying pd.DataFrame representation of the data.
        sheet_name: The name of the Excel sheet to which the data will be
            written.
    """

    def __init__(self, frame: pd.DataFrame, sheet_name: str) -> None:

        super().__init__(frame, sheet_name)

        # Initially populate the processed data columns with default values
        self.toughness = pd.Series([0.0] * self._frame.index.size)  # type: ignore

    @property
    def toughness(self) -> "pd.Series[float]":
        return self._frame["Toughness [MPa]"]  # type: ignore

    @toughness.setter
    def toughness(self, value: "pd.Series[float]") -> None:
        self._frame["Toughness [MPa]"] = value


# === Parameters ============================================================= #


@dataclasses.dataclass
class DataParameters(experiment.DataParameters):
    """
    Parameters of a compression-to-failure experiment using an Instron 68TM.

    Args:
        abort_strain_pct: The strain at which the experiment aborts even if the
            sample has not yet failed.
        toughness_strain_pct: The strain at which the toughness is calculated.
            If set to None, the failure or abort strain will be used.
        e_modulus_strain1_pct: The strain value which defines the first
            datapoint on the stress-strain curve used to calculate the Young's
            modulus.  It is ε1 in the equation E = (σ2 - σ1) / (ε2 - ε1)
        e_modulus_strain2_pct: The strain value which defines the second
            datapoint on the stress-strain curve used to calculate the Young's
            modulus.  It is ε2 in the equation E = (σ2 - σ1) / (ε2 - ε1)
    """

    abort_strain_pct: float = 95.0
    toughness_strain_pct: Optional[float] = None
    e_modulus_strain1_pct: float = 10.0
    e_modulus_strain2_pct: float = 15.0


@dataclasses.dataclass
class AnalyserParameters(experiment.AnalyserParameters):
    """
    Parameters of an analyser of a compression-to-failure experiment using an
    Instron 68TM.

    Args:
        abort_strain_pct: The strain at which the experiment aborts even if the
            sample has not yet failed.
        toughness_strain_pct: The strain at which the toughness is calculated.
            If set to None, the failure or abort strain will be used.
        e_modulus_strain1_pct: The strain value which defines the first
            datapoint on the stress-strain curve used to calculate the Young's
            modulus.  It is ε1 in the equation E = (σ2 - σ1) / (ε2 - ε1)
        e_modulus_strain2_pct: The strain value which defines the second
            datapoint on the stress-strain curve used to calculate the Young's
            modulus.  It is ε2 in the equation E = (σ2 - σ1) / (ε2 - ε1)
    """

    abort_strain_pct: float = 95.0
    toughness_strain_pct: Optional[float] = None
    e_modulus_strain1_pct: float = 10.0
    e_modulus_strain2_pct: float = 15.0


# === Data =================================================================== #


class Data(instron_68tm.Data):
    """
    Data of a compression-to-failure experiment using an Instron 68TM.

    Args:
        raw_frame: The raw data frame from which the processed data frame is
            created.
    """

    def __init__(self, raw_frame: instron_68tm.RawFrame) -> None:

        super().__init__(
            raw_frame,
            Frame(
                pd.DataFrame(columns=raw_frame.frame.columns),
                "Toughness",
            ),
        )

        self._aborted: bool = False
        self._e_modulus_MPa: float = 0.0
        self._toughness_id: int = 0
        self._ultimate_id: int = 0
        self._yield_id: int = 0

    @property
    def aborted(self) -> bool:
        return self._aborted

    @property
    def e_modulus_MPa(self) -> float:
        return self._e_modulus_MPa

    @property
    def processed_frame(self) -> Frame:
        return super().processed_frame  # type: ignore

    @processed_frame.setter
    def processed_frame(self, value: Frame) -> None:  # type: ignore
        super(Data, Data).processed_frame.__set__(self, value)  # type: ignore

    @property
    def toughness_MPa(self) -> float:
        return self.processed_frame.toughness.loc[self._toughness_id]

    @property
    def toughness_strain_pct(self) -> float:
        return self.processed_frame.strain.loc[self._toughness_id]

    @property
    def ultimate_force_N(self) -> float:
        return self.processed_frame.force.loc[self._ultimate_id]

    @property
    def ultimate_strain_pct(self) -> float:
        return self.processed_frame.strain.loc[self._ultimate_id]

    @property
    def ultimate_strength_MPa(self) -> float:
        return self.processed_frame.stress.loc[self._ultimate_id]

    @property
    def yield_force_N(self) -> float:
        # TODO: return self.processed_frame.force.loc[self._yield_id]
        return 0.0

    @property
    def yield_strain_pct(self) -> float:
        # TODO: return self.processed_frame.strain.loc[self._yield_id]
        return 0.0

    @property
    def yield_strength_MPa(self) -> float:
        # TODO: return self.processed_frame.stress.loc[self._yield_id]
        return 0.0

    def process(self, parameters: DataParameters) -> None:  # type: ignore
        """
        Processes the raw data from the compression-to-failure experiment using
        an Instron 68TM.

        Dataset filtering:
            -

        Columns that are populated:
            - Toughness: The area under the stress-strain curve up until each
                data point.

        Summary parameters that are calculated:
            - E-modulus: The slope of the stress-strain curve between the
                specified strains as determined by linear regression.
            - Toughness strain: The measured strain closest to the strain at
                which the toughness is to be calculated.
            - Toughness: The area under the stress-strain curve up until the
                toughness strain.
            - Yield force: The force at which the material begins to deform.
            - Yield strain: The strain at which the material begins to deform.
            - Yield strength: The stress at which the material begins to deform.
            - Ultimate force: The maximum force that the material can withstand.
            - Ultimate strain: The maximum strain that the material can
                withstand.
            - Ultimate strength: The maximum stress that the material can
                withstand.

        Args:
            parameters: The parameters to use when processing the
                compression-to-failure Instron 68TM experiment data.
        """

        self.processed_frame = Frame(self.raw_frame.frame, "Toughness")

        # Add the toughness column
        # NOTE: np.insert is required because the output of
        #       cumulative_trapezoid() is an array one less than the length of
        #       the data frame
        self.processed_frame.toughness = pd.Series(  # type: ignore
            np.insert(
                cumulative_trapezoid(
                    self.processed_frame.stress,
                    # NOTE: convert from percentage to decimal
                    self.processed_frame.strain / 100,
                ),
                0,
                0,
            )
        )

        # Calculate the parameters of the linear equation that best fits the
        # data points
        [self._e_modulus_MPa, _], _ = curve_fit(  # type: ignore
            self.y,
            self.processed_frame.strain[
                (self.processed_frame.strain > (parameters.e_modulus_strain1_pct))
                & (self.processed_frame.strain < (parameters.e_modulus_strain2_pct))
            ]
            # NOTE: convert from percentage to decimal
            / 100.0,
            self.processed_frame.stress[
                (self.processed_frame.strain > (parameters.e_modulus_strain1_pct))
                & (self.processed_frame.strain < (parameters.e_modulus_strain2_pct))
            ],
        )

        # Calculate the remaining summary parameters
        self._aborted = self.ultimate_strain_pct >= parameters.abort_strain_pct
        self._ultimate_id = self.processed_frame.stress.idxmax()  # type: ignore
        self._toughness_id = (
            self._ultimate_id
            if parameters.toughness_strain_pct is None
            else (self.processed_frame.strain - parameters.toughness_strain_pct)
            .abs()
            .idxmin()  # type: ignore
        )
        self._yield_id = 0  # TODO: implement

    @staticmethod
    def y(x: float, E: float, c: float) -> float:
        """
        Calculates the stress according to following equation:
        y = E * x + c

        Args:
            x: Strain at which the stress is to be calculated.
            E: Young's modulus (slope of the stress-strain curve).
            c: Initial stress at zero strain of the function.

        Returns:
            Stress at strain x.
        """

        return E * x + c


# === Results ================================================================ #


class Summary(instron_68tm.Summary):
    """
    Summary of the compression-to-failure Instron experiment.
    """

    def __init__(self) -> None:

        super().__init__(
            pd.DataFrame(
                columns=[
                    "Yield force [N]",
                    "Yield strain [%]",
                    "Yield strength [MPa]",
                    "Ultimate force [N]",
                    "Ultimate strain [%]",
                    "Ultimate strength [MPa]",
                    "E-modulus [MPa]",
                    "Toughness strain [%]",
                    "Toughness [MPa]",
                ]
            )
        )

    def append_row(self, data: Data, parameters: DataParameters) -> None:  # type: ignore
        """
        Append a row to the summary frame.

        Args:
            data: The data of a compression-to-failure Instron 68TM experiment
                to be appended.
            parameters: The parameters of a compression-to-failure experiment
                using an Instron 68TM used to process the data.
        """

        self._frame.loc[len(self._frame)] = [
            data.yield_force_N,
            data.yield_strain_pct,
            data.yield_strength_MPa,
            data.ultimate_force_N,
            data.ultimate_strain_pct,
            data.ultimate_strength_MPa,
            data.e_modulus_MPa,
            data.toughness_strain_pct,
            data.toughness_MPa,
        ]


# === Analysers ============================================================== #


class Analyser(instron_68tm.Analyser):
    """
    Analyser of the compression-to-failure Instron 68TM experiment.

    Args:
        input_csv: The path to the CSV file containing the output of the
            compression-to-failure Instron 68TM experiment.
        output_xlsx: The path to the Excel file which will contain the analysis
            results.
        parameters: The parameters to use when analysing the
            compression-to-failure Instron 68TM experiment.
    """

    def __init__(
        self,
        input_csv: Path,
        output_xlsx: Path,
        parameters: AnalyserParameters,
    ) -> None:

        super().__init__(input_csv, output_xlsx, parameters, Summary())

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
        Analyses the output of the compression-to-failure Instron 68TM
        experiment.
        """

        self.summary.clear_all_rows()

        for i in range(len(self.data)):
            parameters = DataParameters(
                self.parameters.abort_strain_pct,
                self.parameters.toughness_strain_pct,
                self.parameters.e_modulus_strain1_pct,
                self.parameters.e_modulus_strain2_pct,
            )
            self.data[i].process(parameters)
            self.summary.append_row(self.data[i], parameters)


# === Command-line parsers =================================================== #


class Parser(instron_68tm.Parser):
    """
    Parser for the compression-to-failure Instron 68TM experiment.

    Args:
        parsed_arguments: The parsed command-line arguments.
    """

    def __init__(self, parsed_arguments: argparse.Namespace) -> None:

        super().__init__(parsed_arguments)

        self._parameters = AnalyserParameters(
            parsed_arguments.abort_strain,
            parsed_arguments.toughness_strain,
            parsed_arguments.e_modulus_strain1,
            parsed_arguments.e_modulus_strain2,
        )

    def create_analysers(self) -> list[Analyser]:  # type: ignore
        """
        Creates the compression-to-failure Instron 68TM experiment analysers
        from the parsed command-line arguments.

        Returns:
            list[Analyser]: List of all compression-to-failure Instron 68TM
                experiment analysers.
        """

        return [
            Analyser(input_csv, output_xlsx, self._parameters)
            for input_csv, output_xlsx in self._files
        ]

    @staticmethod
    def add_parser(subparser: argparse._SubParsersAction) -> None:  # type: ignore
        """
        Adds the compression-to-failure Instron 68TM experiment subparser to
        to the Instron 68TM experiment subparser.

        Args:
            subparser: Instron 68TM experiment subparser to which to add the
                compression-to-failure Instron 68TM experiment parser.
        """

        parser: argparse.ArgumentParser = subparser.add_parser(  # type: ignore
            Path(__file__).parent.name,
            description="Analyses the data from a compression-to-failure "
            "Instron 68TM experiment",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )

        parser.add_argument(  # type: ignore
            "-a",
            "--abort-strain",
            help="The strain at which the experiment aborts even if the sample "
            "has not yet failed",
            type=experiment.ArgparseTypes.percentage_float,
            default=95.0,
        )
        parser.add_argument(  # type: ignore
            "-t",
            "--toughness-strain",
            help="The strain at which the toughness is calculated",
            type=experiment.ArgparseTypes.percentage_float,
            default=4.0,
        )
        parser.add_argument(  # type: ignore
            "-e",
            "--e-modulus_strain1",
            help="The strain value which defines the first datapoint on the "
            "stress-strain curve used to calculate the Young's modulus.  "
            "It is ε1 in the equation E = (σ2 - σ1) / (ε2 - ε1)",
            type=experiment.ArgparseTypes.percentage_float,
            default=10,
        )
        parser.add_argument(  # type: ignore
            "-f",
            "--e-modulus_strain2",
            help="The strain value which defines the second datapoint on the "
            "stress-strain curve used to calculate the Young's modulus.  "
            "It is ε2 in the equation E = (σ2 - σ1) / (ε2 - ε1)",
            type=experiment.ArgparseTypes.percentage_float,
            default=15,
        )


# === User Interface Widgets ================================================= #


class Widget(instron_68tm.Widget):
    """
    User interface widget for the compression-to-failure Instron 68TM
    experiment.
    """

    def __init__(self) -> None:
        super().__init__(view.Ui_w_Failure(), AnalyserParameters())  # type: ignore

    @property
    def experiment(self) -> str:
        return "Compression-to-failure"

    @property
    def parameters(self) -> AnalyserParameters:
        return super().parameters  # type: ignore

    @property
    def view(self) -> view.Ui_w_Failure:  # type: ignore
        return super().view  # type: ignore

    def create_analyser(  # type: ignore
        self, input_csv: Path, output_xlsx: Path, parameters: AnalyserParameters
    ) -> Analyser:
        """
        Creates the experiment analyser.

        Args:
            input_csv: The path to the CSV file containing the output of the
                compression-to-failure Instron 68TM experiment.
            output_xlsx: The path to the Excel file which will contain the
                analysis results.
            parameters: The parameters to use when analysing the
                compression-to-failure Instron 68TM experiment.
        """

        return Analyser(input_csv, output_xlsx, parameters)

    def init(self) -> None:
        """
        Initialises the widget by setting the input fields to the defaults of
        the parameters to use when analysing the experiment and connecting any
        signals with an associated slot.
        """

        # Set the input fields to the defaults
        self.view.sb_Abort.setValue(self.parameters.abort_strain_pct)
        self.view.cb_Toughness.setChecked(
            self.parameters.toughness_strain_pct is not None
        )
        self.view.sb_Toughness.setValue(
            self.parameters.toughness_strain_pct
            if self.parameters.toughness_strain_pct is not None
            else 0.0
        )
        self.view.sb_Strain1.setValue(self.parameters.e_modulus_strain1_pct)
        self.view.sb_Strain2.setValue(self.parameters.e_modulus_strain2_pct)

        # Connect signals with slots
        self.view.cb_Toughness.checkStateChanged.connect(
            self._handle_cb_Toughness_changed
        )

        # Set initial views
        self.view.sb_Toughness.setEnabled(self.view.cb_Toughness.isChecked())

    def sync_parameters(self) -> None:
        """
        Synchronise the parameters to use when analysing the experiment with the
        widget input fields.
        """

        self.parameters.abort_strain_pct = self.view.sb_Abort.value()
        self.parameters.toughness_strain_pct = (
            self.view.sb_Toughness.value()
            if self.view.cb_Toughness.isChecked()
            else None
        )
        self.parameters.e_modulus_strain1_pct = self.view.sb_Strain1.value()
        self.parameters.e_modulus_strain2_pct = self.view.sb_Strain2.value()

    def _handle_cb_Toughness_changed(self) -> None:
        """
        Enables/disables sb_Toughness.
        """

        self.view.sb_Toughness.setEnabled(self.view.cb_Toughness.isChecked())
