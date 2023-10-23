from typing import List

import geopandas as gpd

from .data import data
from ... import utils


def get_geo_data(iris: List[str] = None) -> gpd.GeoDataFrame:
    iris_ = iris if iris is not None else data.data.index
    return data.data.loc[iris_].copy()


def get_matching_iris(polygons: gpd.GeoDataFrame, return_intersection_area: bool = True) -> gpd.GeoDataFrame:
    return utils.get_matching_between_polygons_and_insee_geo_data(polygons=polygons, insee_geo_data=data.data, insee_geo_data_name='iris', return_intersection_area=return_intersection_area)
