import os
from enum import Enum

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
data_dir = f'{base_dir}/data/commune'


class GeoDataFile(Enum):
    COMMUNE = 'COMMUNE'
    ARRONDISSEMENT_MUNICIPAL = 'ARRONDISSEMENT_MUNICIPAL'


def get_geo_data_file_path(geo_data_file: GeoDataFile):
    geo_data_dir = f'{data_dir}/geo/2022'
    return f'{geo_data_dir}/{geo_data_file.value}.shp'


def get_home_work_displacement_data_file_path():
    return f'{data_dir}/home_work_displacement/base-flux-mobilite-domicile-lieu-travail-2019.csv'
