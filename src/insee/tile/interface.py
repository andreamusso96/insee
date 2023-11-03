from typing import List, Union

import geopandas as gpd
import pandas as pd
import numpy as np

from .data import data
from ..import utils


def get_geo_data(tile: List[str] = None) -> gpd.GeoDataFrame:
    geo_data = get_data(tile=tile, var_name='geometry', shares=False)
    return geo_data

def get_matching_tiles(polygons: gpd.GeoDataFrame, return_intersection_area: bool = True) -> gpd.GeoDataFrame:
    return utils.get_matching_between_polygons_and_insee_geo_data(polygons=polygons, insee_geo_data=data.data, insee_geo_data_name='tile', return_intersection_area=return_intersection_area)


def get_data(tile: Union[str, List[str]] = None, var_name: Union[str, List[str]] = None, shares: bool = False):
    tile_ = [tile] if isinstance(tile, str) else tile
    var_name_ = [var_name] if isinstance(var_name, str) else var_name

    tile_ = np.intersect1d(tile_, data.data.index) if tile_ is not None else data.data.index
    var_name_ = var_name_ if var_name_ is not None else data.data.columns

    data_ = data.data.loc[tile_, var_name_].copy()
    if shares:
        pop = data.data.loc[tile_, 'Ind']
        data_ = data_.div(pop, axis=0)
    return data_


def get_metadata():
    return data.metadata.copy()

