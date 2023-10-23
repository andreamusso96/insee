import os

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
data_dir = f'{base_dir}/data/iris/GeoData'


def get_data_file_path(year: int):
    return f'{data_dir}/{year}/IRIS_GE.SHP'