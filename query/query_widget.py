from common.logger import Logger
from common.worker import Worker
from query.query_kaggle import QueryKaggle
from ui.ui_querywidget import Ui_QueryWidget

from PyQt5.QtCore import pyqtSignal, QThreadPool
from PyQt5.QtWidgets import QWidget


class QueryWidget(QWidget):
    done = pyqtSignal(str)

    def __init__(self, log_level=Logger.INFO):
        super().__init__()
        # Initialize ui
        self.ui = Ui_QueryWidget()
        self.ui.setupUi(self)

        # Setup logging
        self._log_level = log_level
        self._logger = Logger(self.__class__.__name__)
        self._logger.set_level(log_level)

        # Thread pool to run queries
        self._thread_pool = QThreadPool(self)

        # Add available datasources
        self._datasources = {}
        self._add_datasources()

        # Setup signals
        self.ui.execute.pressed.connect(self._execute)

    def _add_datasources(self):
        # TODO adding these datasources should probably be setup in a configuration file
        #  but for now we only have one datasource so this is fine
        kaggle_cls = QueryKaggle(self._log_level)
        self._datasources['Kaggle'] = kaggle_cls
        self.ui.datasources.addItem('Kaggle')
        self._logger.debug(f'Available datasources: {list(self._datasources.keys())}')

    def _execute(self) -> None:
        """Execute clicked. Start thread to run query."""
        datasource = self.ui.datasources.currentText()
        cls = self._datasources[datasource]
        worker = Worker(cls.execute, self.ui.searchText.text().replace(' ', '_'))
        worker.signals.finished.connect(lambda: self.done.emit(self.ui.searchText.text()))
        self._logger.debug(f'Starting query thread for {datasource} datasource')
        self._thread_pool.start(worker)
        self.hide()

    def show(self) -> None:
        """Qt override to set the default search text"""
        # TODO figure out what the best default search text is
        self.ui.searchText.setText('movie IMDb rating')
        super().show()
