import importlib
import mech_analyser.config as ma_config
import mech_analyser.experiment.analyser as ma_analyser
import mech_analyser.experiment.collation as ma_collation
import mech_analyser.experiment.data as ma_data
import mech_analyser.experiment.registry as ma_registry
import mech_analyser.experiment.ui as ma_ui
import mech_analyser.study.sample as ma_sample
import mech_analyser.util.units as ma_units
import mech_analyser.version as ma_version
import re

from PySide6.QtCore import QUrl, Qt
from PySide6.QtGui import QIcon, QDesktopServices
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHeaderView,
    QInputDialog,
    QMainWindow,
    QMessageBox,
    QTableWidgetItem,
    QTreeWidgetItem,
    QWidget,
)
from mech_analyser.ui.window import Ui_MainWindow
from pathlib import Path
from types import ModuleType
from typing import Optional, cast

_EXPERIMENTS: list[dict[str, ModuleType]] = [
    {
        "module": importlib.import_module(module),
        "analyser": importlib.import_module(f"{module}.analyser"),
        "collation": importlib.import_module(f"{module}.collation"),
        "data": importlib.import_module(f"{module}.data"),
        "phase": importlib.import_module(f"{module}.phase"),
        "ui": importlib.import_module(f"{module}.ui"),
    }
    for module in ma_config.EXPERIMENT_MODULES
]


