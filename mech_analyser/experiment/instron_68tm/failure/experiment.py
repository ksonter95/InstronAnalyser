import dataclasses
import enum
import experiment.experiment as experiment
import experiment.instron_68tm.experiment as instron_68tm
import experiment.instron_68tm.failure.view as view
import util.utils as utils

import numpy as np
import pandas as pd

from PySide6.QtCore import Qt
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
        e_modulus_method: Method used to calculate the Young's modulus.
        e_modulus_fixed_strain1_pct: The strain value which defines the first
            datapoint on the stress-strain curve used to calculate the Young's
            modulus.  It is ε1 in the equation E = (σ2 - σ1) / (ε2 - ε1).
        e_modulus_fixed_strain2_pct: The strain value which defines the second
            datapoint on the stress-strain curve used to calculate the Young's
            modulus.  It is ε2 in the equation E = (σ2 - σ1) / (ε2 - ε1).
        e_modulus_anchor_point: The point used to anchor the strain range over
            which the Young's modulus is to be calculated.
        e_modulus_anchor_offset_pct: The strain offset from the specific point
            on the stress-strain curve from/to which the Young's modulus will be
            calculated.  It, in combination with the anchor point, specifies ε1
            in the equation E = (σ2 - σ1) / (ε2 - ε1).
        e_modulus_anchor_strain_width_pct: The width of the range on the
            stress-strain curve over which the Young's modulus will be
            calculated.  It, in combination with the strain offset and anchor
            point, specifies ε2 in the equation E = (σ2 - σ1) / (ε2 - ε1).
        e_modulus_find_strain_min_pct: The strain value which defines the
            minimum strain that can be used to find the best approximation of
            the linear region of the stress-strain curve.
        e_modulus_find_strain_max_pct: The strain value which defines the
            maximum strain that can be used to find the best approximation of
            the linear region of the stress-strain curve.
        e_modulus_find_strain_width_pct: The width of the strain window which
            will be used to find the best approximation of the linear region of
            the stress-strain curve for all possible regions between the minimum
            and maximum strains.
    """

    class AnchorPoint(enum.Enum):
        """
        The point used to anchor the strain range over which the Young's modulus
        is to be calculated.
        """

        START = 0
        TOE = 1
        YIELD = 2
        ULTIMATE = 3
        FAILURE = 4
        END = 5

    class Method(enum.Enum):
        """The method used to calculate the Young's modulus."""

        FIXED_RANGE = 0
        ANCHOR_POINT = 1
        FIND_RANGE = 2

    abort_strain_pct: float = 95.0
    toughness_strain_pct: Optional[float] = None
    e_modulus_method: Method = Method.FIXED_RANGE
    e_modulus_fixed_strain1_pct: float = 10.0
    e_modulus_fixed_strain2_pct: float = 15.0
    e_modulus_anchor_point: AnchorPoint = AnchorPoint.ULTIMATE
    e_modulus_anchor_offset_pct: float = 5.0
    e_modulus_anchor_strain_width_pct: float = 5.0
    e_modulus_find_strain_min_pct: float = 10.0
    e_modulus_find_strain_max_pct: float = 90.0
    e_modulus_find_strain_width_pct: float = 5.0


