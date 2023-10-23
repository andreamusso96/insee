from enum import Enum

import geopandas as gpd
import pandas as pd
import numpy as np

from .data import data


class EquipmentResolution(Enum):
    HIGH = 'TYPEQU'
    LOW = 'SDOM'


def get_equipment(polygons: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    polygons_ = polygons.to_crs(epsg=2154)
    polygons_and_matching_equipments = polygons_.sjoin(data.data, how='left', predicate='contains')[['geometry', 'SDOM', 'TYPEQU']]
    return polygons_and_matching_equipments


def get_equipment_counts(polygons: gpd.GeoDataFrame, resolution: EquipmentResolution) -> pd.DataFrame:
    polygons_matched_with_equipment = get_equipment(polygons=polygons)
    polygons_without_equipment = polygons_matched_with_equipment.loc[polygons_matched_with_equipment[resolution.value].isna()].index
    polygons_matched_with_equipment.dropna(subset=[resolution.value], inplace=True)

    polygons_matched_with_equipment['count'] = 1
    polygons_matched_with_equipment.reset_index(inplace=True, names='index')
    equipment_counts = polygons_matched_with_equipment.groupby(by=['index', resolution.value]).agg({'count': 'sum'}).reset_index()
    equipment_counts = equipment_counts.pivot(index='index', columns=resolution.value, values='count').fillna(0)
    equipment_counts_polygons_without_equipment_np = np.zeros(shape=(len(polygons_without_equipment), len(equipment_counts.columns)))
    equipment_counts_polygons_without_equipment = pd.DataFrame(data=equipment_counts_polygons_without_equipment_np, columns=equipment_counts.columns, index=polygons_without_equipment)
    equipment_counts = pd.concat([equipment_counts, equipment_counts_polygons_without_equipment])

    return equipment_counts


def get_equipment_description(resolution: EquipmentResolution = None) -> pd.DataFrame:
    if resolution is None:
        return data.metadata.copy()
    else:
        return data.metadata.loc[data.metadata['COD_VAR'] == resolution.value].copy()