from common.base_dataset import BaseDataset
from common.logger import Logger
# from query.query_kaggle import QueryKaggle
from query.query_widget import QueryWidget
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

        # Main dataframe
        self._df = BaseDataset()
        self._get_initial_data()

        # Connect signals
        self._query_widget.done.connect(self._finish_query)
        self.ui.openQuery.pressed.connect(self._query_widget.show)

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

    def _finish_query(self):
        self._logger.info('Done with query')
        # TODO after query is executed, read the files and form a base_dataset,
        #  then delete the csv's in filesystem
