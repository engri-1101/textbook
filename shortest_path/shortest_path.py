import pandas as pd
import numpy as np
import math
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


def shortest_path_tree_edges(nodes, prev):
    """Return edges of a shortest path tree given by prev."""
    tree = [(k,v) for k,v in prev.items() if not math.isnan(v)]
    xs = [[nodes.iloc[edge[0]]['x'], nodes.iloc[edge[1]]['x']] for edge in tree]
    ys = [[nodes.iloc[edge[0]]['y'], nodes.iloc[edge[1]]['y']] for edge in tree]
    return xs, ys


def create_table(dist, prev, S):
    """Return table for this iteration."""
    df = pd.DataFrame({'label': dist.copy(), 'prev': prev.copy()})
    df['label'] = ['%.1f' % df['label'][i] + '*'*(i in S) for i in range(len(df['label']))]
    df['prev'] = df['prev'].apply(lambda x: '-' if math.isnan(x) else int(x))
    df = df.T
    df.columns = df.columns.astype(str)
    return df.reset_index()

# ---------
# Algorithm
# ---------

def dijkstras(A, s=0, iterations=True):
    '''Execute Dijkstra's algorithm from source s on the given graph.
    
    Args:
        A (np.ndarray): An adjacency matrix representing this graph.
        s (int): Source vertex to run the algorithm from.
        iterations (bool): True iff all iterations should be returned.
    '''
    dist = {i: float('inf') for i in range(len(A))}
    prev = {i: float('nan') for i in range(len(A))}
    dist[s] = 0
    S = []
    F = [s]
    tables = [create_table(dist, prev, S)]
    prevs = [prev.copy()]
    marks = [S.copy()]
    while len(F) > 0:
        F.sort(reverse=True, key=lambda x: dist[x])
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
        tables.append(create_table(dist, prev, S))
        prevs.append(prev.copy())
        marks.append(S.copy())
    return marks, prevs, tables if iterations else prev


# ------------------
# Plotting functions
# ------------------

increment = """
if ((parseInt(n.text) + 1) < source.data['iteration_nodes'].length) {
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
    plot.toolbar.active_drag = None
    plot.toolbar.active_scroll = None
    return plot

def plot_shortest_path_tree(nodes, edges, prev, width=900, height=500):
    """Plot the heuristic executed on nodes and edges.
    
    Args:
        nodes (pd.DataFrame): Dataframe of nodes with their x,y positions.
        edges (pd.DataFrame): Dataframe of edges (pairs of nodes) and weights.
        prev (Dict): Previous attribute for every edge.
    """
    plot = blank_plot(nodes['x'], nodes['y'], plot_width=width, plot_height=height)
    
    tree_edge_xs, tree_edge_ys = shortest_path_tree_edges(nodes, prev)
    
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
    
    
def plot_dijkstras(nodes, edges, source=0, width=900, height=500):
    """Plot the Dijkstra's algorithm executed on nodes and edges.
    
    Args:
        nodes (pd.DataFrame): Dataframe of nodes with their x,y positions.
        edges (pd.DataFrame): Dataframe of edges (pairs of nodes) and weights.
    """
    plot = blank_plot(nodes['x'], nodes['y'], plot_width=width, plot_height=height)
    
    # get every iteration of the algorithm
    A = adjacency_matrix(nodes, edges)
    marks, prevs, tables = dijkstras(A, s=source, iterations=True)
    
    iteration_xs = []
    iteration_ys = []
    iteration_nodes = marks
    iteration_tables = [table.to_dict(orient='list') for table in tables]
    for prev in prevs:
        xs, ys = shortest_path_tree_edges(nodes, prev)
        iteration_xs.append(xs)
        iteration_ys.append(ys) 
    
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
    nodes.at[source, 'line_color'] = 'steelblue'
    nodes.at[source, 'fill_color'] = 'steelblue'
    edges['line_color'] = 'lightgray'
    
    # data sources
    source = ColumnDataSource(data={'iteration_xs': iteration_xs,
                                    'iteration_ys' : iteration_ys,
                                    'iteration_nodes' : iteration_nodes,
                                    'iteration_tables' : iteration_tables})
    table_src = ColumnDataSource(data=iteration_tables[0])
    tree_edge_src = ColumnDataSource(data={'xs': iteration_xs[0],
                                           'ys': iteration_ys[0]})
    nodes_src = ColumnDataSource(data=nodes.to_dict(orient='list'))
    edges_src = ColumnDataSource(data=edges.to_dict(orient='list'))
    labels_src = ColumnDataSource(data={'x': [np.mean(i) for i in edges['xs']],
                                        'y': [np.mean(i) for i in edges['ys']],
                                        'text': edges['weight']})
    
    # glyphs
    n = Div(text='0', width=width, align='center')
    done = Div(text='', width=int(width/2), align='center')  
    plot.multi_line('xs', 'ys', line_color='line_color', hover_line_color='black',
                    line_width=6, nonselection_line_alpha=1, source=edges_src)
    plot.multi_line('xs', 'ys', line_color='black', line_width=6, source=tree_edge_src)
    nodes_glyph = plot.circle('x', 'y', size=12, line_color='line_color', 
                               fill_color='fill_color', nonselection_fill_alpha=1, source=nodes_src)
    labels = LabelSet(x='x', y='y', text='text', render_mode='canvas', source=labels_src)
    plot.add_layout(labels)
    
    # table
    columns = ([TableColumn(field='index', title='')] + 
               [TableColumn(field=str(i), title=str(i)) for i in range(len(iteration_tables[0])-1)])
    table = DataTable(source=table_src, columns=columns, height=80, width=width, background='white', index_position=None, 
                     editable=False, reorderable=False, sortable=False, selectable=False)
    
    # --------------
    # CUSTOM JS CODE
    # --------------
     
    update = """    
    if (iteration == source.data['iteration_nodes'].length - 1) {
        done.text = "done."
    } else {
        done.text = ""
    }

    tree_edge_src.data['xs'] = source.data['iteration_xs'][iteration]
    tree_edge_src.data['ys'] = source.data['iteration_ys'][iteration]
    table_src.data = source.data['iteration_tables'][iteration]
    
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
    next_button.js_on_click(CustomJS(args=dict(source=source, nodes_src=nodes_src, table_src=table_src,
                                               tree_edge_src=tree_edge_src, done=done, n=n), code=next_btn_code))
    prev_button = Button(label="Previous", button_type="success", width_policy='fit', sizing_mode='scale_width')
    prev_button.js_on_click(CustomJS(args=dict(source=source, nodes_src=nodes_src, table_src=table_src,
                                               tree_edge_src=tree_edge_src, done=done, n=n), code=prev_btn_code))
    
    
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
