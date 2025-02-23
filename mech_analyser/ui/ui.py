import experiment.experiment as experiment
import importlib
import os

from PySide6.QtWidgets import QApplication, QMainWindow
from typing import Optional
from ui.window import Ui_MainWindow


_EXPERIMENTS_DIR: str = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "experiment")
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

        # Create the main window
        self._window = Ui_MainWindow()
        self._window.setupUi(self)  # type: ignore

        # Create the widget and the widget manager
        self._widget_manager = WidgetManager()
        for e in _EXPERIMENTS:
            widget: experiment.Widget = getattr(e, "Widget")()
            widget.init()
            self._window.sw_Configuration.addWidget(widget)
            self._widget_manager.add(widget)

        # Determine the instrument options
        self._window.cb_Instrument.clear()
        self._window.cb_Instrument.addItems(self._widget_manager.get_instruments())

        # Connect the experiment selection to the configuration view
        self._window.cb_Experiment.currentIndexChanged.connect(
            self._handle_cb_Experiment
        )
        self._window.cb_Instrument.currentIndexChanged.connect(
            self._handle_cb_Instrument
        )

        # Set the initial view
        self._handle_cb_Instrument()
        self._handle_cb_Experiment()

    def _handle_cb_Experiment(self) -> None:
        """
        Activates the widget corresponding to the instrument and experiment.
        """

        widget: Optional[experiment.Widget] = self._widget_manager.get(
            self._window.cb_Instrument.currentText(),
            self._window.cb_Experiment.currentText(),
        )

        if widget is not None:
            widget.activate(self._window.sw_Configuration)

    def _handle_cb_Instrument(self) -> None:
        """
        Updates the experiment selection based on the selected instrument.
        """

        self._window.cb_Experiment.clear()
        self._window.cb_Experiment.addItems(
            self._widget_manager.get_experiments(
                self._window.cb_Instrument.currentText()
            )
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
