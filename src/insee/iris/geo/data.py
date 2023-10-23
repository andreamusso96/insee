import geopandas as gpd

from . import config


# Lazy loading
class Data:
    def __init__(self):
        self._data = None

    def load_data(self):
        _data = gpd.read_file(filename=config.get_data_file_path(year=2019), engine="pyogrio")
        _data['CODE_IRIS'] = _data['CODE_IRIS'].apply(lambda x: str(x).zfill(9))
        _data.to_crs(epsg=2154, inplace=True)
        _data = _data[['CODE_IRIS', 'geometry']].copy()
        _data.rename(columns={'CODE_IRIS': 'iris'}, inplace=True)
        _data.set_index('iris', inplace=True)
        self._data = _data

    @property
    def data(self) -> gpd.GeoDataFrame:
        if self._data is None:
            self.load_data()
        return self._data


data = Data()