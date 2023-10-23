import geopandas as gpd
import pandas as pd

from . import preprocessing


# Lazy loading
class Data:
    def __init__(self):
        self._data = None
        self._metadata = None

    def load_data(self):
        self._data = preprocessing.load_equipment_data_file()

    def load_metadata(self):
        self._metadata = preprocessing.load_equipment_metadata_file()

    @property
    def data(self) -> gpd.GeoDataFrame:
        if self._data is None:
            self.load_data()
        return self._data

    @property
    def metadata(self) -> pd.DataFrame:
        if self._metadata is None:
            self.load_metadata()
        return self._metadata


data = Data()
