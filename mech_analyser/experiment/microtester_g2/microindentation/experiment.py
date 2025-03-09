import argparse
import dataclasses
import experiment.experiment as experiment
import experiment.microtester_g2.experiment as microtester_g2
import experiment.microtester_g2.microindentation.view as view
import numpy as np
import pandas as pd

from pathlib import Path
from scipy.optimize import curve_fit  # type: ignore
from typing import Optional

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
        self.indentation_force = pd.Series([0.0] * self._frame.index.size)  # type: ignore
        self.regression_force = pd.Series([0.0] * self._frame.index.size)  # type: ignore
        self.indentation_depth = pd.Series([0.0] * self._frame.index.size)  # type: ignore
        self.h_R = pd.Series([0.0] * self._frame.index.size)  # type: ignore

    @property
    def h_R(self) -> "pd.Series[float]":
        return self._frame["h/R [um/um]"]  # type: ignore

    @h_R.setter
    def h_R(self, value: "pd.Series[float]") -> None:
        self._frame["h/R [um/um]"] = value

        # Move the h/R column to be directly after the indentation depth column
        column: pd.Series = self._frame.pop("h/R [um/um]")  # type: ignore
        self._frame.insert(  # type: ignore
            self._frame.columns.get_loc("Indentation Depth [um]") + 1,  # type: ignore
            "h/R [um/um]",
            column,
        )

    @property
    def indentation_depth(self) -> "pd.Series[float]":
        return self._frame["Indentation Depth [um]"]  # type: ignore

    @indentation_depth.setter
    def indentation_depth(self, value: "pd.Series[float]") -> None:
        self._frame["Indentation Depth [um]"] = value

        # Move the indentation depth column to be directly after the tip
        # displacement column
        column: pd.Series = self._frame.pop("Indentation Depth [um]")  # type: ignore
        self._frame.insert(  # type: ignore
            self._frame.columns.get_loc("Tip Displacement [um]") + 1,  # type: ignore
            "Indentation Depth [um]",
            column,
        )

    @property
    def indentation_force(self) -> "pd.Series[float]":
        return self._frame["Indentation Force [uN]"]  # type: ignore

    @indentation_force.setter
    def indentation_force(self, value: "pd.Series[float]") -> None:
        self._frame["Indentation Force [uN]"] = value

        # Move the indentation force column to be directly after the force column
        column: pd.Series = self._frame.pop("Indentation Force [uN]")  # type: ignore
        self._frame.insert(  # type: ignore
            self._frame.columns.get_loc("Force [uN]") + 1,  # type: ignore
            "Indentation Force [uN]",
            column,
        )

    @property
    def regression_force(self) -> "pd.Series[float]":
        return self._frame["Regression Force [uN]"]  # type: ignore

    @regression_force.setter
    def regression_force(self, value: "pd.Series[float]") -> None:
        self._frame["Regression Force [uN]"] = value

        # Move the regression force column to be directly after the indentation
        # force column
        column: pd.Series = self._frame.pop("Regression Force [uN]")  # type: ignore
        self._frame.insert(  # type: ignore
            self._frame.columns.get_loc("Indentation Force [uN]") + 1,  # type: ignore
            "Regression Force [uN]",
            column,
        )


# === Parameters ============================================================= #


