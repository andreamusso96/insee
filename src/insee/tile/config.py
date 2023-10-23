import os

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
data_dir = f'{base_dir}/data/tile'


def get_data_file_path():
    return f'{data_dir}/Filosofi2017_carreaux_200m_met.shp'


def get_metadata_file_path():
    return f'{data_dir}/metadata.csv'