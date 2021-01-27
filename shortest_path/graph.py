import math
import pickle
import numpy as np
import pandas as pd
import networkx as nx
from ortools.constraint_solver import pywrapcp
from random import randrange
from bokeh.plotting import figure, show
from bokeh.io import output_notebook, show
from bokeh.models.glyphs import Text
from bokeh.tile_providers import get_provider, Vendors
from bokeh.models.widgets.markups import Div
from bokeh.models.widgets.tables import TableColumn, DataTable
from bokeh.layouts import layout, row, column, gridplot
from bokeh.models import (GraphRenderer, Circle, MultiLine, StaticLayoutProvider,
                          HoverTool, TapTool, EdgesAndLinkedNodes, NodesAndLinkedEdges,
                          ColumnDataSource, LabelSet, NodesOnly, Button, CustomJS)


# --------------
# Graph Building
# --------------

def distance_matrix(nodes, manhattan=True):
    """Compute the distance matrix between the nodes.

    Nodes dataframe can have both start and ending locations by having
    columns x_start, y_start and x_end, y_end

    Args:
        nodes (pd.DataFrame): Dataframe of nodes with at least (x,y) positions.
        manhattan (bool): return manhattan distance matrix if true. Otherwise, return euclidian.
    """
    if 'x_start' not in nodes.columns:
        A = np.array(list(zip(nodes['x'].tolist(), nodes['y'].tolist())))
        B = A
    else:
        A = np.array(list(zip(nodes['x_start'].tolist(), nodes['y_start'].tolist())))
        B = np.array(list(zip(nodes['x_end'].tolist(), nodes['y_end'].tolist())))

    if manhattan:
        return np.abs(A[:,0,None] - B[:,0]) + np.abs(A[:,1,None] - B[:,1])
    else:
        p1 = np.sum(A**2, axis=1)[:, np.newaxis]
        p2 = np.sum(B**2, axis=1)
        p3 = -2 * np.dot(A,B.T)
        return np.sqrt(p1+p2+p3)


def create_network(nodes, edges=None, directed=False):
    """Return networkx graph representing list of nodes/edges.

    If no edges are given, defaults to generating all edges with
    weight equivalent to the euclidean distance between the nodes.

    Args:
        nodes (pd.DataFrame): Dataframe of nodes with positional columns (x,y).
        edges (pd.DataFrame): Dataframe of edges (u,v) with weight w.
        directed (bool): True iff graph is directed (defaults to False).
    """
    if edges is None:
        G = nx.convert_matrix.from_numpy_matrix(A=distance_matrix(nodes),
                                                create_using=nx.DiGraph if directed else nx.Graph)
    else:
        G = nx.convert_matrix.from_pandas_edgelist(df=edges,  source='u', target='v', edge_attr='weight',
                                                   create_using=nx.DiGraph if directed else nx.Graph)
    for attr in nodes.columns:
        nx.set_node_attributes(G, pd.Series(nodes[attr]).to_dict(), attr)
    return G


# ----------
# Algorithms
# ----------

def dijkstras(G, s=0, iterations=False):
    '''Execute Dijkstra's algorithm on graph G from source s.

    Args:
        G (nx.Graph): Networkx graph.
        s (int): Source vertex to run the algorithm from.
        iterations (bool): True iff all iterations should be returned.
    '''
    # Helper functions
    def create_table(dist, prev, S):
        """Return table for this iteration."""
        df = pd.DataFrame({'label': dist.copy(), 'prev': prev.copy()})
        df['label'] = ['%.1f' % df['label'][i] + '*'*(i in S) for i in range(len(df['label']))]
        df['prev'] = df['prev'].apply(lambda x: '-' if math.isnan(x) else int(x))
        df = df.T
        df.columns = df.columns.astype(str)
        return df.reset_index()

    def edges_from_prev(prev):
        """Return the edges in the shortest path tree defined by prev."""
        return [(k,v) for k,v in prev.items() if not math.isnan(v)]

    dist = {i: float('inf') for i in range(len(G))}
    prev = {i: float('nan') for i in range(len(G))}
    dist[s] = 0
    S = []
    F = [s]

    tables = [create_table(dist, prev, S)]
    prevs = [edges_from_prev(prev)]
    marks = [S.copy()]

    while len(F) > 0:
        F.sort(reverse=True, key=lambda x: dist[x])
        f = F.pop()
        S.append(f)
        for w in nx.all_neighbors(G,f):
            if w not in S and w not in F:
                dist[w] = dist[f] + G[f][w]['weight']
                prev[w] = f
                F.append(w)
            else:
                if dist[f] + G[f][w]['weight'] < dist[w]:
                    dist[w] = dist[f] + G[f][w]['weight']
                    prev[w] = f
        tables.append(create_table(dist, prev, S))
        prevs.append(edges_from_prev(prev))
        marks.append(S.copy())
    return (marks, prevs, tables) if iterations else edges_from_prev(prev)