@dataclasses.dataclass
class DataParameters(experiment.DataParameters):
    """
    Parameters of a microindentation experiment using a MicroTester G2.

    Args:
        cycle: Compression/recover cycle number to which the data belongs.
        samples_to_skip: Number of samples at the beginning of the sample data
            to skip.
        R_um: Radius of the spherical indenter.
        v: Poisson's ratio of the sample.  See Bas, Onur, et al. "Rational
            design and fabrication of multiphasic soft network composites for
            tissue engineering articular cartilage: A numerical model-based
            approach." Chemical Engineering Journal 340 (2018): 15-23.
        vi: Poisson's ratio of the indenter.  If None, the indenter is assumed
            to be rigid and will not mechanically deform.
        e_modulus_i_MPa: Young's modulus of the indenter.  If None, the indenter
            is assumed to be rigid and will not mechanically deform.
        h_R_threshold: Threshold for the ratio of the indentation depth to the
            radius of the indenter.  If the ratio is greater than this value,
            then the Hertz model is not a valid approximation of the
            indentation response.
        use_regression_offsets: Include the indentation depth and force offsets
            as regression parameters.  They allow the model to fit the data
            more accurately for cases where the tip displacement does not equal
            the indentation depth and the measured force does not equal the
            indentation force.
        a_max_um: Upper bound for the tip displacement to indentation depth
            offset regression parameter.  If None, `a` can take any value.
        b_max_um: Upper bound for the measured force to indentation force offset
            regression parameter.  If None, `b` can take any value.
    """

    cycle: int = 1
    samples_to_skip: int = 0
    R_um: float = 500.0
    v: float = 0.484
    vi: Optional[float] = None
    e_modulus_i_MPa: Optional[float] = None
    h_R_threshold: float = 0.1
    use_regression_offsets: bool = False
    a_max_um: Optional[float] = None
    b_max_uN: Optional[float] = None


