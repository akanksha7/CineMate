import os
import pandas as pd
import uuid

from common.base_dataset import BaseDataset
from common.logger import Logger
from query.query_widget import QueryWidget
from table.table_widget import TableWidget
from ui.ui_main import Ui_MainWindow

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

        # Query Widget
        self._query_widget = QueryWidget(self._log_level)

        # Table Widget
        self._table_widget = TableWidget()

        # Main dataframe
        self._df = BaseDataset()
        self._get_initial_data()

        # Connect signals
        self._query_widget.done.connect(self._finish_query)
        self.ui.openQuery.pressed.connect(self._query_widget.show)
        self.ui.showDataset.pressed.connect(self._show_dataset)

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
        # TODO read all the files in the data directory to set the og dataframe
        pass

    def _finish_query(self) -> None:
        self._logger.info('Done with query. Cleaning up tmp files and creating dataframe.')
        output_dir = './tmp_data'
        csv_files = [file for file in os.listdir(output_dir) if file.endswith('.csv')]

        # Read each CSV file into a DataFrame, then remove the file
        dfs = []
        for file in csv_files:
            file_path = os.path.join(output_dir, file)
            df = pd.read_csv(file_path)
            dfs.append(df)
            self._logger.debug(f"Removing file {file_path}")
            os.remove(file_path)
        dataset = BaseDataset(str(uuid.uuid4()))
        dataset.dataframe = pd.concat(dfs, ignore_index=True)
        self.ui.datasets.addItem(dataset.name, dataset.dataframe)

    def _show_dataset(self) -> None:
        """Show the current dataset's dataframe."""
        if self.ui.datasets.currentData() is not None:
            self._table_widget.set_data(self.ui.datasets.currentData())
            self._table_widget.show()
