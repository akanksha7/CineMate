import kaggle

from common.logger import Logger
from query.query_generic import QueryGeneric


class QueryKaggle(QueryGeneric):

    def __init__(self, log_level=Logger.INFO):
        self._logger = Logger(self.__class__.__name__)
        self._logger.set_level(log_level)

    def execute(self):
        # TODO run this execution in a thread
        self._logger.info('Query kaggle to get dataset related to movie ratings')

        # TODO is this the best way?
        datasets = kaggle.api.dataset_list(search='movie IMDb rating', file_type='csv', sort_by="votes")

        # Download the first 10 most popular datasets
        for dataset in datasets[:3]:
            try:
                self._logger.debug(f"Downloading files from dataset: {dataset}")
                kaggle.api.dataset_download_files(dataset.ref, path='./data/', unzip=True)
            except Exception:
                self._logger.error(f"Unable to download from dataset: {dataset}")
