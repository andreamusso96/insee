import pandas as pd
import geopandas as gpd
import shapely

from . import config


def load_equipment_data_file():
    data = pd.read_csv(config.get_equipment_data_file_path(year=2021), sep=';', low_memory=False, compression='gzip')
    data['geometry'] = data.apply(lambda x: shapely.geometry.Point(x['LAMBERT_X'], x['LAMBERT_Y']), axis=1)
    data.drop(columns=['LAMBERT_X', 'LAMBERT_Y'], inplace=True)
    data = gpd.GeoDataFrame(data=data, geometry='geometry', crs='EPSG:2154')
    return data


def load_equipment_metadata_file():
    metadata = pd.read_csv(config.get_equipment_metadata_file_path(year=2021), sep=';')
    metadata = metadata.loc[metadata['COD_VAR'].isin(['SDOM', 'TYPEQU'])]
    return metadata