class Window(QMainWindow):
    """
    User interface window for interacting with the application.

    Args:
        icon: The icon to display in the window's title bar.
    """

    def __init__(self, icon: QIcon) -> None:
        super().__init__()

        self._samples: list[ma_sample.Sample] = []
        self._output_directory: Optional[Path] = None
        self._collation_xlsx: Optional[Path] = None
        self._raw_collation: Optional[ma_collation.RawCollation] = None
        self._summary_collation: Optional[ma_collation.SummaryCollation] = None
        self._cancel_flag: bool = False

        # Create the main window
        self._window = Ui_MainWindow()
        self._window.setupUi(self)  # type: ignore
        self.setWindowIcon(icon)
        self._window.a_Version.setText(f"Version: {ma_version.__version__}")

        # Add the experiments to the registry
        self._registry = ma_registry.Registry()
        for e in _EXPERIMENTS:
            # Create the configuration widget
            widget: ma_ui.ConfigWidget = getattr(e["ui"], "ConfigWidget")()
            widget.init()
            self._window.sw_Configuration.addWidget(widget)

            # Create the transcoders
            raw_transcoder: ma_data.RawTranscoder = getattr(e["data"], "RawTranscoder")()
            processed_transcoder: ma_data.ProcessedTranscoder = getattr(
                e["data"],
                "ProcessedTranscoder",
            )()
            summary_transcoder: ma_data.SummaryTranscoder = getattr(
                e["data"],
                "SummaryTranscoder",
            )()
            raw_collation_transcoder: ma_collation.RawTranscoder = getattr(
                e["collation"],
                "RawTranscoder",
            )()
            summary_collation_transcoder: ma_collation.SummaryTranscoder = getattr(
                e["collation"],
                "SummaryTranscoder",
            )()

            # Create the collation types
            summary_collation_type: type[ma_collation.SummaryCollation] = getattr(
                e["collation"],
                "SummaryCollation",
            )

            # Add the experiment to the registry
            self._registry.add(
                ma_registry.Registry.Key(
                    instrument=getattr(e["module"], "INSTRUMENT"),
                    experiment=getattr(e["module"], "EXPERIMENT"),
                ),
                ma_registry.Registry.Value(
                    widget=widget,
                    raw_transcoder=raw_transcoder,
                    processed_transcoder=processed_transcoder,
                    summary_transcoder=summary_transcoder,
                    raw_collation_transcoder=raw_collation_transcoder,
                    summary_collation_transcoder=summary_collation_transcoder,
                    summary_collation_type=summary_collation_type,
                ),
            )

        # Determine the instrument options
        self._window.cb_Instrument.addItems(self._registry.get_instruments())

        # Connect the experiment selection to the configuration view
        self._window.cb_Experiment.currentIndexChanged.connect(
            self._handle_cb_Experiment_changed
        )
        self._window.cb_Instrument.currentIndexChanged.connect(
            self._handle_cb_Instrument_changed
        )

        # Connect the transcoder selection to the stacked widget
        self._window.cb_Transcoder.currentIndexChanged.connect(
            self._handle_cb_Transcoder_changed
        )

        # Connect the menu functionality
        self._window.a_Documentation.triggered.connect(
            self._handle_a_Documentation_triggered
        )
        self._window.a_OpenDirectory.triggered.connect(
            self._handle_a_OpenDirectory_triggered
        )
        self._window.a_OpenCsvs.triggered.connect(self._handle_a_OpenCsvs_triggered)

        # Update the table headers
        self._window.tbl_RawTranscoder.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        self._window.tbl_ProcessedTranscoder.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        self._window.tbl_SummaryTranscoder.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )

        # Connect the table clicked functionality
        self._window.tbl_RawTranscoder.itemClicked.connect(
            self._handle_tbl_RawTranscoder_clicked
        )
        self._window.tbl_SummaryTranscoder.itemClicked.connect(
            self._handle_tbl_SummaryTranscoder_clicked
        )

        # Connect the output tree functionality
        self._window.tree_Output.itemClicked.connect(self._handle_treeOutput_clicked)

        # Connect the button functionalities
        self._window.pb_Clear.clicked.connect(self._handle_pb_Clear_triggered)
        self._window.pb_EditOutput.clicked.connect(self._handle_pb_EditOutput_clicked)
        self._window.pb_EditGroup.clicked.connect(self._handle_pb_EditGroup_clicked)
        self._window.pb_EditSample.clicked.connect(self._handle_pb_EditSample_clicked)
        self._window.pb_SaveAnalysis.clicked.connect(self._handle_pb_SaveAnalysis_clicked)
        self._window.pb_SaveCollation.clicked.connect(
            self._handle_pb_SaveCollation_clicked
        )
        self._window.pb_Cancel.clicked.connect(self._handle_pb_Cancel_clicked)
        self._window.pb_Run.clicked.connect(self._handle_pb_Run_clicked)

        self._reset()

    def _clear_t_Output(self) -> None:
        """
        Clears the tw_Output widget of all contents.
        """

        # Clear the output tree and progress bar
        self._window.tree_Output.clear()
        self._update_pgb_Output()

        # Clear the output viewers
        while self._window.sw_Output.count() > 0:
            widget: ma_ui.QWidget = self._window.sw_Output.widget(0)
            self._window.sw_Output.removeWidget(widget)
            widget.deleteLater()

        # Add a blank output viewer
        self._window.sw_Output.addWidget(QWidget())

    def _create_collator(self) -> ma_collation.Collator:
        """
        Creates the collator for collating the raw data and analysis summaries.

        Returns:
            Collator: The collator for collating the raw data and analysis
                summaries.
        """

        # Obtain the unique sample groups
        groups: list[str] = list(
            {sample.group.name for sample in self._samples if sample.group is not None}
        )

        # Determine the registry key
        key: ma_registry.Registry.Key = ma_registry.Registry.Key(
            instrument=self._window.cb_Instrument.currentText(),
            experiment=self._window.cb_Experiment.currentText(),
        )

        # Create the collations
        raw_collation: ma_collation.RawCollation = self._create_raw_collation(key)
        summary_collations: dict[str, ma_collation.SummaryCollation] = {
            group: self._create_summary_collation(key) for group in groups
        }

        # Create the collator
        return ma_collation.Collator(raw_collation, summary_collations)

    def _create_output_xlsx(self, input_csv: Path) -> Path:
        """
        Creates the Excel output file path from the CSV input file path.

        Args:
            input_csv: Path to the CSV input file.

        Returns:
            Path: Path to the Excel output file.
        """

        output_xlsx: Path = input_csv.with_suffix(".xlsx")
        if self._output_directory is not None:
            output_xlsx = self._output_directory / output_xlsx.name

        return output_xlsx

    def _create_raw_collation(
        self, key: ma_registry.Registry.Key
    ) -> ma_collation.RawCollation:
        """
        Creates the raw collation for collating the raw data.

        Args:
            key: The registry key for the instrument and experiment.

        Returns:
            RawCollation: The collation of the raw data.
        """

        # Obtain the raw collation transcoder
        raw_collation_transcoder: ma_collation.RawTranscoder = (
            self._registry.get_raw_collation_transcoder(key)
        )

        # Clear all existing columns (in case this method is called multiple times)
        raw_collation_transcoder.remove_all_base_columns()

        # Add all raw data columns that are selected for collation
        for row in range(self._window.tbl_RawTranscoder.rowCount()):
            name_item: Optional[QTableWidgetItem]
            collate_item: Optional[QTableWidgetItem]

            # Check if the column is selected for collation
            # NOTE: The "Name" column is column 0 and the "Collate" column is column 8
            name_item = self._window.tbl_RawTranscoder.item(row, 0)  # "Name" column
            collate_item = self._window.tbl_RawTranscoder.item(row, 8)  # "Collate" column
            if (
                name_item is None
                or collate_item is None
                or collate_item.checkState() != Qt.CheckState.Checked
            ):
                continue

            # Add the raw data column as a base column of the raw collation
            raw_collation_transcoder.add_base_column(
                self._registry.get_raw_transcoder(key).columns[name_item.text()]
            )

        # Initialise the columns
        raw_collation_transcoder.init_columns()

        # Create the raw collation
        return ma_collation.RawCollation(raw_collation_transcoder)

    def _create_summary_collation(
        self,
        key: ma_registry.Registry.Key,
    ) -> ma_collation.SummaryCollation:
        """
        Creates the summary collation for collating the analysis summaries.

        Args:
            key: The registry key for the instrument and experiment.

        Returns:
            SummaryCollation: The collation of the analysis summaries.
        """

        # Obtain the summary collation transcoder
        summary_collation_transcoder: ma_collation.SummaryTranscoder = (
            self._registry.get_summary_collation_transcoder(key)
        )

        # Clear all existing columns (in case this method is called multiple times)
        summary_collation_transcoder.remove_all_base_columns()

        # Add all summary columns that are selected for collation
        for row in range(self._window.tbl_SummaryTranscoder.rowCount()):
            name_item: Optional[QTableWidgetItem]
            collate_item: Optional[QTableWidgetItem]

            # Check if the column is selected for collation
            # NOTE: The "Name" column is column 0 and the "Collate" column is column 4
            name_item = self._window.tbl_SummaryTranscoder.item(row, 0)
            collate_item = self._window.tbl_SummaryTranscoder.item(row, 4)
            if (
                name_item is None
                or collate_item is None
                or collate_item.checkState() != Qt.CheckState.Checked
            ):
                continue

            # Add the summary column as a column of the summary collation
            summary_collation_transcoder.add_base_column(
                self._registry.get_summary_transcoder(key).columns[name_item.text()]
            )

        # Initialise the columns
        summary_collation_transcoder.init_columns()

        # Create the summary collation
        return self._registry.get_summary_collation_type(key)(
            summary_collation_transcoder  # type: ignore
        )

    def _handle_a_Documentation_triggered(self) -> None:
        """
        Opens the program documentation.
        """

        QMessageBox.information(
            self,
            "Help",
            "Watch this space... not yet implemented",
            QMessageBox.StandardButton.Ok,
        )

    def _handle_a_OpenCsvs_triggered(self) -> None:
        """
        Opens a file dialog box to search for the CSV experiment outputs and
        then updates the tbl_Files with the selected files.
        """

        # Obtain the CSVs
        input_csvs, _ = QFileDialog.getOpenFileNames(
            self, "Select CSV Files", "", "CSV Files (*.csv)"
        )
        for input_csv in [Path(f) for f in input_csvs]:
            output_xlsx: Path = self._create_output_xlsx(input_csv)
            self._samples.append(
                ma_sample.Sample(
                    name=output_xlsx.stem,
                    input_file=input_csv,
                    output_file=output_xlsx,
                    group=ma_sample.Group(name="All"),
                )
            )

        # Update the GUI
        self._sort_samples()
        self._update_tbl_Files()
        self._update_pgb_Output()
        self._window.tw_Main.setCurrentIndex(0)

    def _handle_a_OpenDirectory_triggered(self) -> None:
        """
        Opens a directory dialog box to search for the CSV experiment outputs
        and then updates the tbl_Files with the selected files.
        """

        # Obtain the input directory
        input_directory: str = QFileDialog.getExistingDirectory(
            self,
            "Select Directory",
            "",
        )
        if input_directory == "":
            return

        # Find all CSVs within the directory
        for input_csv in Path(input_directory).iterdir():
            if not input_csv.is_file() or not input_csv.suffix == ".csv":
                continue

            output_xlsx: Path = self._create_output_xlsx(input_csv)
            self._samples.append(
                ma_sample.Sample(
                    name=output_xlsx.stem,
                    input_file=input_csv,
                    output_file=output_xlsx,
                    group=ma_sample.Group(name="All"),
                )
            )

        # Update the GUI
        self._sort_samples()
        self._update_tbl_Files()
        self._update_pgb_Output()
        self._window.tw_Main.setCurrentIndex(0)

    def _handle_cb_Experiment_changed(self) -> None:
        """
        Activates the configuration widget corresponding to the instrument and
        experiment.
        """

        instrument: str = self._window.cb_Instrument.currentText()
        experiment: str = self._window.cb_Experiment.currentText()

        if not instrument or not experiment:
            return

        key = ma_registry.Registry.Key(instrument, experiment)

        self._registry.get(key).widget.activate(self._window.sw_Configuration)

        self._update_tbl_RawTranscoder(self._registry.get(key).raw_transcoder)
        self._update_tbl_ProcessedTranscoder(self._registry.get(key).processed_transcoder)
        self._update_tbl_SummaryTranscoder(self._registry.get(key).summary_transcoder)

    def _handle_cb_Instrument_changed(self) -> None:
        """
        Updates the experiment selection based on the selected instrument.
        """

        self._window.cb_Experiment.clear()
        self._window.cb_Experiment.addItems(
            self._registry.get_experiments(self._window.cb_Instrument.currentText())
        )

    def _handle_cb_Transcoder_changed(self) -> None:
        """
        Updates the transcoder selection based on the selected instrument and experiment.
        """

        match self._window.cb_Transcoder.currentText():
            case "Raw":
                self._window.sw_Transcoder.setCurrentWidget(self._window.w_RawTranscoder)
            case "Processed":
                self._window.sw_Transcoder.setCurrentWidget(
                    self._window.w_ProcessedTranscoder
                )
            case "Summary":
                self._window.sw_Transcoder.setCurrentWidget(
                    self._window.w_SummaryTranscoder
                )
            case _:
                pass

    def _handle_pb_Cancel_clicked(self) -> None:
        """
        Cancels the running analysis and collation.
        """

        self._cancel_flag = True

    def _handle_pb_Clear_triggered(self) -> None:
        """
        Resets the window.
        """

        self._reset()

    def _handle_pb_EditGroup_clicked(self) -> None:
        """
        Edits the group name of the selected file.
        """

        rows: list[int] = sorted(
            {i.row() for i in self._window.tbl_Files.selectedItems()}
        )

        # Handle invalid selection
        if len(rows) == 0:
            QMessageBox.warning(
                self,
                "Edit group name",
                "No sample has been selected",
                QMessageBox.StandardButton.Ok,
            )
            return

        # Edit the group name
        while True:
            text, ok = QInputDialog.getText(
                self,
                "Edit group name",
                "",
                text=(
                    self._samples[rows[0]].group.name  # type: ignore
                    if self._samples[rows[0]].group
                    else ""
                ),
            )
            if not ok:
                return
            elif not text:
                QMessageBox.warning(
                    self,
                    "Edit group name",
                    "Please enter valid group name",
                    QMessageBox.StandardButton.Ok,
                )
            else:
                break

        # Update the group name
        for i in rows:
            if self._samples[i].group:
                self._samples[i].group.name = text  # type: ignore
            else:
                self._samples[i].group = ma_sample.Group(name=text)

        # Update the GUI
        self._sort_samples()
        self._update_tbl_Files()

    def _handle_pb_EditOutput_clicked(self) -> None:
        """
        Edits the Excel output filename of the selected file.
        """

        rows: list[int] = sorted(
            {i.row() for i in self._window.tbl_Files.selectedItems()}
        )

        # Handle invalid selection
        if len(rows) == 0:
            QMessageBox.warning(
                self,
                "Edit filename",
                "No sample has been selected",
                QMessageBox.StandardButton.Ok,
            )
            return
        elif len(rows) != 1:
            QMessageBox.warning(
                self,
                "Edit filename",
                "Select only one sample",
                QMessageBox.StandardButton.Ok,
            )
            return

        # Edit the filename
        while True:
            text, ok = QInputDialog.getText(
                self,
                "Edit filename",
                "",
                text=self._samples[rows[0]].output_file.stem,
            )
            if not ok:
                return
            elif not text:
                QMessageBox.warning(
                    self,
                    "Edit filename",
                    "Please enter valid filename",
                    QMessageBox.StandardButton.Ok,
                )
            else:
                break

        # Update the filename
        self._samples[rows[0]].output_file = self._samples[rows[0]].output_file.with_stem(
            text
        )

        # Update the GUI
        self._sort_samples()
        self._update_tbl_Files()

    def _handle_pb_EditSample_clicked(self) -> None:
        """
        Edits the sample name of the selected file.
        """

        rows: list[int] = sorted(
            {i.row() for i in self._window.tbl_Files.selectedItems()}
        )

        # Handle invalid selection
        if len(rows) == 0:
            QMessageBox.warning(
                self,
                "Edit sample name",
                "No sample has been selected",
                QMessageBox.StandardButton.Ok,
            )
            return

        # Edit the sample name
        while True:
            text, ok = QInputDialog.getText(
                self,
                "Edit sample name",
                "",
                text=self._samples[rows[0]].name,
            )
            if not ok:
                return
            elif not text:
                QMessageBox.warning(
                    self,
                    "Edit sample name",
                    "Please enter valid sample name",
                    QMessageBox.StandardButton.Ok,
                )
            elif any(
                self._samples[i].name == text
                for i in range(len(self._samples))
                if i not in rows
            ):
                QMessageBox.warning(
                    self,
                    "Edit sample name",
                    "Sample name already exists",
                    QMessageBox.StandardButton.Ok,
                )
            else:
                break

        # Update the sample names
        if len(rows) == 1:
            self._samples[rows[0]].name = text
        else:
            id: int = 1
            for i in rows:
                self._samples[i].name = f"{text}_{id}"
                id += 1

        # Update the GUI
        self._sort_samples()
        self._update_tbl_Files()

    def _handle_pb_Run_clicked(self) -> None:
        """
        Runs the analysis, collates the results, and updates the GUI.
        """

        def reset_buttons() -> None:
            """
            Resets the buttons to their default state.
            """

            self._window.pb_Cancel.setEnabled(False)
            self._window.pb_Run.setEnabled(True)

        # Configure the buttons
        self._window.pb_Cancel.setEnabled(True)
        self._window.pb_Run.setEnabled(False)

        # Configure the progress bar
        self._update_pgb_Output()

        # Force the user to choose the file to which the collation will be saved
        if self._collation_xlsx is None:
            QMessageBox.warning(
                self,
                "Run",
                "Please choose a file to which to save the collation",
                QMessageBox.StandardButton.Ok,
            )
            reset_buttons()
            return

        # Parse the transcoder columns
        try:
            self._parse_transcoder_columns()
        except Exception as e:
            QMessageBox.warning(
                self,
                "Run",
                "Failed to parse transcoder columns:\n" + str(e),
                QMessageBox.StandardButton.Ok,
            )
            reset_buttons()
            return

        # Create all of the analysers
        try:
            key: ma_registry.Registry.Key = ma_registry.Registry.Key(
                instrument=self._window.cb_Instrument.currentText(),
                experiment=self._window.cb_Experiment.currentText(),
            )

            widget: ma_ui.ConfigWidget = self._window.sw_Configuration.currentWidget()  # type: ignore
            widget.sync_parameters()
            for sample in self._samples:
                sample.analyser = widget.create_analyser(
                    sample.input_file,
                    widget.parameters,
                    self._registry.get_raw_transcoder(key),
                    self._registry.get_processed_transcoder(key),
                    self._registry.get_summary_transcoder(key),
                )
        except Exception as e:
            QMessageBox.warning(
                self,
                "Run",
                "Failed to create analyser:\n" + str(e),
                QMessageBox.StandardButton.Ok,
            )
            reset_buttons()
            return

        # Create the collator
        collator: ma_collation.Collator = self._create_collator()

        # Analyse and collate all of the experiments
        self._clear_t_Output()
        for i, sample in enumerate(self._samples):
            # NOTE: annoyingly, this needs to be cast to get rid of the "| None" typing
            analyser: ma_analyser.Analyser = cast(ma_analyser.Analyser, sample.analyser)

            # Create the sample view
            sample_item = QTreeWidgetItem(self._window.tree_Output)
            sample_item.setText(0, sample.output_file.name)
            sample_item.setData(0, Qt.ItemDataRole.UserRole, None)

            # Analyse
            try:
                analyser.analyse()
                analyser.save(sample.output_file)
            except Exception as e:
                QMessageBox.warning(
                    self,
                    "Run",
                    "Failed to analyse:\n" + str(e),
                    QMessageBox.StandardButton.Ok,
                )
                reset_buttons()
                return

            # Collate
            collator.raw_collation.append(analyser.raw_data, sample.name)
            for name, summary_collation in collator.summary_collations.items():
                if sample.group is not None and sample.group.name == name:
                    summary_collation.append(analyser.summary_data, sample.name)
                    break

            # Create the sample summary view
            summary_item = QTreeWidgetItem(sample_item)
            summary_item.setText(0, "Summary")
            summary_widget = ma_ui.TableWidget(
                analyser.summary_data.get_transcoded_frame()
            )
            summary_item.setData(0, Qt.ItemDataRole.UserRole, summary_widget)
            self._window.sw_Output.addWidget(summary_widget)

            # Create the sample raw data plot view
            raw_data_item = QTreeWidgetItem(sample_item)
            raw_data_item.setText(0, "Raw data")
            raw_data_widget = ma_ui.PlotWidget(analyser.raw_data.plot)
            raw_data_item.setData(0, Qt.ItemDataRole.UserRole, raw_data_widget)
            self._window.sw_Output.addWidget(raw_data_widget)

            # Create the sample processed data view
            processed_data_item = QTreeWidgetItem(sample_item)
            processed_data_item.setText(0, "Processed data")
            processed_data_item.setData(0, Qt.ItemDataRole.UserRole, None)

            # Create the individual sample processed data plot views
            for phase in analyser.phases:
                sub_item = QTreeWidgetItem(processed_data_item)
                sub_item.setText(
                    0,
                    phase.processed_data.plot.getPlotItem().titleLabel.text,  # type: ignore
                )
                processed_data_widget = ma_ui.PlotWidget(phase.processed_data.plot)
                sub_item.setData(0, Qt.ItemDataRole.UserRole, processed_data_widget)
                self._window.sw_Output.addWidget(processed_data_widget)

            # Update the GUI
            self._window.tree_Output.scrollToBottom()
            self._update_pgb_Output(i + 1)
            QApplication.processEvents()

            # Cancel the analysis and collation
            if self._cancel_flag:
                self._cancel_flag = False
                reset_buttons()
                return

        # Save the collation
        collator.save(self._collation_xlsx)

        # Configure the buttons
        reset_buttons()

        # Open collation
        reply: QMessageBox.StandardButton = QMessageBox.question(
            None,  # type: ignore
            "Run",
            "Analyis and collation complete! Open collation?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            QDesktopServices.openUrl(
                QUrl.fromLocalFile(str(self._collation_xlsx.parent.absolute()))
            )

    def _handle_pb_SaveAnalysis_clicked(self) -> None:
        """
        Opens a directory dialog box to search for the directory to contain the
        experiment analysis outputs and then updates the tb_SaveAnalysis with
        the selected output directory.
        """

        # Obtain the output directory
        output_directory: str = QFileDialog.getExistingDirectory(
            self,
            "Save analysis to...",
            "",
        )
        if output_directory == "":
            return

        self._output_directory = Path(output_directory)

        # Update the output Excel files of the samples
        for sample in self._samples:
            sample.output_file = self._output_directory / sample.output_file.name

        # Update the GUI
        self._update_tb_SaveAnalysis()

    def _handle_pb_SaveCollation_clicked(self) -> None:
        """
        Opens a save file dialog box to enter the Excel file to which to save
        the collation of the experiment raw data and analysis summaries and then
        updates tb_SaveCollation with the selected Excel file name.
        """

        # Obtain the collation Excel filename
        collation_xlsx, _ = QFileDialog.getSaveFileName(
            self,
            "Save collation to...",
            "Collation.xlsx",
            "Excel Files (*.xlsx);;All Files (*)",
        )
        if collation_xlsx == "":
            return

        self._collation_xlsx = Path(collation_xlsx)

        # Update the GUI
        self._update_tb_SaveCollation()

    def _handle_tbl_RawTranscoder_clicked(self, item: QTableWidgetItem) -> None:
        """
        Toggles the checkbox on the corresponding item in the table.

        Args:
            item: The table item that was clicked.
        """

        # Only toggle the checkbox if the "Collate" item was clicked
        if item.column() != 8:
            return

        item.setCheckState(
            Qt.CheckState.Unchecked
            if item.checkState() == Qt.CheckState.Checked
            else Qt.CheckState.Checked
        )

    def _handle_tbl_SummaryTranscoder_clicked(self, item: QTableWidgetItem) -> None:
        """
        Toggles the checkbox on the corresponding item in the table.

        Args:
            item: The table item that was clicked.
        """

        # Only toggle the checkbox if the "Collate" item was clicked
        if item.column() != 4:
            return

        item.setCheckState(
            Qt.CheckState.Unchecked
            if item.checkState() == Qt.CheckState.Checked
            else Qt.CheckState.Checked
        )

    def _handle_treeOutput_clicked(self, item: QTreeWidgetItem, column: int) -> None:
        """
        Updates the output viewer based on the clicked item.

        Args:
            item: The tree item that was clicked.
            column: The column that was clicked.
        """

        widget: Optional[ma_ui.Widget] = item.data(0, Qt.ItemDataRole.UserRole)

        if widget is None:
            self._window.sw_Output.setCurrentIndex(0)  # NOTE: index of blank widget
            return

        widget.activate(self._window.sw_Output)

    def _parse_transcoder_columns(self) -> None:
        """
        Parses the transcoder columns.
        """

        key: ma_registry.Registry.Key = ma_registry.Registry.Key(
            instrument=self._window.cb_Instrument.currentText(),
            experiment=self._window.cb_Experiment.currentText(),
        )

        # Synchronise the raw transcoder
        for row in range(self._window.tbl_RawTranscoder.rowCount()):
            item: QTableWidgetItem
            column: ma_data.RawTranscoder.Column

            # NOTE: It is known that these items are not None
            item = cast(QTableWidgetItem, self._window.tbl_RawTranscoder.item(row, 0))
            column = self._registry.get_raw_transcoder(key).columns[item.text()]

            # Update the input name
            item = cast(QTableWidgetItem, self._window.tbl_RawTranscoder.item(row, 1))
            column.input_name = item.text()

            # Update the input units
            item = cast(QTableWidgetItem, self._window.tbl_RawTranscoder.item(row, 2))
            column.input_units = ma_units.unit_registry.parse_units(item.text())

            # Update the input header rows
            item = cast(QTableWidgetItem, self._window.tbl_RawTranscoder.item(row, 3))
            column.input_header_rows = [int(i) for i in re.split(r",\s*", item.text())]

            # Update the input header column
            item = cast(QTableWidgetItem, self._window.tbl_RawTranscoder.item(row, 4))
            column.input_header_column = int(item.text())

            # Update the output name
            item = cast(QTableWidgetItem, self._window.tbl_RawTranscoder.item(row, 5))
            column.output_name = item.text()

            # Update the output units
            item = cast(QTableWidgetItem, self._window.tbl_RawTranscoder.item(row, 6))
            column.output_units = ma_units.unit_registry.parse_units(item.text())

            # Update the output header column
            item = cast(QTableWidgetItem, self._window.tbl_RawTranscoder.item(row, 7))
            column.output_header_column = int(item.text())

        # Synchronise the processed transcoder
        for row in range(self._window.tbl_ProcessedTranscoder.rowCount()):
            item: QTableWidgetItem
            column: ma_data.ProcessedTranscoder.Column

            # NOTE: It is known that these items are not None
            item = cast(
                QTableWidgetItem, self._window.tbl_ProcessedTranscoder.item(row, 0)
            )
            column = self._registry.get_processed_transcoder(key).columns[item.text()]

            # Update the output name
            item = cast(
                QTableWidgetItem, self._window.tbl_ProcessedTranscoder.item(row, 1)
            )
            column.output_name = item.text()

            # Update the output units
            item = cast(
                QTableWidgetItem, self._window.tbl_ProcessedTranscoder.item(row, 2)
            )
            column.output_units = ma_units.unit_registry.parse_units(item.text())

            # Update the output header column
            item = cast(
                QTableWidgetItem, self._window.tbl_ProcessedTranscoder.item(row, 3)
            )
            column.output_header_column = int(item.text())

        # Synchronise the summary transcoder
        for row in range(self._window.tbl_SummaryTranscoder.rowCount()):
            item: QTableWidgetItem
            column: ma_data.SummaryTranscoder.Column

            # NOTE: It is known that these items are not None
            item = cast(QTableWidgetItem, self._window.tbl_SummaryTranscoder.item(row, 0))
            column = self._registry.get_summary_transcoder(key).columns[item.text()]

            # Update the output name
            item = cast(QTableWidgetItem, self._window.tbl_SummaryTranscoder.item(row, 1))
            column.output_name = item.text()

            # Update the output units
            item = cast(QTableWidgetItem, self._window.tbl_SummaryTranscoder.item(row, 2))
            column.output_units = ma_units.unit_registry.parse_units(item.text())

            # Update the output header column
            item = cast(QTableWidgetItem, self._window.tbl_SummaryTranscoder.item(row, 3))
            column.output_header_column = int(item.text())

    def _reset(self) -> None:
        """
        Resets the window.
        """

        # Reset the files
        self._samples.clear()
        self._update_tbl_Files()

        # Reset the save locations
        self._output_directory = None
        self._collation_xlsx = None
        self._update_tb_SaveAnalysis()
        self._update_tb_SaveCollation()

        # Reset the collations
        self._raw_collation = None
        self._summary_collation = None

        # Reset the outputs
        self._clear_t_Output()

        # Reset the cancel button
        self._window.pb_Cancel.setEnabled(False)
        self._cancel_flag = False

        # Set the initial drop down menus
        self._handle_cb_Instrument_changed()
        self._handle_cb_Experiment_changed()
        self._handle_cb_Transcoder_changed()

    def _sort_samples(self) -> None:
        """
        Sorts the samples in the summaries table by group name and then sample
        name.
        """

        self._samples.sort(
            key=lambda x: ("" if x.group is None else x.group.name, x.name)
        )

    def _update_pgb_Output(self, value: int = 0) -> None:
        """
        Updates the pgb_Output with the progress of the analysis.

        Args:
            value: Number of samples processed.
        """

        self._window.pgb_Output.setMaximum(len(self._samples))
        self._window.pgb_Output.setValue(value)

    def _update_tb_SaveAnalysis(self) -> None:
        """
        Updates tb_SaveAnalysis with the output directory for the analysis.
        """

        self._window.tb_SaveAnalysis.setText(
            str(self._output_directory) if self._output_directory is not None else ""
        )

    def _update_tb_SaveCollation(self) -> None:
        """
        Updates tb_SaveCollation with the Excel file to which the collation will
        be saved.
        """

        self._window.tb_SaveCollation.setText(
            str(self._collation_xlsx) if self._collation_xlsx is not None else ""
        )

    def _update_tbl_Files(self) -> None:
        """
        Updates the tbl_Files with the sample parameters.
        """

        self._window.tbl_Files.setRowCount(len(self._samples))

        for r in range(self._window.tbl_Files.rowCount()):
            self._window.tbl_Files.setItem(
                r,
                0,
                QTableWidgetItem(self._samples[r].input_file.name),
            )
            self._window.tbl_Files.setItem(
                r,
                1,
                QTableWidgetItem(self._samples[r].output_file.name),
            )
            self._window.tbl_Files.setItem(
                r,
                2,
                QTableWidgetItem(
                    self._samples[r].group.name  # type: ignore
                    if self._samples[r].group
                    else ""
                ),
            )
            self._window.tbl_Files.setItem(r, 3, QTableWidgetItem(self._samples[r].name))

        self._window.tbl_Files.resizeColumnsToContents()
        self._window.tbl_Files.horizontalHeader().setVisible(
            self._window.tbl_Files.rowCount() != 0
        )
        self._window.tbl_Files.clearSelection()

    def _update_tbl_ProcessedTranscoder(
        self, processed_transcoder: ma_data.ProcessedTranscoder
    ) -> None:
        """
        Updates the tbl_ProcessedTranscoder with the processed data transcoder parameters.

        Args:
            processed_transcoder: The processed data transcoder.
        """

        self._window.tbl_ProcessedTranscoder.setRowCount(0)

        for i, column in enumerate(processed_transcoder.columns.values()):
            self._window.tbl_ProcessedTranscoder.insertRow(i)

            # Add the column name
            item = QTableWidgetItem(column.name)
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self._window.tbl_ProcessedTranscoder.setItem(i, 0, item)

            # Add the column output name
            item = QTableWidgetItem(column.output_name)
            self._window.tbl_ProcessedTranscoder.setItem(i, 1, item)

            # Add the column output units
            item = QTableWidgetItem(str(column.output_units))
            self._window.tbl_ProcessedTranscoder.setItem(i, 2, item)

            # Add the column output header column
            item = QTableWidgetItem(str(column.output_header_column))
            self._window.tbl_ProcessedTranscoder.setItem(i, 3, item)

            # Add the collate column
            # NOTE: checking is handled solely within the
            #       _handle_tbl_ProcessedTranscoder_clicked() method
            item = QTableWidgetItem("")
            item.setFlags(
                item.flags()
                & ~(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEditable)
            )
            item.setCheckState(Qt.CheckState.Checked)
            self._window.tbl_ProcessedTranscoder.setItem(i, 4, item)

        self._window.tbl_ProcessedTranscoder.resizeColumnsToContents()

    def _update_tbl_RawTranscoder(self, raw_transcoder: ma_data.RawTranscoder) -> None:
        """
        Updates the tbl_RawTranscoder with the raw data transcoder parameters.

        Args:
            raw_transcoder: The raw data transcoder.
        """

        self._window.tbl_RawTranscoder.setRowCount(0)

        for i, column in enumerate(raw_transcoder.columns.values()):
            self._window.tbl_RawTranscoder.insertRow(i)

            # Add the column name
            item = QTableWidgetItem(column.name)
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self._window.tbl_RawTranscoder.setItem(i, 0, item)

            # Add the column input name
            item = QTableWidgetItem(column.input_name.replace("\n", "\\n"))
            self._window.tbl_RawTranscoder.setItem(i, 1, item)

            # Add the column input units
            item = QTableWidgetItem(str(column.input_units))
            self._window.tbl_RawTranscoder.setItem(i, 2, item)

            # Add the column input header row
            item = QTableWidgetItem(", ".join(str(i) for i in column.input_header_rows))
            self._window.tbl_RawTranscoder.setItem(i, 3, item)

            # Add the column input header column
            item = QTableWidgetItem(str(column.input_header_column))
            self._window.tbl_RawTranscoder.setItem(i, 4, item)

            # Add the column output name
            item = QTableWidgetItem(column.output_name)
            self._window.tbl_RawTranscoder.setItem(i, 5, item)

            # Add the column output units
            item = QTableWidgetItem(str(column.output_units))
            self._window.tbl_RawTranscoder.setItem(i, 6, item)

            # Add the column output header column
            item = QTableWidgetItem(str(column.output_header_column))
            self._window.tbl_RawTranscoder.setItem(i, 7, item)

            # Add the collate column
            # NOTE: checking is handled solely within the
            #       _handle_tbl_RawTranscoder_clicked() method
            item = QTableWidgetItem("")
            item.setFlags(
                item.flags()
                & ~(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEditable)
            )
            item.setCheckState(Qt.CheckState.Checked)
            self._window.tbl_RawTranscoder.setItem(i, 8, item)

    def _update_tbl_SummaryTranscoder(
        self, summary_transcoder: ma_data.SummaryTranscoder
    ) -> None:
        """
        Updates the tbl_SummaryTranscoder with the summary data transcoder parameters.

        Args:
            summary_transcoder: The summary data transcoder.
        """

        self._window.tbl_SummaryTranscoder.setRowCount(0)

        for i, column in enumerate(summary_transcoder.columns.values()):
            self._window.tbl_SummaryTranscoder.insertRow(i)

            # Add the column name
            item = QTableWidgetItem(column.name)
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self._window.tbl_SummaryTranscoder.setItem(i, 0, item)

            # Add the column output name
            item = QTableWidgetItem(column.output_name)
            self._window.tbl_SummaryTranscoder.setItem(i, 1, item)

            # Add the column output units
            item = QTableWidgetItem(str(column.output_units))
            self._window.tbl_SummaryTranscoder.setItem(i, 2, item)

            # Add the column output header column
            item = QTableWidgetItem(str(column.output_header_column))
            self._window.tbl_SummaryTranscoder.setItem(i, 3, item)

            # Add the collate column
            # NOTE: checking is handled solely within the
            #       _handle_tbl_SummaryTranscoder_clicked() method
            item = QTableWidgetItem("")
            item.setFlags(
                item.flags()
                & ~(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEditable)
            )
            item.setCheckState(Qt.CheckState.Checked)
            self._window.tbl_SummaryTranscoder.setItem(i, 4, item)


class Application(QApplication):
    """
    User interface application.
    """

    def __init__(self) -> None:
        super().__init__([])

        window_icon = QIcon(
            str(Path(__file__).resolve().parent / "ui" / "icons" / "MechAnalyser.png")
        )
        self.setWindowIcon(window_icon)

        self._window = Window(window_icon)
        self._window.show()

        self.exec()


if __name__ == "__main__":
    Application()
