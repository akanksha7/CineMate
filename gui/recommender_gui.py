import os
import pandas as pd
from datetime import datetime

from common.base_dataset import BaseDataset
from common.logger import Logger
from gui.import_widget import ImportWidget
from query.query_widget import QueryWidget
from table.table_widget import TableWidget
from ui.ui_main import Ui_MainWindow

from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QMainWindow


class RecommenderGui(QMainWindow):
    # Initialize gui
    def __init__(self, log_level=Logger.INFO):
        super().__init__()
        # Initialize ui
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self._set_stylesheet()

        # Setup logging
        self._log_level = log_level
        self._logger = Logger(self.__class__.__name__)
        self._logger.set_level(log_level)
        self._logger.info("Running movie recommendation app")

        # Widgets
        self._query_widget = QueryWidget(self._log_level)
        self._table_widget = TableWidget()
        self._import_widget = ImportWidget(self._log_level)

        # Get the saved data located in ./data
        self._get_initial_data()

        # Connect signals
        self._import_widget.done.connect(self._finish_import)
        self._query_widget.done.connect(self._finish_query)
        self.ui.openImport.pressed.connect(self._import_widget.show)
        self.ui.openQuery.pressed.connect(self._query_widget.show)
        self.ui.openTable.pressed.connect(self._open_table)

    def _set_stylesheet(self):
        # Dark mode stylesheet
        style = """
            QWidget {
                background-color: #323232;
                color: #FFFFFF;
            }
            QPushButton {
                background-color: #666666;
                color: #FFFFFF;
            }
            QPushButton:hover {
                background-color: #888888;
            }
        """
        self.setStyleSheet(style)

    def _get_initial_data(self):
        output_dir = './data'
        for file in os.listdir(output_dir):
            file_path = os.path.join(output_dir, file)
            try:
                dataset = BaseDataset(file.split('.')[0])
                dataset.df = pd.read_csv(file_path)
                self.ui.datasets.addItem(dataset.name, dataset.df)
            except Exception as e:
                self._logger.error(f"Unable to convert file to dataframe: {file_path}")
                self._logger.error(e)

    def _finish_import(self, dataset: BaseDataset):
        self.ui.datasets.addItem(dataset.name, dataset.df)

    def _finish_query(self, name: str) -> None:
        self._logger.info('Done with query. Cleaning up tmp files and creating dataframe.')

        # Read each CSV file into a DataFrame, then remove the file
        output_dir = './tmp_data'
        dfs = []
        for file in os.listdir(output_dir):
            file_path = os.path.join(output_dir, file)
            if file.endswith('.csv'):
                try:
                    df = pd.read_csv(file_path)
                    dfs.append(df)
                except Exception as e:
                    self._logger.error(f"Unable to convert file to dataframe: {file_path}")
                    self._logger.error(e)
                self._logger.debug(f"Removing file {file}")
            os.remove(file_path)

        # Create a new dataset
        if dfs:
            dataset = BaseDataset(name + '_' + datetime.now().strftime("%H:%M:%S"))
            dataset.df = pd.concat(dfs, ignore_index=True)
            self.ui.datasets.addItem(dataset.name, dataset.df)
        else:
            self._logger.info('No dataset created')

    def _open_table(self) -> None:
        """Show the current dataset's dataframe in a table."""
        if self.ui.datasets.currentData() is not None:
            self._table_widget.set_data(self.ui.datasets.currentData())
            self._table_widget.show()
        else:
            self._logger.debug('No dataset selected')

    def closeEvent(self, a0: QCloseEvent) -> None:
        """Qt override to ensure all widgets close once main window closes"""
        self._import_widget.close()
        self._query_widget.close()
        self._table_widget.close()
        super().closeEvent(a0)
