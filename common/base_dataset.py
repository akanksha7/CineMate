import pandas as pd

from common.fields import Genre, Rating, Title


class BaseDataset:
    # Required fields
    REQUIRED_FIELDS = [Genre, Rating, Title]

    def __init__(self, name=''):
        self.name = name
        self._df = pd.DataFrame()

    @property
    def df(self) -> pd.DataFrame:
        return self._df

    @df.setter
    def df(self, value: pd.DataFrame) -> None:
        self._df = value
        self._normalize()

    def _normalize(self) -> None:
        """Ensure the dataframe has it's required columns."""
        for field in self.REQUIRED_FIELDS:
            if not any(col in self._df.columns for col in [field.NAME + field.aliases()]):
                self._df[field.NAME] = None
