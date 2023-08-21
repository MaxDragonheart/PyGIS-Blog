import datetime
import logging
from pathlib import Path
import geopandas as gpd
import pandas as pd
import osmnx as ox

logger = logging.getLogger()
logger.setLevel(logging.INFO)
log_format = '%(asctime)s | %(process)d - %(message)s'
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(log_format))
logger.addHandler(console_handler)

logger.addHandler(console_handler)

excluded_keys = ['aircraft', 'aircraft; memorial', 'anchor', 'battlefield', 'bomb_crater', 'boundary_stone', 'cannon', 'cattle_crush', 'district', 'highwater_mark', 'hotel', 'locomotive', 'memorial', 'ogham_stone', 'railway', 'railway_car', 'railway_station', 'road', 'shieling', 'ship', 'tank', 'vehicle', 'wayside_cross', 'wayside_shrine', 'wreck', 'yes']

osm_crs = 4326

main_folder = Path.cwd().parent.parent.parent.parent.joinpath('sample_data')
regions = main_folder.joinpath('Reg01012023_g').joinpath('Reg01012023_g_WGS84.shp')


regions_gdf = gpd.read_file(regions).to_crs(osm_crs)
italia = regions_gdf.dissolve().squeeze()

italia_data = ox.features_from_polygon(
    polygon=italia.geometry,
    tags={'historic': True}
)

italia_data = italia_data[['historic', 'name', 'historic:civilization', 'geometry']]
italia_data = italia_data[~italia_data['historic'].isin(excluded_keys)]
italia_data = italia_data[italia_data['name'].notna()]
italia_data.reset_index(inplace=True)

italia_polygons = italia_data[italia_data['element_type'] == 'way']

italia_final = pd.concat([italia_polygons, italia_data[italia_data['element_type'] == 'node']])
italia_final.drop(columns={'element_type'}, inplace=True)
italia_final.sort_values(by='name', inplace=True)
italia_final = gpd.GeoDataFrame(italia_final, geometry='geometry')


if __name__ == '__main__':
    time_start = datetime.datetime.now()
    logging.info(f'Start analysis at {time_start}')

    print(italia)

    time_end = datetime.datetime.now()
    time_diff = time_end - time_start
    logging.info(f'End analysis at {time_end}')
    logging.info(f'Process time: {time_diff}')