@dataclasses.dataclass
class AnalyserParameters(microtester_g2.experiment.AnalyserParameters):
    """
    Parameters of an analyser of a microindentation experiment using a
    MicroTester G2.

    Args:
        cycles: Number of compression/recover cycles in the experiment.
        samples_to_skip: Number of samples at the beginning of the sample data
            to skip.
        R_um: Radius of the spherical indenter.
        v: Poisson's ratio of the sample.  See Bas, Onur, et al. "Rational
            design and fabrication of multiphasic soft network composites for
            tissue engineering articular cartilage: A numerical model-based
            approach." Chemical Engineering Journal 340 (2018): 15-23.
        vi: Poisson's ratio of the indenter.  If None, the indenter is assumed
            to be rigid and will not mechanically deform.
        e_modulus_i_MPa: Young's modulus of the indenter.  If None, the indenter
            is assumed to be rigid and will not mechanically deform.
        h_R_threshold: Threshold for the ratio of the indentation depth to the
            radius of the indenter.  If the ratio is greater than this value,
            then the Hertz model is not a valid approximation of the
            indentation response.
        use_regression_offsets: Include the indentation depth and force offsets
            as regression parameters.  They allow the model to fit the data
            more accurately for cases where the tip displacement does not equal
            the indentation depth and the measured force does not equal the
            indentation force.
        a_max_um: Upper bound for the tip displacement to indentation depth
            offset regression parameter.  If None, `a` can take any value.
        b_max_um: Upper bound for the measured force to indentation force offset
            regression parameter.  If None, `b` can take any value.
    """

    cycles: int = 3
    samples_to_skip: int = 0
    R_um: float = 500.0
    v: float = 0.484
    vi: Optional[float] = None
    e_modulus_i_MPa: Optional[float] = None
    h_R_threshold: float = 0.1
    use_regression_offsets: bool = False
    a_max_um: Optional[float] = None
    b_max_uN: Optional[float] = None


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

        self._a: float = 0.0
        self._b: float = 0.0
        self._e_modulus_MPa: float = 0.0
        self._e_modulus_reduced_MPa: float = 0.0

    @property
    def a(self) -> float:
        return self._a

    @property
    def b(self) -> float:
        return self._b

    @property
    def e_modulus_MPa(self) -> float:
        return self._e_modulus_MPa

    @property
    def e_modulus_reduced_MPa(self) -> float:
        return self._e_modulus_reduced_MPa

    @property
    def processed_frame(self) -> Frame:
        return super().processed_frame  # type: ignore

    @processed_frame.setter
    def processed_frame(self, value: Frame) -> None:  # type: ignore
        super(Data, Data).processed_frame.__set__(self, value)  # type: ignore

    def process(self, parameters: DataParameters) -> None:  # type: ignore
        """
        Processes the raw data from the microindentation experiment using a
        MicroTester G2.

        Dataset filtering:
            - Compression cycle number of the sample.

        Columns that are populated:
            - Indentation Force: The force applied to indent the sample.
            - Regression Force: Force at each tip displacement point as
                calculated by the Hertz model regression equation of the force.
            - Indentation Depth: The depth of the indentation.
            - h/R: The ratio of the indentation depth to the radius of the
                indenter.

        Summary parameters that are calculated:
            - Hertz model regression equation parameters (E*, a, and b in
                F = 4/3 * (E*) R^0.5 * (h - a)^1.5 + b, where E* is the reduced
                modulus)
            - Young's modulus of the sample.  It is related to the reduced
                modulus according to the equation
                1 / (E*) = (1 - v^2) / E + (1 - vi^2) / Ei, where vi and Ei are
                the poisson's ratio and Young's modulus of the indenter,
                respectively.

        Args:
            parameters: The parameters to use when processing the
                microindentation MicroTester G2 experiment data.
        """

        # Filter the raw data
        self.processed_frame = Frame(
            self.raw_frame.frame[
                (self.raw_frame.cycle == f"{parameters.cycle}-Compress")
                & (
                    self.raw_frame.tip_displacement / parameters.R_um
                    < parameters.h_R_threshold
                )
            ].iloc[parameters.samples_to_skip :],
            f"Cycle = {parameters.cycle}",
        )

        # Calculate the parameters of the Hertz equation that best fits the data
        # points
        try:
            if parameters.use_regression_offsets:
                a_max_um: float = (
                    parameters.a_max_um if parameters.a_max_um is not None else np.inf
                )
                b_max_uN: float = (
                    parameters.b_max_uN if parameters.b_max_uN is not None else np.inf
                )
                [self._e_modulus_reduced_MPa, self._a, self._b], _ = curve_fit(  # type: ignore
                    lambda x, e, a, b: self.y(x, parameters.R_um, e, a, b),  # type: ignore
                    self.processed_frame.tip_displacement,
                    self.processed_frame.force,
                    p0=[
                        1,
                        self.processed_frame.tip_displacement.min(),  # type: ignore
                        self.processed_frame.force.min(),  # type: ignore
                    ],
                    bounds=(
                        (0, -a_max_um, -b_max_uN),
                        (
                            np.inf,
                            self.processed_frame.tip_displacement.min(),  # type: ignore
                            self.processed_frame.force.min(),  # type: ignore
                        ),
                    ),
                )
            else:
                self._a = self.processed_frame.tip_displacement.min()  # type: ignore
                self._b = self.processed_frame.force.iloc[
                    self.processed_frame.tip_displacement.idxmin()  # type: ignore
                ]
                [self._e_modulus_reduced_MPa], _ = curve_fit(  # type: ignore
                    lambda x, e: self.y(x, parameters.R_um, e, self._a, self._b),  # type: ignore
                    self.processed_frame.tip_displacement,
                    self.processed_frame.force,
                )
        except:
            # Solution could not converge
            print("Solution could not converge")
            self._e_modulus_reduced_MPa = float("nan")
            self._a = float("nan")
            self._b = float("nan")

        # Add the indentation force column
        # NOTE: indentation force = force - b
        self.processed_frame.indentation_force = self.processed_frame.force - self.b

        # Add the regression force column
        self.processed_frame.regression_force = pd.Series(
            [
                self.y(
                    x,
                    parameters.R_um,
                    self.e_modulus_reduced_MPa,
                    self.a,
                    self.b,
                ).real  # NOTE: ignore imaginary part
                for x in self.processed_frame.tip_displacement
            ]
        )

        # Add the indentation depth column
        # NOTE: indentation depth = tip displacement - a
        self.processed_frame.indentation_depth = (
            self.processed_frame.tip_displacement - self.a
        )

        # Add the h/R column
        self.processed_frame.h_R = (
            self.processed_frame.indentation_depth / parameters.R_um  # type: ignore
        )

        # Calculate the remaining summary parameters
        vi: float = parameters.vi if parameters.vi is not None else 1.0
        e_modulus_i_MPa: float = (
            parameters.e_modulus_i_MPa
            if parameters.e_modulus_i_MPa is not None
            else 1.0
        )
        self._e_modulus_MPa = (1 - parameters.v**2) / (
            1 / self.e_modulus_reduced_MPa - (1 - vi**2) / e_modulus_i_MPa  # type: ignore
        )

    @staticmethod
    def y(x: float, R: float, e: float, a: float, b: float) -> float:
        """
        Calculates the force according to the following equation:
        y = 4/3 * e * R^0.5 * x^1.5

        Args:
            x: The tip displacement.
            R: The radius of the indenter.
            e: The reduced modulus.
            a: The tip displacement to indentation depth offset.
            b: The measured force to indentation force offset.

        Returns:
            The force at tip displacement x.
        """

        return 4 / 3 * e * (R**0.5) * ((x - a) ** 1.5) + b


