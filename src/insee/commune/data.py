import geopandas as gpd
import pandas as pd

from . import config
from . import preprocessing


# Lazy loading
class Data:
    def __init__(self):
        self._home_work_displacement_data = None
        self._geo_data = None
        self._geo_data_has_arrondissement_municipal = None

    def geo_data(self, with_arrondissement_municipal: bool = False) -> gpd.GeoDataFrame:
        if self._geo_data is None or self._geo_data_has_arrondissement_municipal != with_arrondissement_municipal:
            self._geo_data_has_arrondissement_municipal = with_arrondissement_municipal
            self._geo_data = preprocessing.load_geo_data(with_arrondissement_municipal=with_arrondissement_municipal)
        return self._geo_data

    @property
    def home_work_displacement_data(self) -> pd.DataFrame:
        if self._home_work_displacement_data is None:
            self._home_work_displacement_data = preprocessing.load_home_work_displacement_data()
        return self._home_work_displacement_data


data = Data()