import pandas as pd

from common.logger import Logger
from query.query_kaggle import QueryKaggle


class RecommenderGui:
    # Initialize gui
    def __init__(self, log_level=Logger.INFO):
        # Set logging
        self._log_level = log_level
        self._logger = Logger(self.__class__.__name__)
        self._logger.set_level(log_level)

        # Main dataframe
        self._df = pd.DataFrame
        self._set_df()

    def _set_df(self):
        # TODO read all the files in the data directory to set the dataframe
        pass

    def run(self):
        self._logger.info("Running movie recommendation app")

        query = QueryKaggle(log_level=self._log_level)
        query.execute()
