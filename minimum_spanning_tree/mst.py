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

def prims(A, i, iterations=False):
    """Run Prim's algorithm on the given graph starting from node i.
    
    Args:
        A (np.ndarray): An adjacency matrix representing this graph.
        i (int): Index of the node to start from.
        iterations (bool): True iff the tree at every iteration should be returned.
    """
    tree = []
    tree_iterations = [[]]
    unvisited = list(range(len(A)))
    unvisited.remove(i)
    visited = [i]
    while len(unvisited) > 0:
        possible = {(i,j) : A[i,j] for j in unvisited for i in visited if A[i,j] >= 0}
        u,v = min(possible, key=possible.get)
        unvisited.remove(v)
        visited.append(v)
        tree.append((u,v))
        tree_iterations.append(list(tree))
    return tree_iterations if iterations else tree


def kruskals(A, iterations=False):
    """Run Kruskal's algorithm on the given graph.
    
    Args:
        A (np.ndarray): An adjacency matrix representing this graph.
        iterations (bool): True iff the tree at every iteration should be returned.
    """
    edges = {(i,j) : A[i,j] for i in range(len(A)) for j in range(i) if A[i,j] >= 0}
    edges = list(dict(sorted(edges.items(), key=lambda item: item[1])))
    tree = []
    tree_iterations = [[]]
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
            tree_iterations.append(list(tree))
        i += 1  
    return tree_iterations if iterations else tree


def reverse_kruskals(A, iterations=False):
    """Run reverse Kruskal's algorithm on the given graph.
    
    Args:
        A (np.ndarray): An adjacency matrix representing this graph.
        iterations (bool): True iff the tree at every iteration should be returned.
    """
    edges = {(i,j) : A[i,j] for i in range(len(A)) for j in range(i) if A[i,j] >= 0}
    edges = list(dict(sorted(edges.items(), key=lambda item: item[1], reverse=True)))
    G = nx.Graph()
    for i in range(len(A)):
        G.add_node(i)
    G.add_edges_from(edges)
    tree_iterations = [list(G.edges)]
    i = 0
    while len(G.edges) > len(A) - 1:
        u,v = edges[i]
        G.remove_edge(u,v)
        if not nx.is_connected(G):
            G.add_edge(u,v)
        else:
            tree_iterations.append(list(G.edges))
        i += 1  
    return tree_iterations if iterations else G.edges


# ------------------
# Plotting functions
# ------------------

increment = """
if ((parseInt(n.text) + 1) < source.data['costs'].length) {
    n.text = (parseInt(n.text) + 1).toString()
}
var iteration = parseInt(n.text)
"""

decrement = """
if ((parseInt(n.text) - 1) >= 0) {
    n.text = (parseInt(n.text) - 1).toString()
}
var iteration = parseInt(n.text)
"""

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

