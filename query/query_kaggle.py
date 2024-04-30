import os
import kaggle
import pandas as pd

from common.logger import Logger
from query.query_generic import QueryGeneric


class QueryKaggle(QueryGeneric):

    def __init__(self, log_level=Logger.INFO):
        super().__init__()
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

    def finalize(self, name: str, merge: bool) -> None:
        """Query has finished. Read the files and cleanup."""
        # Read each CSV file into a DataFrame
        output_dir = './tmp_data'
        dfs = []
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                file_path = os.path.join(root, file)
                self._logger.debug(f"Reading file: {file}")
                if file.endswith('.csv'):
                    try:
                        df = pd.read_csv(file_path)
                        dfs.append(df)
                    except Exception as e:
                        self._logger.error(f"Unable to convert file to dataframe: {file_path}")
                        self._logger.error(e)

        # After we finish reading all files, cleanup tmp directory
        for root, dirs, files in os.walk(output_dir, topdown=False):
            for file in files:
                file_path = os.path.join(root, file)
                os.remove(file_path)
                self._logger.debug(f"Removing file {file}")
            for directory in dirs:
                dir_path = os.path.join(root, directory)
                os.rmdir(dir_path)
                self._logger.debug(f"Removing sub directory {directory}")

        self.finalized.emit(dfs, name, merge)
