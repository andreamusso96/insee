from enum import Enum
import os

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
data_dir = f'{base_dir}/data/iris/AdminData'


def get_data_file_path() -> str:
    return f'{data_dir}/AdminComplete.csv'


def get_metadata_file_path() -> str:
    return f'{data_dir}/AdminCompleteMetaData.csv'


class INSEEDataFileName(Enum):
    OCCUPATION = 'ActiviteResidents.csv'
    COUPLES_FAMILIES_HOUSEHOLDS = 'CouplesFamillesMenages.csv'
    EDUCATION = 'Diplomes.csv'
    HOUSING = 'Logement.csv'
    POPULATION = 'Population.csv'
    INCOME = 'RevenuPauvrete.csv'


def get_insee_data_file_path(file_name: INSEEDataFileName, year: int) -> str:
    return f'{data_dir}/{year}/{file_name.value}'


def get_insee_metadata_file_path(file_name: INSEEDataFileName, year: int) -> str:
    return f'{data_dir}/{year}/{file_name.value.replace(".csv", "MetaData.csv")}'