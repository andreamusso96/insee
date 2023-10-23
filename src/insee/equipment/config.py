import os

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
data_dir = f'{base_dir}/data/equipment'


def get_equipment_data_file_path(year: int):
    return f'{data_dir}/{year}/bpe21_ensemble_xy.csv.gz'


def get_equipment_metadata_file_path(year: int):
    return f'{data_dir}/{year}/Varmod_bpe21_ensemble_xy.csv'