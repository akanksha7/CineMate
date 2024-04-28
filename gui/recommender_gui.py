from common.base_dataset import BaseDataset
from common.logger import Logger
from query.query_kaggle import QueryKaggle
from ui.ui_main import Ui_MainWindow

from PyQt5.QtWidgets import QMainWindow


class RecommenderGui(QMainWindow):
    # Initialize gui
    def __init__(self, log_level=Logger.INFO):
        super().__init__()
        # Initialize ui
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Setup logging
        self._log_level = log_level
        self._logger = Logger(self.__class__.__name__)
        self._logger.set_level(log_level)
        self._logger.info("Running movie recommendation app")

        # Main dataframe
        self._df = BaseDataset()
        self._get_initial_data()

        # Connect signals
        self.ui.query.pressed.connect(self._start_query)

    def _get_initial_data(self):
        # TODO read all the files in the data directory to set the dataframe
        pass

    def _start_query(self) -> None:
        query = QueryKaggle(log_level=self._log_level)
        query.execute()
