import pandas as pd
import numpy as np
from bokeh.plotting import figure, show
from bokeh.io import output_notebook, show
from bokeh.models.glyphs import Text
from bokeh.tile_providers import get_provider, Vendors
from bokeh.models.widgets.markups import Div
from bokeh.layouts import layout, row, column, gridplot
from bokeh.models import (GraphRenderer, Circle, MultiLine, StaticLayoutProvider,
                          HoverTool, TapTool, EdgesAndLinkedNodes, NodesAndLinkedEdges,
                          ColumnDataSource, LabelSet, NodesOnly, Button, CustomJS)


# ----------------
# Create instances
# ----------------

def adjacency_matrix(nodes, edges):
    """Create an adjacency matrix given the list of nodes and edges."""
    A = -np.ones((len(nodes), len(nodes)))
    for index, row in edges.iterrows():
        A[row['u'], row['v']] = row['weight']
        A[row['v'], row['u']] = row['weight']
    return A


# ---------
# Algorithm
# ---------

def dijkstras(A, s=0):
    '''Execute Dijkstra's algorithm from source s on the given graph.
    
    Args:
        A (np.ndarray): An adjacency matrix representing this graph.
        s (int): Source vertex to run the algorithm from.
    '''
    dist = {i: float('inf') for i in range(len(A))}
    prev = {i: None for i in range(len(A))}
    dist[s] = 0
    S = []
    F = [s]
    while len(F) > 0:
        F.sort(key=lambda x: dist[x])
        f = F.pop()
        S.append(f)
        for w in np.where(A[f] != -1)[0]:
            if w not in S and w not in F:
                dist[w] = dist[f] + A[f,w]
                prev[w] = f
                F.append(w)
            else:
                if dist[f] + A[f,w] < dist[w]:
                    dist[w] = dist[f] + A[f,w]
                    prev[w] = f
    return prev


# ------------------
# Plotting functions
# ------------------

def graph_range(x, y):
    """Return graph range for given points."""
    min_x, max_x = min(x), max(x)
    x_margin = 0.085*(max_x - min_x)
    min_x, max_x = min_x - x_margin, max_x + x_margin
    min_y, max_y = min(y), max(y)
    y_margin = 0.085*(max_y - min_y)
    min_y, max_y = min_y - y_margin, max_y + y_margin
    return min_x, max_x, min_y, max_y


def blank_plot(x, y, plot_width, plot_height):
    """Create a blank bokeh plot."""
    min_x, max_x, min_y, max_y = graph_range(x, y)
    plot = figure(x_range=(min_x, max_x), 
                  y_range=(min_y, max_y), 
                  title="", 
                  plot_width=plot_width,
                  plot_height=plot_height)
    plot.toolbar.logo = None
    plot.toolbar_location = None
    plot.xgrid.grid_line_color = None
    plot.ygrid.grid_line_color = None
    plot.xaxis.visible = False
    plot.yaxis.visible = False 
    plot.background_fill_color = None
    plot.border_fill_color = None
    plot.outline_line_color = None
    return plot

def plot_shortest_path_tree(nodes, edges, tree, width=900, height=500):
    """Plot the heuristic executed on nodes and edges.
    
    Args:
        nodes (pd.DataFrame): Dataframe of nodes with their x,y positions.
        edges (pd.DataFrame): Dataframe of edges (pairs of nodes) and weights.
        tree (List): List of edges in the shortest path tree.
    """
    plot = blank_plot(nodes['x'], nodes['y'], plot_width=width, plot_height=height)
    
    tree_edge_xs = [[nodes.iloc[edge[0]]['x'], nodes.iloc[edge[1]]['x']] for edge in tree]
    tree_edge_ys = [[nodes.iloc[edge[0]]['y'], nodes.iloc[edge[1]]['y']] for edge in tree]
    
    # create copy of dfs
    nodes = nodes.copy()
    edges = edges.copy()
    
    # create cooordinates for edges
    edges['u_pos'] = edges['u'].apply(lambda x: tuple(nodes.loc[x]))
    edges['v_pos'] = edges['v'].apply(lambda x: tuple(nodes.loc[x]))
    edges['xs'] = [[row['u_pos'][0], row['v_pos'][0]] for index, row in edges.iterrows()]
    edges['ys'] = [[row['u_pos'][1], row['v_pos'][1]] for index, row in edges.iterrows()]
    
    # set inital colors of edges and nodes
    nodes['line_color'] = 'steelblue'
    nodes['fill_color'] = 'steelblue'
    edges['line_color'] = 'lightgray'
    
    # data sources
    tree_edge_src = ColumnDataSource(data={'xs': tree_edge_xs,
                                           'ys': tree_edge_ys})
    nodes_src = ColumnDataSource(data=nodes.to_dict(orient='list'))
    edges_src = ColumnDataSource(data=edges.to_dict(orient='list'))
    labels_src = ColumnDataSource(data={'x': [np.mean(i) for i in edges['xs']],
                                        'y': [np.mean(i) for i in edges['ys']],
                                        'text': edges['weight']})
    
    # glyphs
    plot.multi_line('xs', 'ys', line_color='line_color', hover_line_color='black',
                    line_width=6, nonselection_line_alpha=1, source=edges_src)
    plot.multi_line('xs', 'ys', line_color='black', line_width=6, source=tree_edge_src)
    plot.circle('x', 'y', size=12, line_color='line_color', 
                fill_color='fill_color', nonselection_fill_alpha=1, source=nodes_src)
    labels = LabelSet(x='x', y='y', text='text', render_mode='canvas', source=labels_src)
    plot.add_layout(labels)
    
    # create layout
    grid = gridplot([[plot]],
                    plot_width=width, plot_height=height,
                    toolbar_location = None,
                    toolbar_options={'logo': None})
    
    show(grid)
