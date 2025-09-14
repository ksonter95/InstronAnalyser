import mech_analyser.experiment.instron_68tm.failure.analyser as ma_analyser
import mech_analyser.experiment.instron_68tm.failure.data as ma_data
import mech_analyser.experiment.instron_68tm.failure.phase as ma_phase
import mech_analyser.experiment.instron_68tm.failure.view as view
import mech_analyser.experiment.instron_68tm.ui as ma_ui

from PySide6.QtCore import Qt
from pathlib import Path
from typing import cast


class ConfigWidget(ma_ui.ConfigWidget):
    """
    User interface configuration widget for the compression-to-failure Instron
    68TM experiment.
    """

    def __init__(self) -> None:
        super().__init__(view.Ui_w_Failure(), ma_analyser.Parameters())  # type: ignore

    @property
    def parameters(self) -> ma_analyser.Parameters:
        return cast(ma_analyser.Parameters, self._parameters)

    @property
    def view(self) -> view.Ui_w_Failure:  # type: ignore
        return cast(view.Ui_w_Failure, self._view)

    def create_analyser(
        self,
        input_file: Path,
        parameters: ma_analyser.ma_analyser.ma_analyser.Parameters,
        raw_transcoder: ma_data.ma_data.ma_data.RawTranscoder,
        processed_transcoder: ma_data.ma_data.ma_data.ProcessedTranscoder,
        summary_transcoder: ma_data.ma_data.ma_data.SummaryTranscoder,
    ) -> ma_analyser.Analyser:
        """
        Creates the experiment analyser.

        Args:
            input_file: The path to the CSV file containing the output of the experiment.
            parameters: The parameters to use when analysing the experiment.
            raw_transcoder: The raw data transcoder.
            processed_transcoder: The processed data transcoder.
            summary_transcoder: The summary data transcoder.
        """

        return ma_analyser.Analyser(
            input_file,
            cast(ma_analyser.Parameters, parameters),
            cast(ma_data.ma_data.RawTranscoder, raw_transcoder),
            cast(ma_data.ProcessedTranscoder, processed_transcoder),
            cast(ma_data.SummaryTranscoder, summary_transcoder),
        )

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
            self.parameters.e_modulus_method == ma_phase.Parameters.Method.FIXED_RANGE
        )
        self.view.sb_Strain1.setValue(self.parameters.e_modulus_fixed_strain1_pct)
        self.view.sb_Strain2.setValue(self.parameters.e_modulus_fixed_strain2_pct)
        self.view.rb_AnchorPoint.setChecked(
            self.parameters.e_modulus_method == ma_phase.Parameters.Method.ANCHOR_POINT
        )
        self.view.sb_StrainOffset.setValue(self.parameters.e_modulus_anchor_offset_pct)
        self.view.cbx_AnchorPoint.setCurrentIndex(
            self.parameters.e_modulus_anchor_point.value
        )
        self.view.sb_StrainRangeWidth.setValue(
            self.parameters.e_modulus_anchor_strain_width_pct
        )
        self.view.rb_FindRange.setChecked(
            self.parameters.e_modulus_method == ma_phase.Parameters.Method.FIND_RANGE
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
            self.view.sb_Toughness.value() if self.view.cb_Toughness.isChecked() else None
        )
        self.parameters.e_modulus_method = (
            ma_phase.Parameters.Method.FIXED_RANGE
            if self.view.rb_FixedRange.isChecked()
            else (
                ma_phase.Parameters.Method.ANCHOR_POINT
                if self.view.rb_AnchorPoint.isChecked()
                else ma_phase.Parameters.Method.FIND_RANGE
            )
        )
        self.parameters.e_modulus_fixed_strain1_pct = self.view.sb_Strain1.value()
        self.parameters.e_modulus_fixed_strain2_pct = self.view.sb_Strain2.value()
        self.parameters.e_modulus_anchor_offset_pct = self.view.sb_StrainOffset.value()
        self.parameters.e_modulus_anchor_point = ma_phase.Parameters.AnchorPoint(
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
            ma_phase.Parameters.AnchorPoint.TOE.value,
            Qt.ItemFlag.NoItemFlags,
            Qt.ItemDataRole.UserRole - 1,
        )
        self.view.cbx_AnchorPoint.setItemData(
            ma_phase.Parameters.AnchorPoint.YIELD.value,
            Qt.ItemFlag.NoItemFlags,
            Qt.ItemDataRole.UserRole - 1,
        )
        self.view.cbx_AnchorPoint.setItemData(
            ma_phase.Parameters.AnchorPoint.FAILURE.value,
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
