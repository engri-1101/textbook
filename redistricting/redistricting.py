# imports
import os
import pickle
import numpy as np
import networkx as nx
import pandas as pd
import geopandas as gpd
from scipy.stats import t
import matplotlib.pyplot as plt

# ----------------------
# Data loading functions
# ----------------------

######################## Constants ########################
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
OPT_DATA_PATH = os.path.join(BASE_PATH, "data", "ga_data_structures")
TRACT_SHAPE_PATH = os.path.join(BASE_PATH, "data", "ga_tract_shapes")
DISTRICT_SHAPE_PATH = os.path.join(BASE_PATH, "data", "congressional_districts_2018")
GEORGIA_FIPS = 13


def load_state_df():
    """Returns: (pd.DataFrame) of selected tract level metrics"""
    state_df_path = os.path.join(OPT_DATA_PATH, 'state_df.csv')
    df = pd.read_csv(state_df_path)
    return df.sort_values(by='GEOID').reset_index(drop=True)


def load_election_df():
    """Returns: (pd.DataFrame) of estimated votes by election and party for all tracts"""
    election_df_path = os.path.join(OPT_DATA_PATH, 'election_df.csv')
    try:
        df = pd.read_csv(election_df_path)
    except FileNotFoundError:
        df = None
    return df  # Indices are equal to state_df integer indices


def load_tract_shapes():
    """Returns: (gpd.GeoDataFrame) of tract shapes"""
    tract_shapes = gpd.read_file(TRACT_SHAPE_PATH)
    tract_shapes = tract_shapes.to_crs(epsg=3078)  # meters
    tract_shapes = tract_shapes[tract_shapes.ALAND > 0]
    return tract_shapes.sort_values(by='GEOID').reset_index(drop=True)


def load_district_shapes():
    """Returns: (gpd.GeoDataFrame) of district shapes"""
    gdf = gpd.read_file(DISTRICT_SHAPE_PATH).sort_values('GEOID').to_crs("EPSG:3078")  # meters
    return gdf[gdf.STATEFP == GEORGIA_FIPS]


def load_graph():
    return nx.read_gpickle(os.path.join(OPT_DATA_PATH, 'G.p'))


# --------------------------------
# Helper functions for model input
# --------------------------------

def make_tdm(leaf_nodes, n_blocks=None):
    """Generate the block district matrix given by a sample trees leaf nodes.
    **Renamed to tdm to align with tract_distanct_matrix nomenclature in lab notebook.**
    
    Args:
        leaf_nodes: SHPNode list, output of the generation routine
        n_blocks: (int) number of blocks in the state

    Returns: (np.array) n x d matrix where a_ij = 1 when block i appears in district j.
    """
    districts = [d['area'] for d in leaf_nodes]
    if n_blocks is None:
        n_blocks = max([max(d) for d in districts]) + 1
    block_district_matrix = np.zeros((n_blocks, len(districts)))
    for ix, d in enumerate(districts):
        block_district_matrix[d, ix] = 1
    return block_district_matrix


def efficiency_gap_coefficients(district_df, state_vote_share):
    """
    Args:
        district_df: (pd.DataFrame) selected district statistics
            (requires "mean", "std_dev", "DoF")
        state_vote_share: (float) average state vote share across historical elections.

    Returns: (np.array) of efficiency gap cost coefficients

    """
    mean = district_df['mean'].values
    std_dev = district_df['std_dev'].values
    DoF = district_df['DoF'].values
    expected_seats = 1 - t.cdf(.5, DoF, mean, std_dev)
    # https://www.brennancenter.org/sites/default/files/legal-work/How_the_Efficiency_Gap_Standard_Works.pdf
    # Efficiency Gap = (Seat Margin – 50%) – 2 (Vote Margin – 50%)
    return (expected_seats - .5) - 2 * (state_vote_share - .5)


def make_root_partition_to_leaf_map(leaf_nodes, internal_nodes):
    """Shard the sample tree leaf nodes by root partition.

    Args:
        leaf_nodes: (SHPNode list) with node capacity equal to 1 (has no child nodes).
        internal_nodes: (SHPNode list) with node capacity >1 (has child nodes).

    Returns: (dict) {root partition index: array of leaf node indices}

    """
    def add_children(node, root_partition_id):
        if node['n_districts'] > 1:
            for partition in node['children_ids']:
                for child in partition:
                    add_children(node_dict[child], root_partition_id)
        else:
            node_to_root_partition[id_to_ix[node['id']]] = root_partition_id

    # Create mapping from leaf ix to root partition ix
    node_to_root_partition = {}
    node_dict = {n['id']: n for n in internal_nodes + leaf_nodes}
    id_to_ix = {n['id']: ix for ix, n in enumerate(leaf_nodes)}
    root = internal_nodes[0]
    for ix, root_partition in enumerate(root['children_ids']):
        for child in root_partition:
            add_children(node_dict[child], ix)

    # Create inverse mapping
    partition_map = {}
    for node_ix, partition_ix in node_to_root_partition.items():
        try:
            partition_map[partition_ix].append(node_ix)
        except KeyError:
            partition_map[partition_ix] = [node_ix]
    partition_map = {ix: np.array(leaf_list) for ix, leaf_list in partition_map.items()}

    return partition_map

# ------------------
# Plotting functions
# ------------------

def draw_adjacency_graph(gdf, G, figsize=(200, 150)):
    base = gdf.plot(color='white', edgecolor='black', figsize=figsize, lw=.5)
    edge_colors = ['green' if G[u][v].get('inferred', False) else 'red'
                   for u, v in G.edges]
    pos = {i: (geo.centroid.x, geo.centroid.y)
           for i, geo in gdf.geometry.iteritems()}
    if len(G) == len(gdf) + 1:  # If adj graph with dummy node
        pos[len(gdf)] = (min(gdf.centroid.x), min(gdf.centroid.y))
    nx.draw_networkx(G,
                     pos=pos,
                     ax=base,
                     node_size=1,
                     width=.5,
                     linewidths=.5,
                     with_labels=False,
                     edge_color=edge_colors)
    base.axis('off')
    return base


def politics_map(gdf, district_df, leaf_nodes, solution, figsize=(10,10)):

    districting = {ix: leaf_nodes[ix]['area'] for ix in solution['solution_ixs']}
    politics = district_df.loc[districting.keys(), 'mean']
    
    inv_map = {block: k for k, district in districting.items()
               for block in district}

    gdf['district'] = pd.Series(inv_map)

    shapes = []
    colors = []
    for name, group in gdf.groupby('district'):
        shapes.append(group.geometry.unary_union)
        colors.append(politics[name])
    shape_series = gpd.GeoSeries(shapes)

    map_gdf = gpd.GeoDataFrame({'geometry': shape_series,
                                'color': pd.Series(colors)})
    ax = map_gdf.plot(column='color', figsize=figsize, edgecolor='black', lw=1,
                      cmap='seismic', vmin=.35, vmax=.65)
    gdf.plot(ax=ax, facecolor='none', edgecolor='white', lw=.05)
    ax.axis('off')
    return map_gdf