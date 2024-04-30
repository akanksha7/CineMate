import pandas as pd
from datetime import datetime

from common.base_dataset import BaseDataset
from common.logger import Logger
from common.worker import Worker
from query.query_kaggle import QueryKaggle
from ui.ui_querywidget import Ui_QueryWidget

from PyQt5.QtCore import pyqtSignal, QThreadPool
from PyQt5.QtWidgets import QWidget


class QueryWidget(QWidget):
    done = pyqtSignal(list)

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
        kaggle_cls.finalized.connect(self._create_datasets)
        self._datasources['Kaggle'] = kaggle_cls
        self.ui.datasources.addItem('Kaggle')
        self._logger.debug(f'Available datasources: {list(self._datasources.keys())}')

    def _create_datasets(self, dfs: list, name: str, merge: bool) -> None:
        """From the query results, create a merged dataset, or individual datasets."""
        datasets = []
        if merge:
            if dfs:
                try:
                    dataset = BaseDataset(name + '_' + datetime.now().strftime("%H:%M:%S"))
                    dataset.df = pd.concat(dfs, ignore_index=True)
                    datasets.append(dataset)
                except Exception as e:
                    self._logger.error(f"Unable to concat dataframes.")
                    self._logger.error(e)
        else:
            for idx, df in enumerate(dfs):
                try:
                    dataset = BaseDataset(name + f'_{idx}_' + datetime.now().strftime("%H:%M:%S"))
                    dataset.df = df
                    datasets.append(dataset)
                except Exception as e:
                    self._logger.error(f"Unable to concat dataframes.")
                    self._logger.error(e)
        self.done.emit(datasets)

    def _execute(self) -> None:
        """Execute clicked. Start thread to run query."""
        datasource = self.ui.datasources.currentText()
        cls = self._datasources[datasource]
        worker = Worker(cls.execute, self.ui.searchText.text())
        worker.signals.finished.connect(lambda: cls.finalize(self.ui.searchText.text().replace(' ', '_'),
                                                             self.ui.merge.isChecked()))
        self._logger.debug(f'Starting query thread for {datasource} datasource')
        self._thread_pool.start(worker)
        self.hide()

    def show(self) -> None:
        """Qt override to set the default search text"""
        # TODO figure out what the best default search text is
        self.ui.searchText.setText('movie IMDb rating')
        super().show()
