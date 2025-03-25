import experiment.experiment as experiment
import importlib
import os

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QInputDialog,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QTableWidgetItem,
)
from PySide6.QtCore import Qt
from pathlib import Path
from typing import Optional
from ui.window import Ui_MainWindow


_EXPERIMENTS_DIR: str = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "experiment")
)
_EXPERIMENTS = [
    importlib.import_module(f"experiment.{d1}.{d2}.experiment")
    for d1 in os.listdir(_EXPERIMENTS_DIR)
    if os.path.isdir(os.path.join(_EXPERIMENTS_DIR, d1))
    for d2 in os.listdir(os.path.join(_EXPERIMENTS_DIR, d1))
    if os.path.isdir(os.path.join(_EXPERIMENTS_DIR, d1, d2))
    and os.path.exists(os.path.join(_EXPERIMENTS_DIR, d1, d2, "experiment.py"))
]


class Sample(object):
    """
    Data storage object for all properties of an experiment sample.

    Args:

    """

    def __init__(self, input_csv: Path, output_xlsx: Path) -> None:

        self._input_csv: Path = input_csv
        self._output_xlsx: Path = output_xlsx
        self._analyser: Optional[experiment.Analyser] = None
        self._name: str
        self._sheet: str

        self.set_to_default()

    @property
    def analyser(self) -> experiment.Analyser:
        if self._analyser is None:
            raise ValueError("Analyser not set")

        return self._analyser

    @analyser.setter
    def analyser(self, value: experiment.Analyser) -> None:
        self._analyser = value

    @property
    def input_csv(self) -> Path:
        return self._input_csv

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def output_xlsx(self) -> Path:
        return self._output_xlsx

    @output_xlsx.setter
    def output_xlsx(self, value: Path) -> None:
        self._output_xlsx = value

    @property
    def sheet(self) -> str:
        return self._sheet

    @sheet.setter
    def sheet(self, value: str) -> None:
        self._sheet = value

    def set_to_default(self) -> None:
        """
        Resets all sample parameters to their default.
        """

        self._name = self.output_xlsx.stem
        self._sheet = "Summary"


class WidgetManager:
    """
    Class for managing the experiment widgets.
    """

    def __init__(self) -> None:
        self._widgets: list[experiment.Widget] = []

    def add(self, widget: experiment.Widget) -> None:
        """
        Adds the widget to the list of managed widgets.

        Args:
            widget: Widget to be added to the list of managed widgets.
        """

        if widget not in self._widgets:
            self._widgets.append(widget)

    def get(self, instrument: str, experiment: str) -> Optional[experiment.Widget]:
        """
        Obtains the widget associated with the specified instrument and
        experiment.

        Args:
            instrument: Instrument for which to obtain the widget.
            experiment: Experiment for which to obtain the widget.

        Raises:
            KeyError: If no widget is associated with the specified instrument
            and experiment.

        Returns:
            Widget: The widget associated with the specified instrument and
                experiment.
            None: If no widget is associated with the specified instrument and
                experiment.
        """

        for widget in self._widgets:
            if widget.instrument == instrument and widget.experiment == experiment:
                return widget

        return None

    def get_experiments(self, instrument: str) -> list[str]:
        """
        Obtains the list of experiments associated with the specified
        instrument.

        Args:
            instrument: The instrument for which to obtain the list of
                associated experiments.

        Returns:
            list[str]: A list of experiments associated with the specified
                instrument.
        """

        experiments: list[str] = [
            w.experiment for w in self._widgets if w.instrument == instrument
        ]
        experiments.sort()

        return experiments

    def get_instruments(self) -> list[str]:
        """
        Obtains the list of recognised instruments.

        Returns:
            list[str]: The list of recognised instruments.
        """

        instruments: list[str] = list(set([w.instrument for w in self._widgets]))
        instruments.sort()

        return instruments