@dataclasses.dataclass
class AnalyserParameters(instron_68tm.AnalyserParameters):
    """
    Parameters of an analyser of a compression-to-failure experiment using an
    Instron 68TM.

    Args:
        abort_strain_pct: The strain at which the experiment aborts even if the
            sample has not yet failed.
        toughness_strain_pct: The strain at which the toughness is calculated.
            If set to None, the failure or abort strain will be used.
        e_modulus_method: Method used to calculate the Young's modulus.
        e_modulus_fixed_strain1_pct: The strain value which defines the first
            datapoint on the stress-strain curve used to calculate the Young's
            modulus.  It is ε1 in the equation E = (σ2 - σ1) / (ε2 - ε1)
        e_modulus_fixed_strain2_pct: The strain value which defines the second
            datapoint on the stress-strain curve used to calculate the Young's
            modulus.  It is ε2 in the equation E = (σ2 - σ1) / (ε2 - ε1)
        e_modulus_anchor_point: The point used to anchor the strain range over
            which the Young's modulus is to be calculated.
        e_modulus_anchor_offset_pct: The strain offset from the specific point
            on the stress-strain curve from/to which the Young's modulus will be
            calculated.  It, in combination with the anchor point, specifies ε1
            in the equation E = (σ2 - σ1) / (ε2 - ε1).
        e_modulus_anchor_strain_width_pct: The width of the range on the
            stress-strain curve over which the Young's modulus will be
            calculated.  It, in combination with the strain offset and anchor
            point, specifies ε2 in the equation E = (σ2 - σ1) / (ε2 - ε1).
        e_modulus_find_strain_min_pct: The strain value which defines the
            minimum strain that can be used to find the best approximation of
            the linear region of the stress-strain curve.
        e_modulus_find_strain_max_pct: The strain value which defines the
            maximum strain that can be used to find the best approximation of
            the linear region of the stress-strain curve.
        e_modulus_find_strain_width_pct: The width of the strain window which
            will be used to find the best approximation of the linear region of
            the stress-strain curve for all possible regions between the minimum
            and maximum strains.
    """

    abort_strain_pct: float = 95.0
    toughness_strain_pct: Optional[float] = None
    e_modulus_method: DataParameters.Method = DataParameters.Method.FIXED_RANGE
    e_modulus_fixed_strain1_pct: float = 10.0
    e_modulus_fixed_strain2_pct: float = 15.0
    e_modulus_anchor_point: DataParameters.AnchorPoint = (
        DataParameters.AnchorPoint.ULTIMATE
    )
    e_modulus_anchor_offset_pct: float = 5.0
    e_modulus_anchor_strain_width_pct: float = 5.0
    e_modulus_find_strain_min_pct: float = 10.0
    e_modulus_find_strain_max_pct: float = 90.0
    e_modulus_find_strain_width_pct: float = 5.0


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
        self._e_modulus_r2: float = 0.0
        self._e_modulus_strain1_pct: float = 0.0
        self._e_modulus_strain2_pct: float = 0.0
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
    def e_modulus_r2(self) -> float:
        return self._e_modulus_r2

    @property
    def e_modulus_strain1_pct(self) -> float:
        return self._e_modulus_strain1_pct

    @property
    def e_modulus_strain2_pct(self) -> float:
        return self._e_modulus_strain2_pct

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
            - E-modulus coefficient of determination: The R-squared value of
                the linear regression used to determine the E-modulus.
            - E-modulus strains: The strains over which the E-modulus was
                calculated.
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

        # Calculate the summary parameters
        self._ultimate_id = self.processed_frame.stress.idxmax()  # type: ignore
        self._aborted = (
            self.ultimate_strain_pct + self.raw_frame.tare_strain_pct
        ) >= parameters.abort_strain_pct
        self._toughness_id = (
            self._ultimate_id
            if parameters.toughness_strain_pct is None
            else (self.processed_frame.strain - parameters.toughness_strain_pct)
            .abs()
            .idxmin()  # type: ignore
        )
        self._yield_id = 0  # TODO: implement

        # Calculate the parameters of the linear equation that best fits the
        # data points
        match parameters.e_modulus_method:
            # Calculate the E-modulus for the fixed range
            case DataParameters.Method.FIXED_RANGE:
                self._e_modulus_strain1_pct = parameters.e_modulus_fixed_strain1_pct
                self._e_modulus_strain2_pct = parameters.e_modulus_fixed_strain2_pct
                self._e_modulus_MPa, self._e_modulus_r2 = self._execute_regression(
                    self._e_modulus_strain1_pct,
                    self._e_modulus_strain2_pct,
                )

            # Calculate the E-modulus for the range that is anchored to a point
            case DataParameters.Method.ANCHOR_POINT:
                if (
                    parameters.e_modulus_anchor_point
                    == DataParameters.AnchorPoint.START
                ):
                    self._e_modulus_strain1_pct = parameters.e_modulus_anchor_offset_pct
                    self._e_modulus_strain2_pct = (
                        self._e_modulus_strain1_pct
                        + parameters.e_modulus_anchor_strain_width_pct
                    )
                elif (
                    parameters.e_modulus_anchor_point
                    == DataParameters.AnchorPoint.YIELD
                ):
                    self._e_modulus_strain2_pct = (
                        self.yield_strain_pct - parameters.e_modulus_anchor_offset_pct
                    )
                    self._e_modulus_strain1_pct = (
                        self._e_modulus_strain2_pct
                        - parameters.e_modulus_anchor_strain_width_pct
                    )
                elif (
                    parameters.e_modulus_anchor_point
                    == DataParameters.AnchorPoint.ULTIMATE
                ):
                    self._e_modulus_strain2_pct = (
                        self.ultimate_strain_pct
                        - parameters.e_modulus_anchor_offset_pct
                    )
                    self._e_modulus_strain1_pct = (
                        self._e_modulus_strain2_pct
                        - parameters.e_modulus_anchor_strain_width_pct
                    )
                elif (
                    parameters.e_modulus_anchor_point == DataParameters.AnchorPoint.END
                ):
                    self._e_modulus_strain2_pct = (
                        100 - parameters.e_modulus_anchor_offset_pct
                    )
                    self._e_modulus_strain1_pct = (
                        self._e_modulus_strain2_pct
                        - parameters.e_modulus_anchor_strain_width_pct
                    )

                # Ensure that the strains are bounded between 0% and 100%
                self._e_modulus_strain1_pct = max(
                    0, min(100, self._e_modulus_strain1_pct)
                )
                self._e_modulus_strain2_pct = max(
                    0, min(100, self._e_modulus_strain2_pct)
                )

                # Execute the regression
                self._e_modulus_MPa, self._e_modulus_r2 = self._execute_regression(
                    self._e_modulus_strain1_pct,
                    self._e_modulus_strain2_pct,
                )

            # Calculate the E-modulus for all possible windows and save the one
            # with the highest R^2 value
            case DataParameters.Method.FIND_RANGE:
                results: list[tuple[int, int, float, float]] = [
                    (
                        strain_pct,
                        int(strain_pct + parameters.e_modulus_find_strain_width_pct),
                        *self._execute_regression(
                            strain_pct,
                            strain_pct + parameters.e_modulus_find_strain_width_pct,
                        ),
                    )
                    for strain_pct in range(
                        int(parameters.e_modulus_find_strain_min_pct),
                        int(
                            parameters.e_modulus_find_strain_max_pct
                            - parameters.e_modulus_find_strain_width_pct
                            + 1
                        ),
                    )
                    if strain_pct + parameters.e_modulus_find_strain_width_pct
                    < self.ultimate_strain_pct
                ]
                (
                    self._e_modulus_strain1_pct,
                    self._e_modulus_strain2_pct,
                    self._e_modulus_MPa,
                    self._e_modulus_r2,
                ) = max(results, key=lambda x: x[1])

            case _:
                self._e_modulus_strain1_pct = float("NaN")
                self._e_modulus_strain2_pct = float("NaN")
                self._e_modulus_MPa = float("NaN")
                self._e_modulus_r2 = float("NaN")

    def _execute_regression(
        self, strain1_pct: float, strain2_pct: float
    ) -> tuple[float, float]:
        """
        Executes the regression to determine the E-modulus and its corresponding
        coefficient of determination.

        Args:
            strain1_pct: The lower bound of the strain range over which to
                regress.
            strain2_pct: The upper bound of the strain range over which to
                regress.

        Returns:
            Tuple of the E-modulus and its corresponding coefficient of
            determination.
        """

        x: "pd.Series[float]" = (
            self.processed_frame.strain[
                (self.processed_frame.strain > strain1_pct)
                & (self.processed_frame.strain < strain2_pct)
            ]
            # NOTE: convert from percentage to decimal
            / 100.0
        )
        y: "pd.Series[float]" = self.processed_frame.stress[
            (self.processed_frame.strain > strain1_pct)
            & (self.processed_frame.strain < strain2_pct)
        ]

        # Ensure that the regression has more data points than the polynomial
        # degree
        if len(x) < 3:
            return 0.0, 0.0

        [e_modulus_MPa, c], _ = curve_fit(self.y, x, y)  # type: ignore

        e_modulus_r2: float = utils.calculate_r2(
            list(y),
            [self.y(strain_pct, e_modulus_MPa, c) for strain_pct in x],  # type: ignore
        )

        return e_modulus_MPa, e_modulus_r2  # type: ignore

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
                    "E-modulus strain 1 [%]",
                    "E-modulus strain 2 [%]",
                    "E-modulus [MPa]",
                    "E-modulus R^2 [MPa^2/MPa^2]",
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
            data.e_modulus_strain1_pct,
            data.e_modulus_strain2_pct,
            data.e_modulus_MPa,
            data.e_modulus_r2,
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
                self.parameters.e_modulus_method,
                self.parameters.e_modulus_fixed_strain1_pct,
                self.parameters.e_modulus_fixed_strain2_pct,
                self.parameters.e_modulus_anchor_point,
                self.parameters.e_modulus_anchor_offset_pct,
                self.parameters.e_modulus_anchor_strain_width_pct,
                self.parameters.e_modulus_find_strain_min_pct,
                self.parameters.e_modulus_find_strain_max_pct,
                self.parameters.e_modulus_find_strain_width_pct,
            )
            self.data[i].process(parameters)
            self.summary.append_row(self.data[i], parameters)


