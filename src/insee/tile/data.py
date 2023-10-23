import geopandas as gpd
import pandas as pd

from . import config


# Lazy loading
class Data:
    def __init__(self):
        self._data = None
        self._metadata = None

    def load_data(self):
        _data = gpd.read_file(filename=config.get_data_file_path(), engine="pyogrio")
        _data.to_crs(epsg=2154, inplace=True)
        _data.set_index('Idcar_200m', inplace=True)
        self._data = _data

    def load_metadata(self):
        _metadata = pd.read_csv(config.get_metadata_file_path())
        self._metadata = _metadata

    @property
    def data(self) -> gpd.GeoDataFrame:
        if self._data is None:
            self.load_data()
        return self._data

    @property
    def metadata(self) -> gpd.GeoDataFrame:
        if self._metadata is None:
            self.load_metadata()
        return self._metadata


data = Data()