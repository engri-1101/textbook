# imports
import os
import math
import pickle
import numpy as np
import networkx as nx
import itertools
import pandas as pd
from polyomino import *
import geopandas as gpd
from scipy.stats import t
from bokeh.layouts import layout, row, column, gridplot
from bokeh.plotting import figure, output_file, show
from bokeh.io import output_notebook, show
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
    with open(os.path.join(OPT_DATA_PATH, 'G.p'), 'rb') as f:
        G = pickle.load(f)
    return G


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
           for i, geo in gdf.geometry.items()}
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

# ------------------
# Functions for grid
# ------------------

small_example = np.array([[0,1,1,1,0],
                          [0,0,1,1,1],
                          [1,0,1,1,0]])
large_example = np.array([[1., 0., 1., 1., 0., 0.],
                          [1., 1., 1., 1., 1., 1.],
                          [0., 1., 1., 1., 1., 1.],
                          [1., 1., 0., 0., 1., 0.],
                          [1., 0., 0., 0., 1., 1.],
                          [1., 1., 0., 0., 1., 1.],
                          [1., 1., 1., 1., 1., 0.]])

# 9x5 example solution gerrymandered for red: [4842, 24453, 59212, 60208, 65129]

def feasible_districts_on_grid(grid, k):
    """Get a dataframe of feasible districts on this grid."""
    n,m = grid.shape
    D_coordinates = []
    D_indices = []
    polyominos = [list(poly) for poly in generate(k)]
    for poly in polyominos:
        x,y = zip(*poly)
        assert min(x) == 0
        assert min(y) == 0
        w = max(x)
        h = max(y)
        x_np = np.array(x)
        y_np = np.array(y)
        for i in range(n-h):
            for j in range(m-w):
                d = list(zip(np.array(y_np)+i, np.array(x_np)+j))
                D_coordinates.append(d)
                D_indices.append([m*i + j for i,j in d])
    return D_coordinates, D_indices
    
    
def create_districts_df(grid, k):
    """Create a dataframe of districts and compute statistics for each."""
    n,m = grid.shape
    district_df = {}
    even_50_pct = math.ceil(k/2)
    D_coordinates, D_indices = feasible_districts_on_grid(grid,k)
    for i in range(len(D_coordinates)):
        row = {}
        row['tracts'] = D_indices[i]
        row['tract_coord'] = D_coordinates[i]
        votes = [grid[i,j] for i,j in D_coordinates[i]]
        D_votes = votes.count(0)
        R_votes = votes.count(1)
        row['D_votes'] = D_votes
        row['R_votes'] = R_votes
        if D_votes > R_votes:
            D_wasted = D_votes - even_50_pct
            R_wasted = R_votes
            row['R_win'] = False
        else:
            D_wasted = D_votes
            R_wasted = R_votes - even_50_pct
            row['R_win'] = True
        row['efficiency_gap'] = (D_wasted - R_wasted) / k
        
        x,y = list(zip(*D_coordinates[i]))
        w = max(max(x) - min(x), max(y) - min(y)) + 1
        row['square_roeck'] = (len(x) / (w**2))
     
        district_df[i] = row
    return pd.DataFrame(district_df).T


def grid_district_matrix(grid,k):
    """Return a district matrix for the grid with size k districts."""
    n,m = grid.shape
    D = feasible_districts_on_grid(grid,k)[1]
    A = np.zeros((n*m, len(D)))
    for j in range(len(D)):
        for i in D[j]:
            A[i,j] = 1
    return A


def blank_grid_plot(n,m, box_size=30):
    """Create a blank bokeh plot."""
    plt = figure(x_range=(0, m), 
                 y_range=(0, n), 
                 title="", 
                 width=box_size*m,
                 height=box_size*n)
    plt.toolbar.logo = None
    plt.toolbar_location = None
    plt.xgrid.grid_line_color = None
    plt.ygrid.grid_line_color = None
    plt.xaxis.visible = False
    plt.yaxis.visible = False 
    plt.background_fill_color = None
    plt.border_fill_color = None
    plt.outline_line_color = None
    return plt


def grid_plot(grid,color_map={1:'#DC0000', 0:'#195495'},line_color='white'):
    """Return a plot of the grid."""
    n,m = grid.shape
    plt = blank_grid_plot(n,m)
    top = [i+1 for i in range(n) for j in range(m)]
    bottom = [i for i in range(n) for j in range(m)]
    left = [i for j in range(n) for i in range(m)]
    right = [i+1 for j in range(n) for i in range(m)]
    color = [color_map[i] for i in grid.flatten()]
    plt.quad(top=top, bottom=bottom, left=left, right=right, color=color, line_color=line_color, line_width=2)
    return plt


def plot_feasible_districts(grid,k,columns=5):
    """Plot all the feasible districts of size k on an the grid."""
    n,m = grid.shape
    D = feasible_districts_on_grid(grid,k)[0]
    rows = math.ceil(len(D) / columns)
    plots = [[] for r in range(rows)]
    for d in range(len(D)):
        M = np.zeros((n,m))
        for i,j in D[d]:
            M[i,j] = 1
        plots[d % rows].append(grid_plot(M,color_map={1:'black', 0:'white'},line_color='gray'))
    grid = gridplot(plots,
                    toolbar_location = None,
                    toolbar_options={'logo': None})   
    show(grid)
    

def add_grid_district(plt, grid, district_df, d):
    """Add the given district d to the grid plot."""
    n,m = grid.shape
    indices = district_df.loc[d]['tracts']
    y,x = zip(*district_df.loc[d]['tract_coord'])
    for k in range(len(indices)):
        i = indices[k]
        # bottom, top, left, right
        has_side = [not j in indices for j in [i-m,i+m,i-1,i+1]]
        if i // m == 0:
            has_side[0] = True
        if i // m == n-1:
            has_side[1] = True
        if i % m == 0:
            has_side[2] = True
        if i % m == m-1:
            has_side[3] = True

        sides_x = [[x[k],x[k]+1], [x[k],x[k]+1], [x[k],x[k]], [x[k]+1,x[k]+1]]
        sides_x = [sides_x[i] for i in range(4) if has_side[i]]
        sides_y = [[y[k],y[k]], [y[k]+1,y[k]+1], [y[k],y[k]+1], [y[k],y[k]+1]]
        sides_y = [sides_y[i] for i in range(4) if has_side[i]]

        plt.multi_line(sides_x,sides_y, line_width=6, line_color='black', line_cap='round')


def plot_grid_districts(grid, district_df, districts):
    """Plot the grid with the given chosen districts."""
    n,m = grid.shape
    plt = grid_plot(grid)
    for d in districts:
        add_grid_district(plt, grid, district_df, d)
        
    show(plt)
    results = list(district_df.iloc[districts]['R_win'])
    print('R : %d, D : %d' % (results.count(True), results.count(False)))
    print('Efficiency Gap: %f' % (district_df.iloc[districts]['efficiency_gap'].mean()))
    print('Square Roeck: %f' % (district_df.iloc[districts]['square_roeck'].mean()))