# === User Interface Widgets ================================================= #


class ConfigWidget(instron_68tm.ConfigWidget):
    """
    User interface configuration widget for the compression-to-failure Instron
    68TM experiment.
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
        Initialises the configuration widget by setting the input fields to the
        defaults of the parameters to use when analysing the experiment and
        connecting any signals with an associated slot.
        """

        # Set the input fields to the defaults
        self.view.sb_Tare.setValue(self.parameters.tare_force_N)
        self.view.sb_Abort.setValue(self.parameters.abort_strain_pct)
        self.view.cb_Toughness.setChecked(
            self.parameters.toughness_strain_pct is not None
        )
        self.view.sb_Toughness.setValue(
            self.parameters.toughness_strain_pct
            if self.parameters.toughness_strain_pct is not None
            else 0.0
        )
        self.view.rb_FixedRange.setChecked(
            self.parameters.e_modulus_method == DataParameters.Method.FIXED_RANGE
        )
        self.view.sb_Strain1.setValue(self.parameters.e_modulus_fixed_strain1_pct)
        self.view.sb_Strain2.setValue(self.parameters.e_modulus_fixed_strain2_pct)
        self.view.rb_AnchorPoint.setChecked(
            self.parameters.e_modulus_method == DataParameters.Method.ANCHOR_POINT
        )
        self.view.sb_StrainOffset.setValue(self.parameters.e_modulus_anchor_offset_pct)
        self.view.cbx_AnchorPoint.setCurrentIndex(
            self.parameters.e_modulus_anchor_point.value
        )
        self.view.sb_StrainRangeWidth.setValue(
            self.parameters.e_modulus_anchor_strain_width_pct
        )
        self.view.rb_FindRange.setChecked(
            self.parameters.e_modulus_method == DataParameters.Method.FIND_RANGE
        )
        self.view.sb_StrainMin.setValue(self.parameters.e_modulus_find_strain_min_pct)
        self.view.sb_StrainMax.setValue(self.parameters.e_modulus_find_strain_max_pct)
        self.view.sb_StrainWindowWidth.setValue(
            self.parameters.e_modulus_find_strain_width_pct
        )

        # Connect signals with slots
        self.view.cb_Toughness.checkStateChanged.connect(
            self._handle_cb_Toughness_changed
        )
        self.view.rb_FixedRange.toggled.connect(self._handle_rb_FixedRange_toggled)
        self.view.rb_AnchorPoint.toggled.connect(self._handle_rb_AnchorPoint_toggled)
        self.view.rb_FindRange.toggled.connect(self._handle_rb_FindRange_toggled)

        # Set initial views
        self._handle_cb_Toughness_changed()
        self._handle_rb_FixedRange_toggled()
        self._handle_rb_AnchorPoint_toggled()
        self._handle_rb_FindRange_toggled()

    def sync_parameters(self) -> None:
        """
        Synchronise the parameters to use when analysing the experiment with the
        configuration widget input fields.
        """

        self.parameters.tare_force_N = self.view.sb_Tare.value()
        self.parameters.abort_strain_pct = self.view.sb_Abort.value()
        self.parameters.toughness_strain_pct = (
            self.view.sb_Toughness.value()
            if self.view.cb_Toughness.isChecked()
            else None
        )
        self.parameters.e_modulus_method = (
            DataParameters.Method.FIXED_RANGE
            if self.view.rb_FixedRange.isChecked()
            else (
                DataParameters.Method.ANCHOR_POINT
                if self.view.rb_AnchorPoint.isChecked()
                else DataParameters.Method.FIND_RANGE
            )
        )
        self.parameters.e_modulus_fixed_strain1_pct = self.view.sb_Strain1.value()
        self.parameters.e_modulus_fixed_strain2_pct = self.view.sb_Strain2.value()
        self.parameters.e_modulus_anchor_offset_pct = self.view.sb_StrainOffset.value()
        self.parameters.e_modulus_anchor_point = DataParameters.AnchorPoint(
            self.view.cbx_AnchorPoint.currentIndex()
        )
        self.parameters.e_modulus_anchor_strain_width_pct = (
            self.view.sb_StrainRangeWidth.value()
        )
        self.parameters.e_modulus_find_strain_min_pct = self.view.sb_StrainMin.value()
        self.parameters.e_modulus_find_strain_max_pct = self.view.sb_StrainMax.value()
        self.parameters.e_modulus_find_strain_width_pct = (
            self.view.sb_StrainWindowWidth.value()
        )

    def _handle_cb_Toughness_changed(self) -> None:
        """
        Enables/disables sb_Toughness.
        """

        self.view.sb_Toughness.setEnabled(self.view.cb_Toughness.isChecked())

    def _handle_rb_AnchorPoint_toggled(self) -> None:
        """
        Enables/disables sb_StrainOffset, l_From, cbx_AnchorPoint, l_With1, and
        sb_StrainRangeWidth.
        """

        self.view.sb_StrainOffset.setEnabled(self.view.rb_AnchorPoint.isChecked())
        self.view.l_From.setEnabled(self.view.rb_AnchorPoint.isChecked())
        self.view.cbx_AnchorPoint.setEnabled(self.view.rb_AnchorPoint.isChecked())
        self.view.l_With1.setEnabled(self.view.rb_AnchorPoint.isChecked())
        self.view.sb_StrainRangeWidth.setEnabled(self.view.rb_AnchorPoint.isChecked())

        # TODO: these can be deleted once the corresponding points are added
        self.view.cbx_AnchorPoint.setItemData(
            DataParameters.AnchorPoint.TOE.value,
            Qt.ItemFlag.NoItemFlags,
            Qt.ItemDataRole.UserRole - 1,
        )
        self.view.cbx_AnchorPoint.setItemData(
            DataParameters.AnchorPoint.YIELD.value,
            Qt.ItemFlag.NoItemFlags,
            Qt.ItemDataRole.UserRole - 1,
        )
        self.view.cbx_AnchorPoint.setItemData(
            DataParameters.AnchorPoint.FAILURE.value,
            Qt.ItemFlag.NoItemFlags,
            Qt.ItemDataRole.UserRole - 1,
        )

    def _handle_rb_FindRange_toggled(self) -> None:
        """
        Enables/disables sb_StrainMin, l_To2, sb_StrainMax, l_Width, and
        sb_StrainWindowWidth.
        """

        self.view.sb_StrainMin.setEnabled(self.view.rb_FindRange.isChecked())
        self.view.l_To2.setEnabled(self.view.rb_FindRange.isChecked())
        self.view.sb_StrainMax.setEnabled(self.view.rb_FindRange.isChecked())
        self.view.l_With2.setEnabled(self.view.rb_FindRange.isChecked())
        self.view.sb_StrainWindowWidth.setEnabled(self.view.rb_FindRange.isChecked())

    def _handle_rb_FixedRange_toggled(self) -> None:
        """
        Enables/disables sb_Strain1, l_To1, and sb_Strain2.
        """

        self.view.sb_Strain1.setEnabled(self.view.rb_FixedRange.isChecked())
        self.view.l_To1.setEnabled(self.view.rb_FixedRange.isChecked())
        self.view.sb_Strain2.setEnabled(self.view.rb_FixedRange.isChecked())