class Window(QMainWindow):
    """
    User interface window for interacting with the application.
    """

    def __init__(self) -> None:
        super().__init__()

        self._samples: list[Sample] = []
        self._output_directory: Optional[Path] = None
        self._raw_collation: Optional[experiment.RawCollation] = None
        self._summary_collation: Optional[experiment.SummaryCollation] = None

        # Create the main window
        self._window = Ui_MainWindow()
        self._window.setupUi(self)  # type: ignore
        self.setWindowIcon(QIcon("ui/MechAnalyser.png"))

        # Create the widget and the widget manager
        self._widget_manager = WidgetManager()
        for e in _EXPERIMENTS:
            widget: experiment.Widget = getattr(e, "Widget")()
            widget.init()
            self._window.sw_Configuration.addWidget(widget)
            self._widget_manager.add(widget)

        # Determine the instrument options
        self._window.cb_Instrument.addItems(self._widget_manager.get_instruments())

        # Connect the experiment selection to the configuration view
        self._window.cb_Experiment.currentIndexChanged.connect(
            self._handle_cb_Experiment_changed
        )
        self._window.cb_Instrument.currentIndexChanged.connect(
            self._handle_cb_Instrument_changed
        )

        # Connect the button functionalities
        self._window.cb_All.checkStateChanged.connect(self._handle_cb_All_changed)
        self._window.pb_Clear.clicked.connect(self._handle_pb_Clear_clicked)
        self._window.pb_Collate.clicked.connect(self._handle_pb_Collate_clicked)
        self._window.pb_Configuration.clicked.connect(
            self._handle_pb_Configuration_clicked
        )
        self._window.pb_Continue.clicked.connect(self._handle_pb_Continue_clicked)
        self._window.pb_EditSample.clicked.connect((self._handle_pb_EditSample_clicked))
        self._window.pb_EditSheet.clicked.connect((self._handle_pb_EditSheet_clicked))
        self._window.pb_OpenCsv.clicked.connect(self._handle_pb_OpenCsv_clicked)
        self._window.pb_OpenDirectory.clicked.connect(
            self._handle_pb_OpenDirectory_clicked
        )
        self._window.pb_Run.clicked.connect(self._handle_pb_Run_clicked)
        self._window.pb_SaveDirectory.clicked.connect(
            self._handle_pb_SaveDirectory_clicked
        )

        self._reset()

    def _create_output_xlsx(self, input_csv: Path) -> Path:
        """
        Creates the Excel output file path from the CSV input file path.

        Args:
            input_csv: Path to the CSV input file.

        Returns:
            Path: Path to the Excel output file.
        """

        output_xlsx: Path = input_csv.with_suffix(".xlsx")
        if self._window.cb_All.isChecked() and self._output_directory is not None:
            output_xlsx = self._output_directory / output_xlsx.name

        return output_xlsx

    def _handle_cb_All_changed(self) -> None:
        """
        Updates the output directory path of the Excel files.
        """

        for sample in self._samples:
            sample.output_xlsx = self._create_output_xlsx(sample.input_csv)

        self._update_tbl_Files()

    def _handle_cb_Experiment_changed(self) -> None:
        """
        Activates the widget corresponding to the instrument and experiment.
        """

        widget: Optional[experiment.Widget] = self._widget_manager.get(
            self._window.cb_Instrument.currentText(),
            self._window.cb_Experiment.currentText(),
        )

        if widget is not None:
            widget.activate(self._window.sw_Configuration)

    def _handle_cb_Instrument_changed(self) -> None:
        """
        Updates the experiment selection based on the selected instrument.
        """

        self._window.cb_Experiment.clear()
        self._window.cb_Experiment.addItems(
            self._widget_manager.get_experiments(
                self._window.cb_Instrument.currentText()
            )
        )

    def _handle_pb_Clear_clicked(self) -> None:
        """
        Resets the window.
        """

        self._reset()

    def _handle_pb_Collate_clicked(self) -> None:
        """
        Collates all of the experiment raw data and summaries into one Excel
        file.
        """

        raw_collation = experiment.RawCollation(
            [
                self._window.lst_RawData.item(i).text()
                for i in range(self._window.lst_RawData.count())
                if self._window.lst_RawData.item(i).checkState()
                == Qt.CheckState.Checked
            ]
        )
        summary_collations = [
            experiment.SummaryCollation(sheet)
            for sheet in list({sample.sheet for sample in self._samples})
        ]

        for sample in self._samples:
            raw_collation.append(sample.analyser.raw_frame, sample.name)
            for summary_collation in summary_collations:
                if sample.sheet == summary_collation.sheet_name:
                    summary_collation.append(sample.analyser.summary, sample.name)
                    break

        collator = experiment.Collator(
            self._output_directory / f"{self._window.le_CollationFilename.text()}.xlsx",  # type: ignore
            raw_collation,
            summary_collations,
        )

        collator.save()

        self._reset()

    def _handle_pb_Configuration_clicked(self) -> None:
        """
        Enables the configuration tab and sets it as the current tab.
        """

        if self._output_directory is None:
            QMessageBox.warning(
                self,
                "Configuration",
                "Please choose output directory",
                QMessageBox.StandardButton.Ok,
            )
            return

        self._window.tw_Main.setTabEnabled(1, True)
        self._window.tw_Main.setCurrentIndex(1)

    def _handle_pb_Continue_clicked(self) -> None:
        """
        Enables the collation tab.
        """

        self._window.tw_Main.setTabEnabled(2, False)
        self._window.tw_Main.setTabEnabled(3, True)
        self._window.tw_Main.setCurrentIndex(3)
        self._update_lst_RawData()
        self._update_tbl_Summaries()

    def _handle_pb_EditSample_clicked(self) -> None:
        """
        Edits the sample name of the selected file.
        """

        rows: list[int] = sorted(
            {i.row() for i in self._window.tbl_Summaries.selectedItems()}
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

        self._sort_samples()
        self._update_tbl_Summaries()

    def _handle_pb_EditSheet_clicked(self) -> None:
        """
        Edits the sheet name of the selected file.
        """

        rows: list[int] = sorted(
            {i.row() for i in self._window.tbl_Summaries.selectedItems()}
        )

        # Handle invalid selection
        if len(rows) == 0:
            QMessageBox.warning(
                self,
                "Edit sheet name",
                "No sample has been selected",
                QMessageBox.StandardButton.Ok,
            )
            return

        # Edit the sheet name
        while True:
            text, ok = QInputDialog.getText(
                self,
                "Edit sheet name",
                "",
                text=self._samples[rows[0]].sheet,
            )
            if not ok:
                return
            elif not text:
                QMessageBox.warning(
                    self,
                    "Edit sheet name",
                    "Please enter valid sheet name",
                    QMessageBox.StandardButton.Ok,
                )
            else:
                break

        # Update the sheet name
        for i in rows:
            self._samples[i].sheet = text

        self._sort_samples()
        self._update_tbl_Summaries()

    def _handle_pb_OpenCsv_clicked(self) -> None:
        """
        Opens a file dialog box to search for the CSV experiment outputs and
        then updates the tbl_Files with the selected files.
        """

        input_csvs, _ = QFileDialog.getOpenFileNames(
            self, "Select CSV Files", "", "CSV Files (*.csv);;All Files (*)"
        )

        for input_csv in [Path(f) for f in input_csvs]:
            self._samples.append(Sample(input_csv, self._create_output_xlsx(input_csv)))

        self._sort_samples()
        self._update_tbl_Files()

    def _handle_pb_OpenDirectory_clicked(self) -> None:
        """
        Opens a directory dialog box to search for the CSV experiment outputs
        and then updates the tbl_Files with the selected files.
        """

        input_directory: Path = Path(
            QFileDialog.getExistingDirectory(self, "Select Directory", "")
        )

        for input_csv in input_directory.iterdir():
            if not input_csv.is_file() or not input_csv.suffix == ".csv":
                continue

            self._samples.append(Sample(input_csv, self._create_output_xlsx(input_csv)))

        self._sort_samples()
        self._update_tbl_Files()

    def _handle_pb_Run_clicked(self) -> None:
        """
        Enables the output tab, sets it as the current tab, and begins the
        analysis.
        """

        # Enable the output tab and set it to be the current tab
        self._window.tw_Main.setTabEnabled(0, False)
        self._window.tw_Main.setTabEnabled(1, False)
        self._window.tw_Main.setTabEnabled(2, True)
        self._window.tw_Main.setCurrentIndex(2)

        # Create all of the analysers
        widget: experiment.Widget = self._window.sw_Configuration.currentWidget()  # type: ignore
        widget.sync_parameters()
        for sample in self._samples:
            sample.analyser = widget.create_analyser(
                sample.input_csv, sample.output_xlsx, widget.parameters
            )

        # Analyse all of the experiments
        for i in range(self._window.tbl_Files.rowCount()):
            self._window.tbl_Output.setRowCount(i + 1)
            self._window.tbl_Output.setItem(
                i,
                0,
                QTableWidgetItem(
                    f"{i + 1}/{len(self._samples)}: {self._samples[i].output_xlsx.name}"
                ),
            )
            self._window.tbl_Output.scrollToBottom()
            QApplication.processEvents()

            self._samples[i].analyser.analyse()
            self._samples[i].analyser.save()

        self._window.pb_Continue.setEnabled(True)

    def _handle_pb_SaveDirectory_clicked(self) -> None:
        """
        Opens a directory dialog box to search for the directory to contain the
        experiment analysis outputs and then updates the tbl_Files with the
        selected output directory.
        """

        self._output_directory = Path(
            QFileDialog.getExistingDirectory(self, "Select Directory", "")
        )

        for sample in self._samples:
            sample.output_xlsx = self._create_output_xlsx(sample.input_csv)

        self._update_tbl_Files()
        self._window.tb_SaveDirectory.setText(str(self._output_directory))

    def _reset(self) -> None:
        """
        Resets the window.
        """

        # Initially disable the configuration and output tabs
        self._window.tw_Main.setTabEnabled(0, True)
        self._window.tw_Main.setTabEnabled(1, False)
        self._window.tw_Main.setTabEnabled(2, False)
        self._window.tw_Main.setTabEnabled(3, False)

        # Reset the files
        self._samples.clear()
        self._output_directory = None
        self._update_tbl_Files()

        # Reset the collations
        self._window.le_CollationFilename.setText("Summary")
        self._raw_collation = None
        self._summary_collation = None

        # Set the initial instrument and experiment drop down menus
        self._handle_cb_Instrument_changed()
        self._handle_cb_Experiment_changed()

        # Disable the continue button
        self._window.pb_Continue.setEnabled(False)

    def _sort_samples(self) -> None:
        """
        Sorts the samples in the summaries table by sheet name and then sample
        name.
        """

        self._samples.sort(key=lambda x: (x.sheet, x.name))

    def _update_lst_RawData(self) -> None:
        """
        Updates the raw data list view.
        """

        for column in self._samples[0].analyser.raw_frame.columns:
            item = QListWidgetItem(column)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Checked)
            self._window.lst_RawData.addItem(item)

    def _update_tbl_Files(self) -> None:
        """
        Updates the files table.
        """

        self._window.tbl_Files.setRowCount(len(self._samples))

        for r in range(self._window.tbl_Files.rowCount()):
            self._window.tbl_Files.setItem(
                r, 0, QTableWidgetItem(self._samples[r].input_csv.stem)
            )
            self._window.tbl_Files.setItem(
                r, 1, QTableWidgetItem(str(self._samples[r].input_csv))
            )
            self._window.tbl_Files.setItem(
                r, 2, QTableWidgetItem(str(self._samples[r].output_xlsx))
            )

        self._window.tbl_Files.resizeColumnsToContents()
        self._window.tbl_Files.horizontalHeader().setVisible(
            self._window.tbl_Files.rowCount() != 0
        )

    def _update_tbl_Summaries(self) -> None:
        """
        Updates the summaries table.
        """

        self._window.tbl_Summaries.setRowCount(len(self._samples))

        for r in range(self._window.tbl_Summaries.rowCount()):
            self._window.tbl_Summaries.setItem(
                r, 0, QTableWidgetItem(self._samples[r].input_csv.name)
            )
            self._window.tbl_Summaries.setItem(
                r, 1, QTableWidgetItem(self._samples[r].sheet)
            )
            self._window.tbl_Summaries.setItem(
                r, 2, QTableWidgetItem(self._samples[r].name)
            )

        self._window.tbl_Summaries.resizeColumnsToContents()
        self._window.tbl_Summaries.horizontalHeader().setVisible(
            self._window.tbl_Summaries.rowCount() != 0
        )
        self._window.tbl_Summaries.clearSelection()


class Application(QApplication):
    """
    User interface application.
    """

    def __init__(self) -> None:
        super().__init__([])

        self._window = Window()
        self._window.show()

        self.exec()


if __name__ == "__main__":
    Application()
