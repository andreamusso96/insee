import numpy as np
import pandas as pd

from . import config
from ... import equipment
from .. import geo


def save_preprocessed_admin_data():
    admin_data = generate_admin_data()
    admin_data.to_csv(config.get_data_file_path(), index=True)


def save_preprocessed_admin_metadata():
    admin_metadata = generate_admin_metadata()
    admin_metadata.to_csv(config.get_metadata_file_path(), index=False)


def generate_admin_data() -> pd.DataFrame:
    equipment_counts = get_equipment_counts_data()
    data = merge_insee_datasets(dataset1=equipment_counts, dataset2=load_insee_data_file(file_name=config.INSEEDataFileName.OCCUPATION))
    data = merge_insee_datasets(dataset1=data, dataset2=load_insee_data_file(file_name=config.INSEEDataFileName.COUPLES_FAMILIES_HOUSEHOLDS))
    data = merge_insee_datasets(dataset1=data, dataset2=load_insee_data_file(file_name=config.INSEEDataFileName.EDUCATION))
    data = merge_insee_datasets(dataset1=data, dataset2=load_insee_data_file(file_name=config.INSEEDataFileName.HOUSING))
    data = merge_insee_datasets(dataset1=data, dataset2=load_insee_data_file(file_name=config.INSEEDataFileName.INCOME))
    data = merge_insee_datasets(dataset1=data, dataset2=load_insee_data_file(file_name=config.INSEEDataFileName.POPULATION))
    data.sort_index(inplace=True)
    return data


def merge_insee_datasets(dataset1: pd.DataFrame, dataset2: pd.DataFrame) -> pd.DataFrame:
    merged_datasets = dataset1.merge(dataset2, left_index=True, right_index=True, how='outer', suffixes=('', f'_duplicate'))
    merged_datasets.drop(columns=[c for c in merged_datasets.columns if c.endswith('_duplicate')], inplace=True)
    return merged_datasets


def generate_admin_metadata() -> pd.DataFrame:
    merged_metadata = pd.concat([load_insee_metadata_file(file_name=file_name) for file_name in config.INSEEDataFileName])
    merged_metadata = pd.concat([merged_metadata, get_equipment_counts_metadata()])
    merged_metadata = merged_metadata[~merged_metadata['COD_VAR'].duplicated()]
    merged_metadata = merged_metadata.sort_values(by='COD_VAR').reset_index(drop=True)
    return merged_metadata


def get_equipment_counts_data() -> pd.DataFrame:
    iris_geo = geo.get_geo_data()
    equipment_counts = equipment.get_equipment_counts(polygons=iris_geo, resolution=equipment.EquipmentResolution.HIGH)
    equipment_counts.reset_index(inplace=True, names='iris')
    equipment_counts.rename(columns={col: f'EQUIP_{col}' for col in equipment_counts.columns if col != 'iris'}, inplace=True)
    equipment_counts.set_index('iris', inplace=True)
    equipment_counts.sort_index(inplace=True)
    return equipment_counts


def get_equipment_counts_metadata() -> pd.DataFrame:
    metadata = equipment.get_equipment_description(resolution=equipment.EquipmentResolution.HIGH)
    metadata = metadata[['COD_MOD', 'LIB_MOD']].copy()
    metadata.rename(columns={'COD_MOD': 'COD_VAR', 'LIB_MOD': 'DESC'}, inplace=True)
    metadata['COD_VAR'] = metadata['COD_VAR'].apply(lambda x: f'EQUIP_{x}')
    return metadata


def load_insee_data_file(file_name: config.INSEEDataFileName) -> pd.DataFrame:
    if file_name != config.INSEEDataFileName.INCOME:
        return preprocess_insee_data_file(file_name=file_name, year=2019)
    elif file_name == config.INSEEDataFileName.INCOME:
        return preprocess_income_data_file(year=2019)
    else:
        raise NotImplementedError(f'File name {file_name} not implemented')


def load_insee_metadata_file(file_name: config.INSEEDataFileName) -> pd.DataFrame:
    return preprocess_insee_metadata_file(file_name=file_name, year=2019)


def preprocess_insee_data_file(file_name: config.INSEEDataFileName, year: int) -> pd.DataFrame:
    data = read_insee_data_file(file_name=file_name, year=year, sep=';', dtype={'IRIS': str}, low_memory=False)
    data.rename(columns={'IRIS': 'iris'}, inplace=True)
    data.drop(columns=['COM', 'LAB_IRIS', 'MODIF_IRIS'], inplace=True)
    data.sort_values(by='iris', inplace=True)
    data.set_index('iris', inplace=True)
    return data


def preprocess_income_data_file(year: int) -> pd.DataFrame:
    data = read_insee_data_file(file_name=config.INSEEDataFileName.INCOME, year=year, sep=',', dtype={'IRIS': str}, low_memory=False)
    data.rename(columns={'IRIS': 'iris'}, inplace=True)
    data['iris'] = data['iris'].apply(lambda x: str(x).zfill(9))
    data.sort_values(by='iris', inplace=True)
    data.set_index('iris', inplace=True)
    return data


def read_insee_data_file(file_name: config.INSEEDataFileName, year: int, **kwargs) -> pd.DataFrame:
    file_path = config.get_insee_data_file_path(file_name=file_name, year=year)
    data = pd.read_csv(file_path, **kwargs)
    return data


def preprocess_insee_metadata_file(file_name: config.INSEEDataFileName, year: int) -> pd.DataFrame:
    data = read_insee_metadata_file(file_name=file_name, year=year, sep=';')
    data = data[['COD_VAR', 'LIB_VAR_LONG']].copy()
    data.rename(columns={'LIB_VAR_LONG': 'DESC'}, inplace=True)
    data = data[~data['COD_VAR'].isin(['IRIS', 'COM', 'MODIF_IRIS', 'LAB_IRIS'])]
    return data


def read_insee_metadata_file(file_name: config.INSEEDataFileName, year: int, **kwargs) -> pd.DataFrame:
    file_path = config.get_insee_metadata_file_path(file_name=file_name, year=year)
    metadata = pd.read_csv(file_path, **kwargs)
    return metadata