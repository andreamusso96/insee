import geopandas as gpd
import pandas as pd
import numpy as np
import shapely


def get_matching_between_polygons_and_insee_geo_data(polygons: gpd.GeoDataFrame, insee_geo_data: gpd.GeoDataFrame, insee_geo_data_name: str, return_intersection_area: bool = True, epsilon_buffer: float = 0.001) -> gpd.GeoDataFrame:
    polygons_ = polygons.to_crs(epsg=2154)
    insee_geo_ = insee_geo_data.to_crs(epsg=2154)
    polygons_['geometry'] = polygons_['geometry'].buffer(epsilon_buffer)
    insee_geo_['geometry'] = insee_geo_data['geometry'].buffer(epsilon_buffer)
    polygons_and_matching_insee_geo = gpd.sjoin(polygons_, insee_geo_, how='left', predicate='intersects')[['geometry', 'index_right']]
    if return_intersection_area:
        polygons_and_matching_insee_geo['intersection_area'] = _compute_intersection_area_polygons_tiles(polygons_and_matching_insee_geo=polygons_and_matching_insee_geo, insee_geo_data=insee_geo_)

    polygons_and_matching_insee_geo.rename(columns={'index_right': insee_geo_data_name}, inplace=True)
    return polygons_and_matching_insee_geo


def _compute_intersection_area_polygons_tiles(polygons_and_matching_insee_geo: gpd.GeoDataFrame, insee_geo_data: gpd.GeoDataFrame) -> pd.Series:
    def intersection_area(x) -> float:
        if pd.isna(x['index_right']):
            return np.nan
        area = x['geometry'].intersection(insee_geo_data.loc[x['index_right'], 'geometry']).area
        return area

    intersection_area_ = polygons_and_matching_insee_geo.apply(lambda x: intersection_area(x=x), axis=1)
    return intersection_area_
