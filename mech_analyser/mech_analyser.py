import experiment.experiment as experiment
import importlib
import os

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QTableWidgetItem,
)
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

        self._files: list[tuple[Path, Path]] = []
        self._output_directory: Optional[Path] = None

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
        self._window.pb_OpenDirectory.clicked.connect(
            self._handle_pb_OpenDirectory_clicked
        )
        self._window.pb_OpenCsv.clicked.connect(self._handle_pb_OpenCsv_clicked)
        self._window.pb_SaveDirectory.clicked.connect(
            self._handle_pb_SaveDirectory_clicked
        )
        self._window.pb_Configuration.clicked.connect(
            self._handle_pb_Configuration_clicked
        )
        self._window.pb_Run.clicked.connect(self._handle_pb_Run_clicked)
        self._window.pb_Continue.clicked.connect(self._handle_pb_Continue_clicked)

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
        if self._output_directory is not None:
            output_xlsx = self._output_directory / output_xlsx.name

        return output_xlsx

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

    def _handle_pb_Configuration_clicked(self) -> None:
        """
        Enables the configuration tab and sets it as the current tab.
        """

        self._window.tw_Main.setTabEnabled(1, True)
        self._window.tw_Main.setCurrentIndex(1)

    def _handle_pb_Continue_clicked(self) -> None:
        """
        Resets the window.
        """

        self._reset()

    def _handle_pb_OpenCsv_clicked(self) -> None:
        """
        Opens a file dialog box to search for the CSV experiment outputs and
        then updates the tbl_Files with the selected files.
        """

        input_csvs, _ = QFileDialog.getOpenFileNames(
            self, "Select CSV Files", "", "CSV Files (*.csv);;All Files (*)"
        )

        for input_csv in [Path(f) for f in input_csvs]:
            self._files.append((input_csv, self._create_output_xlsx(input_csv)))

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

            self._files.append((input_csv, self._create_output_xlsx(input_csv)))

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
        analysers: list[experiment.Analyser] = [
            widget.create_analyser(input_csv, output_xlsx, widget.parameters)
            for input_csv, output_xlsx in self._files
        ]

        # Analyse all of the experiments
        for i in range(self._window.tbl_Files.rowCount()):
            self._window.tbl_Output.setRowCount(i + 1)
            self._window.tbl_Output.setItem(
                i,
                0,
                QTableWidgetItem(
                    f"{i + 1}/{len(analysers)}: {analysers[i].output_xlsx.name}"
                ),
            )
            self._window.tbl_Output.scrollToBottom()
            QApplication.processEvents()

            analysers[i].analyse()
            analysers[i].save()

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

        for i, (_, output_xlsx) in enumerate(self._files):
            self._files[i] = (_, self._output_directory / output_xlsx.name)

        self._update_tbl_Files()

    def _reset(self) -> None:
        """
        Resets the window.
        """

        # Initially disable the configuration and output tabs
        self._window.tw_Main.setTabEnabled(0, True)
        self._window.tw_Main.setTabEnabled(1, False)
        self._window.tw_Main.setTabEnabled(2, False)

        # Reset the files
        self._files.clear()
        self._output_directory = None
        self._update_tbl_Files()

        # Set the initial instrument and experiment drop down menus
        self._handle_cb_Instrument_changed()
        self._handle_cb_Experiment_changed()

        # Disable the continue button
        self._window.pb_Continue.setEnabled(False)

    def _update_tbl_Files(self) -> None:
        """
        Updates the files table.
        """

        self._window.tbl_Files.setRowCount(len(self._files))

        for r in range(self._window.tbl_Files.rowCount()):
            self._window.tbl_Files.setItem(
                r, 0, QTableWidgetItem(self._files[r][0].stem)
            )
            for c in range(len(self._files[r])):
                self._window.tbl_Files.setItem(
                    r, c + 1, QTableWidgetItem(str(self._files[r][c]))
                )

        self._window.tbl_Files.resizeColumnsToContents()
        self._window.tbl_Files.horizontalHeader().setVisible(
            self._window.tbl_Files.rowCount() != 0
        )


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
