import kaggle

from common.logger import Logger
from query.query_generic import QueryGeneric


class QueryKaggle(QueryGeneric):

    def __init__(self, log_level=Logger.INFO):
        self._logger = Logger(self.__class__.__name__)
        self._logger.set_level(log_level)

    def execute(self, text: str, **kwargs) -> None:
        """Use kaggle api to query and download data."""
        self._logger.info('Query kaggle to get dataset related to movie ratings')

        # TODO is this the best way?
        datasets = kaggle.api.dataset_list(search=text, file_type='csv', sort_by="hottest")

        # Download the first n most popular datasets
        for dataset in datasets[:3]:
            try:
                self._logger.debug(f"Downloading files from dataset: {dataset}")
                kaggle.api.dataset_download_files(dataset.ref, path='./tmp_data/', unzip=True)
            except Exception as e:
                self._logger.error(f"Unable to download from dataset: {dataset}")
                self._logger.error(e)

