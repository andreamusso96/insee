from typing import List

import geopandas as gpd
import numpy as np

from .. import utils
from . data import data


def get_geo_data(commune_ids: List[str] = None, with_arrondissement_municipal: bool = False) -> gpd.GeoDataFrame:
    commune_geo_data = data.geo_data(with_arrondissement_municipal=with_arrondissement_municipal)
    commune_ids_ = commune_geo_data.index if commune_ids is None else np.intersect1d(commune_ids, commune_geo_data.index)
    return commune_geo_data.loc[commune_ids_].copy()

def get_matching_communes(polygons: gpd.GeoDataFrame, return_intersection_area: bool = True, with_arrondissement_municipal: bool = False) -> gpd.GeoDataFrame:
    commune_geo_data = data.geo_data(with_arrondissement_municipal=with_arrondissement_municipal)
    return utils.get_matching_between_polygons_and_insee_geo_data(polygons=polygons, insee_geo_data=commune_geo_data, insee_geo_data_name='commune', return_intersection_area=return_intersection_area)


def get_home_work_displacements(home_commune_ids: List[str] = None, work_commune_ids: List[str] = None):
    all_home_insee_com_ids = data.home_work_displacement_data['home_insee_com'].unique()
    all_work_insee_com_ids = data.home_work_displacement_data['work_insee_com'].unique()
    home_commune_ids = all_home_insee_com_ids if home_commune_ids is None else np.intersect1d(home_commune_ids, all_home_insee_com_ids)
    work_commune_ids = all_work_insee_com_ids if work_commune_ids is None else np.intersect1d(work_commune_ids, all_work_insee_com_ids)
    data_ = data.home_work_displacement_data.loc[(data.home_work_displacement_data['home_insee_com'].isin(home_commune_ids) & data.home_work_displacement_data['work_insee_com'].isin(work_commune_ids))].copy()
    return data_