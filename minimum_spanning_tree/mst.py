import pandas as pd
import numpy as np
import networkx as nx
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


def spanning_tree_cost(A, tree):
    """Return the cost of the given spanning tree.
    
    Args:
        A (np.ndarray): An adjacency matrix representing this graph.
        tree (List): List of edges in the spanning tree.
    """
    return sum([A[edge] for edge in tree])


# --------------
# MST Heuristics
# --------------

def prims(A, i):
    """Run Prim's algorithm on the given graph starting from node i.
    
    Args:
        A (np.ndarray): An adjacency matrix representing this graph.
        i (int): Index of the node to start from.
    """
    tree = []
    unvisited = list(range(len(A)))
    unvisited.remove(i)
    visited = [i]
    while len(unvisited) > 0:
        possible = {(i,j) : A[i,j] for j in unvisited for i in visited if A[i,j] >= 0}
        u,v = min(possible, key=possible.get)
        unvisited.remove(v)
        visited.append(v)
        tree.append((u,v))
    return tree


def kruskals(A):
    """Run Kruskal's algorithm on the given graph.
    
    Args:
        A (np.ndarray): An adjacency matrix representing this graph.
    """
    edges = {(i,j) : A[i,j] for i in range(len(A)) for j in range(i) if A[i,j] >= 0}
    edges = list(dict(sorted(edges.items(), key=lambda item: item[1])))
    tree = []
    forest = {i:i for i in range(len(A))}
    i = 0
    while len(tree) < len(A) - 1:
        u,v = edges[i]
        x = forest[u]
        y = forest[v]
        if x != y:
            for k in [k for k,v in forest.items() if v == y]:
                forest[k] = x
            tree.append((u,v))
        i += 1  
    return tree


def reverse_kruskals(A):
    """Run reverse Kruskal's algorithm on the given graph.
    
    Args:
        A (np.ndarray): An adjacency matrix representing this graph.
    """
    edges = {(i,j) : A[i,j] for i in range(len(A)) for j in range(i) if A[i,j] >= 0}
    edges = list(dict(sorted(edges.items(), key=lambda item: item[1], reverse=True)))
    G = nx.Graph()
    for i in range(len(A)):
        G.add_node(i)
    G.add_edges_from(edges)
    i = 0
    while len(G.edges) > len(A) - 1:
        u,v = edges[i]
        G.remove_edge(u,v)
        if not nx.is_connected(G):
            G.add_edge(u,v)
        i += 1  
    return G.edges


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

def plot_tour(nodes, edges, width=900, height=500):
    """Plot the graph given by the list of nodes and edges."""
    edges['u_pos'] = edges['u'].apply(lambda x: tuple(nodes.loc[x]))
    edges['v_pos'] = edges['v'].apply(lambda x: tuple(nodes.loc[x]))

    plot = blank_plot(nodes['x'], nodes['y'], plot_width=width, plot_height=height)
    
    xs = [[row['u_pos'][0], row['v_pos'][0]] for index, row in edges.iterrows()]
    ys = [[row['u_pos'][1], row['v_pos'][1]] for index, row in edges.iterrows()]
    plot.multi_line(xs, ys, line_color='gray', line_width=5)
    plot.circle(nodes['x'], nodes['y'], size=12, line_color='steelblue', fill_color='steelblue')
    lbl_source = ColumnDataSource(data=dict(x=[np.mean(i) for i in xs],
                                            y=[np.mean(i) for i in ys],
                                            text=edges['weight']))
    labels = LabelSet(x='x', y='y', text='text', source=lbl_source, render_mode='canvas')
    plot.add_layout(labels)
    
    # create layout
    grid = gridplot([[plot]], 
                    plot_width=width, plot_height=height,
                    toolbar_location = None,
                    toolbar_options={'logo': None})
    
    show(grid)