def plot_tree(nodes, edges, tree, width=900, height=500):
    """Plot the heuristic executed on nodes and edges.
    
    Args:
        nodes (pd.DataFrame): Dataframe of nodes with their x,y positions.
        edges (pd.DataFrame): Dataframe of edges (pairs of nodes) and weights.
        tree (List): List of edges in the spanning tree.
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
    cost = Div(text=str(spanning_tree_cost(adjacency_matrix(nodes, edges), tree)), width=int(width/2), align='center') 
    plot.multi_line('xs', 'ys', line_color='line_color', hover_line_color='black',
                    line_width=6, nonselection_line_alpha=1, source=edges_src)
    plot.multi_line('xs', 'ys', line_color='black', line_width=6, source=tree_edge_src)
    plot.circle('x', 'y', size=12, line_color='line_color', 
                fill_color='fill_color', nonselection_fill_alpha=1, source=nodes_src)
    labels = LabelSet(x='x', y='y', text='text', render_mode='canvas', source=labels_src)
    plot.add_layout(labels)
    
    # create layout
    grid = gridplot([[plot],
                     [row(cost)]], 
                    plot_width=width, plot_height=height,
                    toolbar_location = None,
                    toolbar_options={'logo': None})
    
    show(grid)


def plot_mst_algorithm(nodes, edges, alg, width=900, height=500):
    """Plot the heuristic executed on nodes and edges.
    
    Args:
        nodes (pd.DataFrame): Dataframe of nodes with their x,y positions.
        edges (pd.DataFrame): Dataframe of edges (pairs of nodes) and weights.
        alg (string): {'prims', 'kruskals', 'reverse_kruskals'}
    """
    plot = blank_plot(nodes['x'], nodes['y'], plot_width=width, plot_height=height)
    
    # get every iteration of the algorithm
    A = adjacency_matrix(nodes, edges)
    if alg == 'prims':
        iteration_edges = prims(A, 0, iterations=True)
    elif alg == 'kruskals':
        iteration_edges = kruskals(A, iterations=True)
    elif alg == 'reverse_kruskals':
        iteration_edges = reverse_kruskals(A, iterations=True)
 
    iteration_xs = []
    iteration_ys = []
    iteration_nodes = []
    for iter_edges in iteration_edges:
        iteration_xs.append([[nodes.iloc[edge[0]]['x'], nodes.iloc[edge[1]]['x']] for edge in iter_edges])
        iteration_ys.append([[nodes.iloc[edge[0]]['y'], nodes.iloc[edge[1]]['y']] for edge in iter_edges])
        iteration_nodes.append(list(set([item for sublist in iter_edges for item in sublist])))
    costs = [spanning_tree_cost(A,iter_edges) for iter_edges in iteration_edges]
    
    # create copy of dfs
    nodes = nodes.copy()
    edges = edges.copy()
    
    # create cooordinates for edges
    edges['u_pos'] = edges['u'].apply(lambda x: tuple(nodes.loc[x]))
    edges['v_pos'] = edges['v'].apply(lambda x: tuple(nodes.loc[x]))
    edges['xs'] = [[row['u_pos'][0], row['v_pos'][0]] for index, row in edges.iterrows()]
    edges['ys'] = [[row['u_pos'][1], row['v_pos'][1]] for index, row in edges.iterrows()]
    
    # set inital colors of edges and nodes
    if alg == 'reverse_kruskals':
        nodes['line_color'] = 'steelblue'
        nodes['fill_color'] = 'steelblue'
    else:
        nodes['line_color'] = '#EA8585'
        nodes['fill_color'] = '#EA8585'
    edges['line_color'] = 'lightgray'
    
    # data sources
    source = ColumnDataSource(data={'iteration_xs': iteration_xs,
                                    'iteration_ys' : iteration_ys,
                                    'iteration_nodes' : iteration_nodes,
                                    'costs' : costs})
    tree_edge_src = ColumnDataSource(data={'xs': iteration_xs[0],
                                           'ys': iteration_ys[0]})
    nodes_src = ColumnDataSource(data=nodes.to_dict(orient='list'))
    edges_src = ColumnDataSource(data=edges.to_dict(orient='list'))
    labels_src = ColumnDataSource(data={'x': [np.mean(i) for i in edges['xs']],
                                        'y': [np.mean(i) for i in edges['ys']],
                                        'text': edges['weight']})
    
    # glyphs
    n = Div(text='0', width=width, align='center')
    cost = Div(text=str(spanning_tree_cost(A, iteration_edges[0])), width=int(width/2), align='center') 
    done = Div(text='', width=int(width/2), align='center')  
    plot.multi_line('xs', 'ys', line_color='line_color', hover_line_color='black',
                    line_width=6, nonselection_line_alpha=1, source=edges_src)
    plot.multi_line('xs', 'ys', line_color='black', line_width=6, source=tree_edge_src)
    plot.circle('x', 'y', size=12, line_color='line_color', 
                fill_color='fill_color', nonselection_fill_alpha=1, source=nodes_src)
    labels = LabelSet(x='x', y='y', text='text', render_mode='canvas', source=labels_src)
    plot.add_layout(labels)
    
    # --------------
    # CUSTOM JS CODE
    # --------------
     
    update = """
    cost.text = source.data['costs'][iteration].toFixed(1)
    
    
    if (iteration == source.data['costs'].length - 1) {
        done.text = "done."
    } else {
        done.text = ""
    }

    tree_edge_src.data['xs'] = source.data['iteration_xs'][iteration]
    tree_edge_src.data['ys'] = source.data['iteration_ys'][iteration]
    
    var in_tree = source.data['iteration_nodes'][iteration]

    for (let i = 0; i < nodes_src.data['line_color'].length ; i++) {
        if (in_tree.includes(i)) {
            nodes_src.data['fill_color'][i] = 'steelblue'
            nodes_src.data['line_color'][i] = 'steelblue'
        } else {
            nodes_src.data['fill_color'][i] = '#EA8585'
            nodes_src.data['line_color'][i] = '#EA8585'
        }
    }
    
    nodes_src.change.emit()
    tree_edge_src.change.emit()
    """ 
    
    next_btn_code = increment + update
    prev_btn_code = decrement + update
    
    # add buttons
    next_button = Button(label="Next", button_type="success", width_policy='fit', sizing_mode='scale_width')
    next_button.js_on_click(CustomJS(args=dict(source=source, nodes_src=nodes_src,
                                               tree_edge_src=tree_edge_src,
                                               cost=cost, done=done, n=n), code=next_btn_code))
    prev_button = Button(label="Previous", button_type="success", width_policy='fit', sizing_mode='scale_width')
    prev_button.js_on_click(CustomJS(args=dict(source=source, nodes_src=nodes_src,
                                               tree_edge_src=tree_edge_src,
                                               cost=cost, done=done, n=n), code=prev_btn_code))
    
    
    # create layout
    grid = gridplot([[plot],
                     [row(prev_button, next_button, max_width=width, sizing_mode='stretch_both')],
                     [row(cost,done)]], 
                    plot_width=width, plot_height=height,
                    toolbar_location = None,
                    toolbar_options={'logo': None})
    
    show(grid)

    
def plot_create_tree(nodes, edges, width=900, height=500):
    """Plot the graph given by the list of nodes and edges.
    
    Args:
        nodes (pd.DataFrame): Dataframe of nodes with their x,y positions.
        edges (pd.DataFrame): Dataframe of edges (pairs of nodes) and weights.
        initial (int): The inital node to start prims algorithm from.
    """
    plot = blank_plot(nodes['x'], nodes['y'], plot_width=width, plot_height=height)
    
    # create copy of dfs
    nodes = nodes.copy()
    edges = edges.copy()
    
    # create cooordinates for edges
    edges['u_pos'] = edges['u'].apply(lambda x: tuple(nodes.loc[x]))
    edges['v_pos'] = edges['v'].apply(lambda x: tuple(nodes.loc[x]))
    edges['xs'] = [[row['u_pos'][0], row['v_pos'][0]] for index, row in edges.iterrows()]
    edges['ys'] = [[row['u_pos'][1], row['v_pos'][1]] for index, row in edges.iterrows()]
    
    # set inital colors of edges and nodes
    nodes['line_color'] = '#EA8585'
    nodes['fill_color'] = '#EA8585'
    edges['line_color'] = 'lightgray'
    
    # data sources
    source = ColumnDataSource(data={'tree_nodes': [],
                                    'tree_edges' : []})
    nodes_src = ColumnDataSource(data=nodes.to_dict(orient='list'))
    edges_src = ColumnDataSource(data=edges.to_dict(orient='list'))
    labels_src = ColumnDataSource(data={'x': [np.mean(i) for i in edges['xs']],
                                        'y': [np.mean(i) for i in edges['ys']],
                                        'text': edges['weight']})
    
    # glyphs
    cost = Div(text=str(0.0), width=int(width/3), align='center') 
    error_msg = Div(text='', width=int(width/3), align='center') 
    done = Div(text='', width=int(width/3), align='center')  
    edge_glyphs = plot.multi_line('xs', 'ys', line_color='line_color', hover_line_color='black',
                                  line_width=6, nonselection_line_alpha=1, source=edges_src)
    node_glyphs = plot.circle('x', 'y', size=13, line_color='line_color', 
                              fill_color='fill_color', nonselection_fill_alpha=1, source=nodes_src)
    labels = LabelSet(x='x', y='y', text='text', render_mode='canvas', source=labels_src)
    plot.add_layout(labels)
    
    # --------------
    # CUSTOM JS CODE
    # --------------
    
    on_hover = """
    source.data['last_index'] = cb_data.index.indices[0]
    """
     
    on_click = """ 
    var i = source.data['last_index']
    var u = edges_src.data['u'][i]
    var v = edges_src.data['v'][i]
    var w = edges_src.data['weight'][i]
    var tree_nodes = source.data['tree_nodes']
    var tree_edges = source.data['tree_edges']
    
    if (!tree_nodes.includes(u) || !tree_nodes.includes(v)) {
        if (!tree_nodes.includes(v)) {
            tree_nodes.push(v)
            nodes_src.data['line_color'][v] = 'steelblue'
            nodes_src.data['fill_color'][v] = 'steelblue'
        }
        if (!tree_nodes.includes(u)) {
            tree_nodes.push(u)
            nodes_src.data['line_color'][u] = 'steelblue'
            nodes_src.data['fill_color'][u] = 'steelblue'
        }
        edges_src.data['line_color'][i] = 'black'
        tree_edges.push((u,v))
        var prev_cost = parseFloat(cost.text)
        cost.text = (prev_cost + w).toFixed(1) 
        error_msg.text = ''
    } else {
        error_msg.text = 'You have selected an invalid edge.'
    }
    
    if (tree_nodes.length == nodes_src.data['x'].length) {
        done.text = 'done.'
    }
    
    source.change.emit()
    nodes_src.change.emit()
    edges_src.change.emit()
    """
    
    plot.add_tools(HoverTool(tooltips=None,
                             callback=CustomJS(args=dict(source=source), code=on_hover),
                             renderers=[edge_glyphs]),
                   TapTool(callback=CustomJS(args=dict(source=source, edges_src=edges_src, nodes_src=nodes_src, 
                                                       cost=cost, error_msg=error_msg, done=done), code=on_click),
                           renderers=[edge_glyphs]))
    
    # create layout
    grid = gridplot([[plot],
                     [row(cost,error_msg,done)]], 
                    plot_width=width, plot_height=height,
                    toolbar_location = None,
                    toolbar_options={'logo': None})
    
    show(grid)