# --------
# Plotting
# --------

# JAVASCRIPT

increment = """
if ((parseInt(n.text) + 1) < source.data['nodes'].length) {
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

iteration_update = """
if (iteration == source.data['nodes'].length - 1) {
    done.text = "done."
} else {
    done.text = ""
}

edge_subset_src.data['xs'] = source.data['edge_xs'][iteration]
edge_subset_src.data['ys'] = source.data['edge_ys'][iteration]
table_src.data = source.data['tables'][iteration]

var in_tree = source.data['nodes'][iteration]

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
edge_subset_src.change.emit()
"""

# HELPER FUNCTIONS


def graph_range(x, y):
    """Return graph range containing the given points."""
    min_x, max_x = min(x), max(x)
    x_margin = 0.085*(max_x - min_x)
    min_x, max_x = min_x - x_margin, max_x + x_margin
    min_y, max_y = min(y), max(y)
    y_margin = 0.085*(max_y - min_y)
    min_y, max_y = min_y - y_margin, max_y + y_margin
    return min_x, max_x, min_y, max_y


def blank_plot(G, plot_width, plot_height):
    """Return a blank bokeh plot."""
    min_x, max_x, min_y, max_y = graph_range(nx.get_node_attributes(G,'x').values(),
                                             nx.get_node_attributes(G,'y').values())
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
    plot.toolbar.active_drag = None
    plot.toolbar.active_scroll = None
    return plot


def set_edge_positions(G):
    """Add edge attribute with positional data."""
    nx.set_edge_attributes(G, {(u,v) : (G.nodes[u]['x'], G.nodes[v]['x']) for u,v in G.edges}, 'xs')
    nx.set_edge_attributes(G, {(u,v) : (G.nodes[u]['y'], G.nodes[v]['y']) for u,v in G.edges}, 'ys')


def set_graph_colors(G, edges=[]):
    """Add node/edge attribute with color data. Highlight edges."""
    for u in G.nodes:
        G.nodes[u]['line_color'] = 'steelblue'
        G.nodes[u]['fill_color'] = 'steelblue'
    for u,v in G.edges:
        G[u][v]['line_color'] = 'lightgray'
    for u,v in edges:
        G[u][v]['line_color'] = 'black'


def graph_sources(G):
    """Return data sources for the graph G."""
    nodes_src = ColumnDataSource(data=pd.DataFrame([G.nodes[u] for u in sorted(G.nodes())]).to_dict(orient='list'))
    edges_src = ColumnDataSource(data=pd.DataFrame([G[u][v] for u,v in G.edges()]).to_dict(orient='list'))
    labels_src = ColumnDataSource(data={'x': [np.mean(i) for i in nx.get_edge_attributes(G, 'xs').values()],
                                        'y': [np.mean(i) for i in nx.get_edge_attributes(G, 'ys').values()],
                                        'text': list(nx.get_edge_attributes(G,'weight').values())})
    return nodes_src, edges_src, labels_src

# TODO: Ensure nodes are plotted above edges
def graph_glyphs(plot, nodes_src, edges_src, labels_src):
    """Add and return glyphs for nodes and edges"""
    edges_glyph = plot.multi_line(xs='xs', ys='ys',
                                  line_color='line_color', hover_line_color='black',
                                  line_width=6, nonselection_line_alpha=1,
                                  source=edges_src)
    nodes_glyph = plot.circle(x='x', y='y', size=12,
                              line_color='line_color', fill_color='fill_color',
                              nonselection_fill_alpha=1, source=nodes_src)
    labels = LabelSet(x='x', y='y', text='text', render_mode='canvas', source=labels_src)
    plot.add_layout(labels)
    return edges_glyph, nodes_glyph


# MAIN FUNCTIONS


def plot_graph(G, edges=[], width=900, height=500):
    """Plot the graph G.

    Args:
        G (nx.Graph): Networkx graph.
        edges (List): Edges to highlight.
    """
    G = G.copy()
    plot = blank_plot(G, plot_width=width, plot_height=height)

    set_edge_positions(G)
    set_graph_colors(G, edges)

    nodes_src, edges_src, labels_src = graph_sources(G)
    edges_glyph, nodes_glyph = graph_glyphs(plot, nodes_src, edges_src, labels_src)

    plot.add_tools(HoverTool(tooltips=[("Node", "$index")], renderers=[nodes_glyph]))
    grid = gridplot([[plot]],
                    plot_width=width, plot_height=height,
                    toolbar_location = None,
                    toolbar_options={'logo': None})
    show(grid)


def plot_graph_iterations(G, nodes=[], edges=[], tables=None, width=900, height=500):
    """Plot the graph G with iterations of edges, nodes, and tables.

    Args:
        G (nx.Graph): Networkx graph.
        nodes (List): Nodes to highlight at each iteration.
        edges (List): Edges to highlight at each iteration.
        tables (List): Tables at each iteration.
    """
    G = G.copy()
    plot = blank_plot(G, plot_width=width, plot_height=height)

    set_edge_positions(G)
    set_graph_colors(G)
    for u in G.nodes:
        G.nodes[u]['line_color'] = '#EA8585'
        G.nodes[u]['fill_color'] = '#EA8585'

    edge_xs = []
    edge_ys = []
    tables = [table.to_dict(orient='list') for table in tables]
    for i in range(len(edges)):
        xs = [G[u][v]['xs'] for u,v in edges[i]]
        ys = [G[u][v]['ys'] for u,v in edges[i]]
        edge_xs.append(xs)
        edge_ys.append(ys)

    # data sources
    nodes_src, edges_src, labels_src = graph_sources(G)
    source = ColumnDataSource(data={'edge_xs': edge_xs,
                                    'edge_ys' : edge_ys,
                                    'nodes' : nodes,
                                    'tables' : tables})
    edge_subset_src = ColumnDataSource(data={'xs': edge_xs[0],
                                             'ys': edge_ys[0]})
    table_src = ColumnDataSource(data=tables[0])


    # glyphs
    n = Div(text='0', width=width, align='center')
    done = Div(text='', width=int(width/2), align='center')
    edges_glyph, nodes_glyph = graph_glyphs(plot, nodes_src, edges_src, labels_src)
    plot.multi_line('xs', 'ys', line_color='black', line_width=6, source=edge_subset_src)
    columns = ([TableColumn(field='index', title='')] +
               [TableColumn(field=str(i), title=str(i)) for i in range(len(tables[0])-1)])
    table = DataTable(source=table_src, columns=columns, height=80, width=width, background='white', index_position=None,
                      editable=False, reorderable=False, sortable=False, selectable=False)

    # Javascript
    next_btn_code = increment + iteration_update
    prev_btn_code = decrement + iteration_update

    # buttons
    next_button = Button(label="Next", button_type="success", width_policy='fit', sizing_mode='scale_width')
    next_button.js_on_click(CustomJS(args=dict(source=source, nodes_src=nodes_src, edge_subset_src=edge_subset_src,
                                               table_src=table_src, done=done, n=n), code=next_btn_code))
    prev_button = Button(label="Previous", button_type="success", width_policy='fit', sizing_mode='scale_width')
    prev_button.js_on_click(CustomJS(args=dict(source=source, nodes_src=nodes_src, edge_subset_src=edge_subset_src,
                                               table_src=table_src, done=done, n=n), code=prev_btn_code))

    plot.add_tools(HoverTool(tooltips=[("Node", "$index")], renderers=[nodes_glyph]))

    # create layout
    grid = gridplot([[plot],
                     [table],
                     [row(prev_button, next_button, max_width=width, sizing_mode='stretch_both')],
                     [row(done)]],
                    plot_width=width, plot_height=height,
                    toolbar_location = None,
                    toolbar_options={'logo': None})

    show(grid)


def plot_dijkstras(G, source=0, width=900, height=500):
    """Plot the Dijkstra's algorithm executed on nodes and edges.

    Args:
        G (nx.Graph): Networkx graph.
        s (int): Source vertex to run the algorithm from.
    """
    nodes, edges, tables = dijkstras(G, s=source, iterations=True)
    plot_graph_iterations(G, nodes=nodes, edges=edges, tables=tables, width=width, height=height)
