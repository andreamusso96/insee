import pandas as pd
import geopandas as gpd

from . import config


def load_geo_data(with_arrondissement_municipal: bool) -> gpd.GeoDataFrame:
    if with_arrondissement_municipal:
        commune = load_commune_data()
        arrondissement_municipal = load_arrondissement_municipal_data()

        commune_to_remove = arrondissement_municipal['insee_com'].unique()
        commune = commune.loc[~commune.index.isin(commune_to_remove)].copy()

        commune_to_add = arrondissement_municipal[['insee_arm', 'geometry']].copy()
        commune_to_add.rename(columns={'insee_arm': 'insee_com'}, inplace=True)
        commune_to_add.set_index('insee_com', inplace=True)
        commune = gpd.GeoDataFrame(pd.concat([commune, commune_to_add], axis=0))
        return commune
    else:
        return load_commune_data()


def load_commune_data() -> gpd.GeoDataFrame:
    data = gpd.read_file(filename=config.get_geo_data_file_path(geo_data_file=config.GeoDataFile.COMMUNE), engine="pyogrio")
    data = data.to_crs(epsg=2154)
    data['INSEE_COM'] = data['INSEE_COM'].astype(str).str.zfill(5)
    data = data[['INSEE_COM', 'geometry']].copy()
    data.rename(columns={'INSEE_COM': 'insee_com'}, inplace=True)
    data.set_index('insee_com', inplace=True)
    return data


def load_arrondissement_municipal_data() -> gpd.GeoDataFrame:
    data = gpd.read_file(filename=config.get_geo_data_file_path(geo_data_file=config.GeoDataFile.ARRONDISSEMENT_MUNICIPAL), engine="pyogrio")
    data = data.to_crs(epsg=2154)
    data['INSEE_COM'] = data['INSEE_COM'].astype(str).str.zfill(5)
    data['INSEE_ARM'] = data['INSEE_ARM'].astype(str).str.zfill(5)
    data = data[['INSEE_COM', 'INSEE_ARM', 'geometry']].copy()
    data.rename(columns={'INSEE_COM': 'insee_com', 'INSEE_ARM': 'insee_arm'}, inplace=True)
    return data


def load_home_work_displacement_data() -> pd.DataFrame:
    data = pd.read_csv(config.get_home_work_displacement_data_file_path(), sep=';', low_memory=False, dtype={'CODGEO': str, 'DCLT': str, 'NBFLUX_C19_ACTOCC15P': float})
    rename_map = {'CODGEO': 'home_insee_com', 'LIBGEO': 'home_insee_com_label', 'DCLT': 'work_insee_com', 'L_DCLT': 'work_insee_com_label', 'NBFLUX_C19_ACTOCC15P': 'count'}
    data.rename(columns=rename_map, inplace=True)
    return data