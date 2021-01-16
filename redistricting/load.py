import pickle
import networkx as nx
import os
import numpy as np
import pandas as pd
import geopandas as gpd

######################## Constants ########################
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
OPT_DATA_PATH = os.path.join(BASE_PATH, "data", "ga_data_structures")
TRACT_SHAPE_PATH = os.path.join(BASE_PATH, "data", "ga_tract_shapes")
DISTRICT_SHAPE_PATH = os.path.join(BASE_PATH, "data", "congressional_districts_2018")

GEORGIA_FIPS = 13


######################## Loading Functions ########################
def load_state_df():
    """
    Returns: (pd.DataFrame) of selected tract level metrics
    """
    state_df_path = os.path.join(OPT_DATA_PATH,
                                 'state_df.csv')
    df = pd.read_csv(state_df_path)
    return df.sort_values(by='GEOID').reset_index(drop=True)


def load_election_df():
    """
    Returns: (pd.DataFrame) of estimated votes by election and party for all tracts
    """
    election_df_path = os.path.join(OPT_DATA_PATH,
                                    'election_df.csv')
    try:
        df = pd.read_csv(election_df_path)
    except FileNotFoundError:
        df = None
    return df  # Indices are equal to state_df integer indices


def load_tract_shapes():
    """
    Returns: (gpd.GeoDataFrame) of tract shapes
    """

    tract_shapes = gpd.read_file(TRACT_SHAPE_PATH)
    tract_shapes = tract_shapes.to_crs(epsg=3078)  # meters
    tract_shapes = tract_shapes[tract_shapes.ALAND > 0]
    return tract_shapes.sort_values(by='GEOID').reset_index(drop=True)


def load_district_shapes():
    """
    Returns: (gpd.GeoDataFrame) of district shapes
    """
    gdf = gpd.read_file(DISTRICT_SHAPE_PATH).sort_values('GEOID').to_crs("EPSG:3078")  # meters
    return gdf[gdf.STATEFP == GEORGIA_FIPS]

def load_graph():
    return nx.read_gpickle(os.path.join(OPT_DATA_PATH, 'G.p'))
