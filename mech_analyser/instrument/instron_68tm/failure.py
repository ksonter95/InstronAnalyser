import argparse
import instrument.instrument as instrument
import instrument.instron_68tm.instron_68tm as instron_68tm

import numpy as np
import pandas as pd

from pathlib import Path
from scipy.integrate import cumulative_trapezoid  # type: ignore
from scipy.optimize import curve_fit  # type: ignore

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
        self.stiffness = pd.Series([0.0] * self._frame.index.size)  # type: ignore

    @property
    def stiffness(self) -> "pd.Series[float]":
        return self._frame["Stiffness [N/mm]"]  # type: ignore

    @stiffness.setter
    def stiffness(self, value: "pd.Series[float]") -> None:
        self._frame["Stiffness [N/mm]"] = value

    @property
    def toughness(self) -> "pd.Series[float]":
        return self._frame["Toughness [MPa]"]  # type: ignore

    @toughness.setter
    def toughness(self, value: "pd.Series[float]") -> None:
        self._frame["Toughness [MPa]"] = value


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
                "Toughness and Stiffness",
            ),
        )

        self._abort_strain_pct: float = 0.0
        self._e_modulus_MPa: float = 0.0
        self._stiffness_strain_pct: float = 0.0
        self._toughness_strain_pct: float = 0.0
        self._yield_strain_pct: float = 0.0

    @property
    def aborted(self) -> bool:
        return self.ultimate_strain_pct >= self._abort_strain_pct

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
    def stiffness_N_mm(self) -> float:
        return self.processed_frame.stiffness.loc[
            (self.processed_frame.strain - self._stiffness_strain_pct)
            .abs()
            .idxmin()  # type: ignore
        ]

    @property
    def stiffness_strain_pct(self) -> float:
        return self._stiffness_strain_pct

    @property
    def toughness_MPa(self) -> float:
        return self.processed_frame.toughness.loc[
            (self.processed_frame.strain - self._toughness_strain_pct)
            .abs()
            .idxmin()  # type: ignore
        ]

    @property
    def toughness_strain_pct(self) -> float:
        return self._toughness_strain_pct

    @property
    def ultimate_force_N(self) -> float:
        return self.processed_frame.force.loc[
            self.processed_frame.stress.idxmax()  # type: ignore
        ]

    @property
    def ultimate_strain_pct(self) -> float:
        return self.processed_frame.strain.loc[
            self.processed_frame.stress.idxmax()  # type: ignore
        ]

    @property
    def ultimate_strength_MPa(self) -> float:
        return self.processed_frame.stress.max()  # type: ignore

    @property
    def yield_force_N(self) -> float:
        return self.processed_frame.force.loc[
            (self.processed_frame.strain - self._yield_strain_pct)
            .abs()
            .idxmin()  # type: ignore
        ]

    @property
    def yield_strain_pct(self) -> float:
        return self._yield_strain_pct

    @property
    def yield_strength_MPa(self) -> float:
        return self.processed_frame.stress.loc[
            (self.processed_frame.strain - self._yield_strain_pct)
            .abs()
            .idxmin()  # type: ignore
        ]

    def process(  # type: ignore
        self,
        abort_strain_pct: float,
        toughness_strain_pct: float,
        stiffness_strain_pct: float,
        e_modulus_strain1_pct: float,
        e_modulus_strain2_pct: float,
    ) -> None:
        """
        Processes the raw data from the compression-to-failure experiment using
        an Instron 68TM.

        Dataset filtering:
            -

        Columns that are populated:
            - Toughness: The area under the stress-strain curve up until each
                data point.
            - Stiffness: The extent to which an object resists deformation in
                response to an applied force.

        Summary parameters that are calculated:
            - E-modulus: The slope of the stress-strain curve between the
                specified strains as determined by linear regression.


        Args:
            abort_strain_pct: The strain threshold at which the experiment is
                considered to be aborted.
            toughness_strain_pct: The strain at which the toughness is
                calculated.
            stiffness_strain_pct: The strain at which the stiffness is
                calculated.
            e_modulus_strain1_pct: The strain value which defines the first
                datapoint on the stress-strain curve used to calculate the
                Young's modulus.
            e_modulus_strain2_pct: The strain value which defines the second
                datapoint on the stress-strain curve used to calculate the
                Young's modulus.
        """

        self._abort_strain_pct = abort_strain_pct
        self._toughness_strain_pct = toughness_strain_pct
        self._stiffness_strain_pct = stiffness_strain_pct

        self.processed_frame = Frame(
            self.raw_frame.frame,
            "Toughness and Stiffness",
        )

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

        # Add the stiffness column
        # NOTE: k = F / δ
        #       Where:
        #           - k: stiffness
        #           - F: force
        #           - δ: displacement
        self.processed_frame.stiffness = self.processed_frame.force / (
            self.processed_frame.displacement
        )

        # Calculate the parameters of the linear equation that best fits the
        # data points
        [self._e_modulus_MPa, _], _ = curve_fit(  # type: ignore
            self.y,
            self.processed_frame.strain[
                (self.processed_frame.strain > (e_modulus_strain1_pct))
                & (self.processed_frame.strain < (e_modulus_strain2_pct))
            ]
            # NOTE: convert from percentage to decimal
            / 100.0,
            self.processed_frame.stress[
                (self.processed_frame.strain > (e_modulus_strain1_pct))
                & (self.processed_frame.strain < (e_modulus_strain2_pct))
            ],
        )

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
                    "Stiffness strain [%]",
                    "Stiffness [N/mm]",
                ]
            )
        )

    def append_row(  # type: ignore
        self,
        yield_force_N: float,
        yield_strain_pct: float,
        yield_strength_MPa: float,
        ultimate_force_N: float,
        ultimate_strain_pct: float,
        ultimate_strength_MPa: float,
        e_modulus_MPa: float,
        toughness_strain_pct: float,
        toughness_MPa: float,
        stiffness_strain_pct: float,
        stiffness_N_mm: float,
    ) -> None:
        """
        Append a row to the summary frame.

        Args:
            yield_force_N: The force at which the sample deformation changes
                from elastic to plastic.
            yield_strain_pct: The strain at which the sample deformation changes
                from elastic to plastic.
            yield_strength_MPa: The stress at which the sample deformation
                changes from elastic to plastic.
            ultimate_force_N: The force at which the sample broke or the
                experiment was aborted.
            ultimate_strain_pct: The strain at which the sample broke or the
                experiment was aborted.
            ultimate_strength_MPa: The stress at which the sample broke or the
                experiment was aborted.
            e_modulus_MPa: The Young's modulus of the sample, which is defined
                as the slope of the stress-strain curve at a specified strain.
            toughness_strain_pct: The strain at which the toughness was
                calculated.
            toughness_MPa: The toughness of the sample, which is defined as the
                area under the stress-strain curve up until a specified strain.
            stiffness_strain_pct: The strain at which the stiffness was
                calculated.
            stiffness_N_mm: The stiffness of the sample, which is defined as the
                stress at a specified strain.
        """

        self._frame.loc[len(self._frame)] = [
            yield_force_N,
            yield_strain_pct,
            yield_strength_MPa,
            ultimate_force_N,
            ultimate_strain_pct,
            ultimate_strength_MPa,
            e_modulus_MPa,
            toughness_strain_pct,
            toughness_MPa,
            stiffness_strain_pct,
            stiffness_N_mm,
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
        abort_strain_pct: The strain threshold at which the experiment is
            considered to be aborted.
        toughness_strain_pct: The strain at which the toughness is calculated.
        stiffness_strain_pct: The strain at which the stiffness is calculated.
        e_modulus_strain1_pct: The strain value which defines the first
            datapoint on the stress-strain curve used to calculate the Young's
            modulus.
        e_modulus_strain2_pct: The strain value which defines the second
            datapoint on the stress-strain curve used to calculate the Young's
            modulus.
    """

    def __init__(
        self,
        input_csv: Path,
        output_xlsx: Path,
        abort_strain_pct: float,
        toughness_strain_pct: float,
        stiffness_strain_pct: float,
        e_modulus_strain1_pct: float,
        e_modulus_strain2_pct: float,
    ) -> None:

        super().__init__(input_csv, output_xlsx, Summary())

        self._abort_strain_pct: float
        self._e_modulus_strain1_pct: float
        self._e_modulus_strain2_pct: float
        self._stiffness_strain_pct: float
        self._toughness_strain_pct: float

        self.abort_strain_pct = abort_strain_pct
        self.e_modulus_strain1_pct = e_modulus_strain1_pct
        self.e_modulus_strain2_pct = e_modulus_strain2_pct
        self.stiffness_strain_pct = stiffness_strain_pct
        self.toughness_strain_pct = toughness_strain_pct

        self.data.append(Data(self.raw_frame))

    @property
    def abort_strain_pct(self) -> float:
        return self._abort_strain_pct

    @abort_strain_pct.setter
    def abort_strain_pct(self, value: float) -> None:
        self._abort_strain_pct = value

    @property
    def data(self) -> list[Data]:  # type: ignore
        return super().data  # type: ignore

    @data.setter
    def data(self, value: list[Data]) -> None:  # type: ignore
        super(Analyser, Analyser).data.__set__(self, value)  # type: ignore

    @property
    def e_modulus_strain1_pct(self) -> float:
        return self._e_modulus_strain1_pct

    @e_modulus_strain1_pct.setter
    def e_modulus_strain1_pct(self, value: float) -> None:
        self._e_modulus_strain1_pct = value

    @property
    def e_modulus_strain2_pct(self) -> float:
        return self._e_modulus_strain2_pct

    @e_modulus_strain2_pct.setter
    def e_modulus_strain2_pct(self, value: float) -> None:
        self._e_modulus_strain2_pct = value

    @property
    def stiffness_strain_pct(self) -> float:
        return self._stiffness_strain_pct

    @stiffness_strain_pct.setter
    def stiffness_strain_pct(self, value: float) -> None:
        self._stiffness_strain_pct = value

    @property
    def summary(self) -> Summary:
        return super().summary  # type: ignore

    @property
    def toughness_strain_pct(self) -> float:
        return self._toughness_strain_pct

    @toughness_strain_pct.setter
    def toughness_strain_pct(self, value: float) -> None:
        self._toughness_strain_pct = value

    def analyse(self) -> None:
        """
        Analyses the output of the compression-to-failure Instron 68TM
        experiment.
        """

        self.summary.clear_all_rows()

        self.data[0].process(
            self._abort_strain_pct,
            self._toughness_strain_pct,
            self._stiffness_strain_pct,
            self._e_modulus_strain1_pct,
            self._e_modulus_strain2_pct,
        )

        self.summary.append_row(
            self.data[0].yield_force_N,
            self.data[0].yield_strain_pct,
            self.data[0].yield_strength_MPa,
            self.data[0].ultimate_force_N,
            self.data[0].ultimate_strain_pct,
            self.data[0].ultimate_strength_MPa,
            self.data[0].e_modulus_MPa,
            self.data[0].toughness_strain_pct,
            self.data[0].toughness_MPa,
            self.data[0].stiffness_strain_pct,
            self.data[0].stiffness_N_mm,
        )


# === Command-line parsers =================================================== #


class Parser(instron_68tm.Parser):
    """
    Parser for the compression-to-failure Instron 68TM experiment.

    Args:
        parsed_arguments: The parsed command-line arguments.
    """

    def __init__(self, parsed_arguments: argparse.Namespace) -> None:

        super().__init__(parsed_arguments)

        self._abort_strain_pct: float = parsed_arguments.abort_strain
        self._toughness_strain_pct: float = parsed_arguments.toughness_strain
        self._stiffness_strain_pct: float = parsed_arguments.stiffness_strain
        self._e_modulus_strain1_pct: float = parsed_arguments.e_modulus_strain1
        self._e_modulus_strain2_pct: float = parsed_arguments.e_modulus_strain2

    def create_analysers(self) -> list[Analyser]:
        """
        Creates the compression-to-failure Instron 68TM experiment analysers
        from the parsed command-line arguments.

        Returns:
            list[Analyser]: List of all compression-to-failure Instron 68TM
                experiment analysers.
        """

        return [
            Analyser(
                input_csv,
                output_xlsx,
                self._abort_strain_pct,
                self._toughness_strain_pct,
                self._stiffness_strain_pct,
                self._e_modulus_strain1_pct,
                self._e_modulus_strain2_pct,
            )
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
            "failure",
            description="Analyses the data from a compression-to-failure "
            "Instron 68TM experiment",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )

        parser.add_argument(  # type: ignore
            "-a",
            "--abort-strain",
            help="The strain at which the experiment aborts even if the sample "
            "has not yet failed",
            type=instrument.ArgparseTypes.percentage_float,
            default=95.0,
        )
        parser.add_argument(  # type: ignore
            "-t",
            "--toughness-strain",
            help="The strain at which the toughness is calculated",
            type=instrument.ArgparseTypes.percentage_float,
            default=4.0,
        )
        parser.add_argument(  # type: ignore
            "-s",
            "--stiffness-strain",
            help="The strain at which the stiffness is calculated",
            type=instrument.ArgparseTypes.percentage_float,
            default=4.0,
        )
        parser.add_argument(  # type: ignore
            "-e",
            "--e-modulus_strain1",
            help="The strain value which defines the first datapoint on the "
            "stress-strain curve used to calculate the Young's modulus.  "
            "It is ε1 in the equation E = (σ2 - σ1) / (ε2 - ε1)",
            type=instrument.ArgparseTypes.percentage_float,
            default=10,
        )
        parser.add_argument(  # type: ignore
            "-f",
            "--e-modulus_strain2",
            help="The strain value which defines the second datapoint on the "
            "stress-strain curve used to calculate the Young's modulus.  "
            "It is ε2 in the equation E = (σ2 - σ1) / (ε2 - ε1)",
            type=instrument.ArgparseTypes.percentage_float,
            default=15,
        )