# === Results ================================================================ #


class Summary(microtester_g2.Summary):
    """
    Summary of the microindentation MicroTester G2 experiment.
    """

    def __init__(self) -> None:

        super().__init__(
            pd.DataFrame(
                columns=[
                    "Cycle",
                    "Reduced Modulus [MPa]",
                    "E-modulus [MPa]",
                    "a [um]",
                    "b [uN]",
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
            parameters.cycle,
            data.e_modulus_reduced_MPa,
            data.e_modulus_MPa,
            data.a,
            data.b,
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

        for _ in range(parameters.cycles):
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

        # Resize the processed data based on the number of cycles
        if len(self.data) > self.parameters.cycles:
            del self.data[self.parameters.cycles :]
        else:
            self.data.extend(
                [
                    Data(self.raw_frame)
                    for _ in range(self.parameters.cycles - len(self.data))
                ]
            )

        self.summary.clear_all_rows()

        for i in range(len(self.data)):
            parameters = DataParameters(
                i + 1,
                self.parameters.samples_to_skip,
                self.parameters.R_um,
                self.parameters.v,
                self.parameters.vi,
                self.parameters.e_modulus_i_MPa,
                self.parameters.h_R_threshold,
                self.parameters.use_regression_offsets,
                self.parameters.a_max_um,
                self.parameters.b_max_uN,
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
            parsed_arguments.cycles,
            parsed_arguments.samples_to_skip,
            parsed_arguments.radius,
            parsed_arguments.poissons_ratio,
            parsed_arguments.indenter_poissons_ratio,
            parsed_arguments.indenter_e_modulus,
            parsed_arguments.h_r_threshold,
            parsed_arguments.use_regression_offsets,
            parsed_arguments.a_max,
            parsed_arguments.b_max,
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

        parser.add_argument(  # type: ignore
            "-n",
            "--cycles",
            help="Number of compression/recover cycles in the experiment",
            type=experiment.ArgparseTypes.positive_non_zero_integer,
            default=3,
        )
        parser.add_argument(  # type: ignore
            "-s",
            "--samples-to-skip",
            help="Number of samples at the beginning of the sample data to skip",
            type=experiment.ArgparseTypes.positive_integer,
            default=1,
        )
        parser.add_argument(  # type: ignore
            "-r",
            "--radius",
            help="Radius of the spherical indenter (in um)",
            type=experiment.ArgparseTypes.positive_non_zero_integer,
            default=500,
        )
        parser.add_argument(  # type: ignore
            "-v",
            "--poissons-ratio",
            help="Poisson's ratio of the sample.  See Bas, Onur, et al. "
            "'Rational design and fabrication of multiphasic soft network "
            "composites for tissue engineering articular cartilage: A "
            "numerical model-based approach.' Chemical Engineering Journal 340 "
            "(2018): 15-23",
            type=experiment.ArgparseTypes.poisson_float,
            default=0.484,
        )
        parser.add_argument(  # type: ignore
            "-i",
            "--indenter-poissons-ratio",
            help="Poisson's ratio of the indenter.  If None, the indenter is "
            "assumed to be rigid and will not mechanically deform",
            type=experiment.ArgparseTypes.poisson_float,
            default=None,
        )
        parser.add_argument(  # type: ignore
            "-e",
            "--indenter-e-modulus",
            help="Young's modulus of the indenter.  If None, the indenter is "
            "assumed to be rigid and will not mechanically deform",
            type=experiment.ArgparseTypes.positive_non_zero_float,
            default=None,
        )
        parser.add_argument(  # type: ignore
            "-t",
            "--h-r-threshold",
            help="Threshold for the ratio of the indentation depth to the "
            "radius of the indenter.  If the ratio is greater than this value, "
            "then the Hertz model is not a valid approximation of the "
            "indentation response",
            type=experiment.ArgparseTypes.positive_non_zero_float,
            default=0.1,
        )
        parser.add_argument(  # type: ignore
            "-u",
            "--use-regression-offsets",
            help="Include the indentation depth and force offsets as "
            "regression parameters.  They allow the model to fit the data more "
            "accurately for cases where the tip displacement does not equal "
            "the indentation depth and the measured force does not equal the "
            "indentation force.",
            action="store_true",
        )
        parser.add_argument(  # type: ignore
            "-a",
            "--a-max",
            help="Upper bound for the tip displacement to indentation depth "
            "offset regression parameter.  If None, `a` can take any value",
            type=experiment.ArgparseTypes.positive_non_zero_float,
            default=None,
        )
        parser.add_argument(  # type: ignore
            "-b",
            "--b-max",
            help="Upper bound for the measured force to indentation force "
            "offset regression parameter.  If None, `b` can take any value",
            type=experiment.ArgparseTypes.positive_non_zero_float,
            default=None,
        )


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
        self.view.sb_Cycles.setValue(self.parameters.cycles)
        self.view.sb_SamplesToSkip.setValue(self.parameters.samples_to_skip)
        self.view.sb_IndenterRadius.setValue(self.parameters.R_um)
        self.view.sb_PoissonsRatio.setValue(self.parameters.v)
        self.view.sb_HRThreshold.setValue(self.parameters.h_R_threshold)
        self.view.cb_IndenterProperties.setChecked(
            self.parameters.vi is not None
            and self.parameters.e_modulus_i_MPa is not None
        )
        self.view.sb_IndenterPoissonsRatio.setValue(self.parameters.vi or 0.0)
        self.view.sb_IndenterYoungsModulus.setValue(
            self.parameters.e_modulus_i_MPa or 0.0
        )
        self.view.cb_RegressionOffsets.setChecked(
            self.parameters.use_regression_offsets
        )
        self.view.cb_OffsetBounds.setChecked(
            self.parameters.use_regression_offsets
            and self.parameters.a_max_um is not None
            and self.parameters.b_max_uN is not None
        )
        self.view.sb_OffsetTipDisplacement.setValue(self.parameters.a_max_um or 0.0)
        self.view.sb_OffsetForce.setValue(self.parameters.b_max_uN or 0.0)

        # Connect signals with slots
        self.view.cb_IndenterProperties.checkStateChanged.connect(
            self._handle_cb_IndenterProperties_changed
        )
        self.view.cb_RegressionOffsets.checkStateChanged.connect(
            self._handle_cb_RegressionOffsets_changed
        )
        self.view.cb_OffsetBounds.checkStateChanged.connect(
            self._handle_cb_OffsetBounds_changed
        )

        # Set initial views
        self._handle_cb_IndenterProperties_changed()
        self._handle_cb_RegressionOffsets_changed()
        self._handle_cb_OffsetBounds_changed()

    def sync_parameters(self) -> None:
        """
        Synchronise the parameters to use when analysing the experiment with the
        widget input fields.
        """

        self.parameters.cycles = self.view.sb_Cycles.value()
        self.parameters.samples_to_skip = self.view.sb_SamplesToSkip.value()
        self.parameters.R_um = self.view.sb_IndenterRadius.value()
        self.parameters.v = self.view.sb_PoissonsRatio.value()
        self.parameters.h_R_threshold = self.view.sb_HRThreshold.value()
        self.parameters.vi = (
            self.view.sb_IndenterPoissonsRatio.value()
            if self.view.cb_IndenterProperties.isChecked()
            else None
        )
        self.parameters.e_modulus_i_MPa = (
            self.view.sb_IndenterYoungsModulus.value()
            if self.view.cb_IndenterProperties.isChecked()
            else None
        )
        self.parameters.use_regression_offsets = (
            self.view.cb_RegressionOffsets.isChecked()
        )
        self.parameters.a_max_um = (
            self.view.sb_OffsetTipDisplacement.value()
            if self.view.cb_RegressionOffsets.isChecked()
            and self.view.cb_OffsetBounds.isChecked()
            else None
        )
        self.parameters.b_max_uN = (
            self.view.sb_OffsetForce.value()
            if self.view.cb_RegressionOffsets.isChecked()
            and self.view.cb_OffsetBounds.isChecked()
            else None
        )

    def _handle_cb_IndenterProperties_changed(self) -> None:
        """
        Sets the visibility of sb_IndenterPoissonsRatio and
        sb_IndenterYoungsModulus to the state of cb_IndenterProperties.
        """

        self.view.l_IndenterPoissonsRatio.setDisabled(
            not self.view.cb_IndenterProperties.isChecked()
        )
        self.view.l_IndenterYoungsModulus.setDisabled(
            not self.view.cb_IndenterProperties.isChecked()
        )
        self.view.sb_IndenterPoissonsRatio.setDisabled(
            not self.view.cb_IndenterProperties.isChecked()
        )
        self.view.sb_IndenterYoungsModulus.setDisabled(
            not self.view.cb_IndenterProperties.isChecked()
        )

    def _handle_cb_OffsetBounds_changed(self) -> None:
        """
        Sets the visibility of sb_OffsetTipDisplacement and sb_OffsetForce to
        the state of cb_RegressionOffsets and cb_OffsetBounds.
        """

        self.view.l_OffsetTipDisplacement.setDisabled(
            not self.view.cb_RegressionOffsets.isChecked()
            or not self.view.cb_OffsetBounds.isChecked()
        )
        self.view.l_OffsetForce.setDisabled(
            not self.view.cb_RegressionOffsets.isChecked()
            or not self.view.cb_OffsetBounds.isChecked()
        )
        self.view.sb_OffsetTipDisplacement.setDisabled(
            not self.view.cb_RegressionOffsets.isChecked()
            or not self.view.cb_OffsetBounds.isChecked()
        )
        self.view.sb_OffsetForce.setDisabled(
            not self.view.cb_RegressionOffsets.isChecked()
            or not self.view.cb_OffsetBounds.isChecked()
        )

    def _handle_cb_RegressionOffsets_changed(self) -> None:
        """
        Sets the visibility of cb_OffsetBounds to the state of
        cb_RegressionOffsets and sets the visibility of sb_OffsetTipDisplacement
        and sb_OffsetForce to the state of cb_RegressionOffsets and
        cb_OffsetBounds.
        """

        self.view.cb_OffsetBounds.setDisabled(
            not self.view.cb_RegressionOffsets.isChecked()
        )
        self.view.l_OffsetTipDisplacement.setDisabled(
            not self.view.cb_RegressionOffsets.isChecked()
            or not self.view.cb_OffsetBounds.isChecked()
        )
        self.view.l_OffsetForce.setDisabled(
            not self.view.cb_RegressionOffsets.isChecked()
            or not self.view.cb_OffsetBounds.isChecked()
        )
        self.view.sb_OffsetTipDisplacement.setDisabled(
            not self.view.cb_RegressionOffsets.isChecked()
            or not self.view.cb_OffsetBounds.isChecked()
        )
        self.view.sb_OffsetForce.setDisabled(
            not self.view.cb_RegressionOffsets.isChecked()
            or not self.view.cb_OffsetBounds.isChecked()
        )
