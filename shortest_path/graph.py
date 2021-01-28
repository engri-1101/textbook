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


def create_network(nodes, edges=None, directed=False, manhattan=True):
    """Return networkx graph representing list of nodes/edges.

    If no edges are given, defaults to generating all edges with
    weight equivalent to the euclidean distance between the nodes.

    Args:
        nodes (pd.DataFrame): Dataframe of nodes with positional columns (x,y).
        edges (pd.DataFrame): Dataframe of edges (u,v) with weight w.
        directed (bool): True iff graph is directed (defaults to False).
        manhattan (bool): use manhattan distance matrix if true. Otherwise, use euclidian.
    """
    if edges is None:
        G = nx.convert_matrix.from_numpy_matrix(A=distance_matrix(nodes, manhattan=manhattan),
                                                create_using=nx.DiGraph if directed else nx.Graph)
    else:
        G = nx.convert_matrix.from_pandas_edgelist(df=edges,  source='u', target='v', edge_attr='weight',
                                                   create_using=nx.DiGraph if directed else nx.Graph)
    for attr in nodes.columns:
        nx.set_node_attributes(G, pd.Series(nodes[attr]).to_dict(), attr)
    return G


def grid_instance(n, m, manhattan=True):
    """Return a graph G representing an n x m set of nodes.

    Args:
        n (int): width of the grid.
        m (int): height of the grid.
        manhattan (bool): use manhattan distance matrix if true. Otherwise, use euclidian.
    """
    nodes = pd.DataFrame()
    for i in range(n):
        for j in range(m):
            nodes = nodes.append({'name' : str((i,j)), 'x' : i, 'y' : j}, ignore_index=True)
    return create_network(nodes, directed=False, manhattan=manhattan)


# ----------
# Algorithms
# ----------

# SHORTEST PATH

def dijkstras(G, s=0, iterations=False):
    '''Run Dijkstra's algorithm on graph G from source s.

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

# MINIMUM SPANNING TREE (MST)

def prims(G, i, iterations=False):
    """Run Prim's algorithm on graph G starting from node i.

    Args:
        G (nx.Graph): Networkx graph.
        i (int): Index of the node to start from.
        iterations (bool): True iff the tree at every iteration should be returned.
    """
    tree = []
    trees = [[]]
    unvisited = list(range(len(G)))
    unvisited.remove(i)
    visited = [i]
    while len(unvisited) > 0:
        possible = {(u,v) : G[u][v]['weight'] for u in visited for v in unvisited if G.has_edge(u,v)}
        u,v = min(possible, key=possible.get)
        unvisited.remove(v)
        visited.append(v)
        tree.append((u,v))
        trees.append(list(tree))
    return trees if iterations else tree


def kruskals(G, iterations=False):
    """Run Kruskal's algorithm on graph G.

    Args:
        G (nx.Graph): Networkx graph.
        iterations (bool): True iff the tree at every iteration should be returned.
    """
    edges = nx.get_edge_attributes(G,'weight')
    edges = list(dict(sorted(edges.items(), key=lambda item: item[1])))
    tree = []
    trees = [[]]
    forest = {i:i for i in range(len(G))}
    i = 0
    while len(tree) < len(G) - 1:
        u,v = edges[i]
        x = forest[u]
        y = forest[v]
        if x != y:
            for k in [k for k,v in forest.items() if v == y]:
                forest[k] = x
            tree.append((u,v))
            trees.append(list(tree))
        i += 1
    return trees if iterations else tree


def reverse_kruskals(G, iterations=False):
    """Run reverse Kruskal's algorithm on graph G.

    Args:
        G (nx.Graph): Networkx graph.
        iterations (bool): True iff the tree at every iteration should be returned.
    """
    edges = nx.get_edge_attributes(G,'weight')
    edges = list(dict(sorted(edges.items(), key=lambda item: item[1], reverse=True)))
    G_prime = nx.Graph()
    for i in range(len(G)):
        G_prime.add_node(i)
    G_prime.add_edges_from(edges)
    trees = [list(G_prime.edges)]
    i = 0
    while len(G_prime.edges) > len(G) - 1:
        u,v = edges[i]
        G_prime.remove_edge(u,v)
        if not nx.is_connected(G_prime):
            G_prime.add_edge(u,v)
        else:
            trees.append(list(G_prime.edges))
        i += 1
    return trees if iterations else list(G_prime.edges)


def spanning_tree_cost(G, tree):
    """Return the cost of the given spanning tree.

    Args:
        G (nx.Graph): Networkx graph.
        tree (List): List of edges in the spanning tree.
    """
    return sum([G[u][v]['weight'] for u,v in tree])


# TRAVELLING SALESMAN PROBLEM (TSP)

def neighbor(G, initial=0, nearest=True, iterations=False):
    """Run a neighbor heuristic on G starting at the given initial node.

    Args:
        G (nx.Graph): Networkx graph.
        intial (int): index of the node to start from.
        nearest (bool): run nearest neighbor if true. Otherwise, run random.
        iterations (bool): True iff the tree at every iteration should be returned.
    """
    unvisited = list(range(len(G))) # list of nodes

    # start tour at initial and remove it from unvisited
    tour = [initial]
    unvisited.remove(initial)
    tours = [tour.copy()]

    # choose next node from unvisited
    while len(unvisited) > 0:
        if nearest:
            u = tour[-1]
            d = {v : G[u][v]['weight'] for v in range(len(G)) if v in unvisited}
            min_val = min(d.values())
            possible = [k for k, v in d.items() if v==min_val]
            next_node = possible[randrange(len(possible))]
        else:
            next_node = unvisited[randrange(len(unvisited))]
        tour.append(next_node)
        unvisited.remove(next_node)
        tours.append(tour.copy())

    # go back to start
    tour.append(initial)
    tours.append(tour.copy())

    return tours if iterations else tour


def insertion(G, initial=[0,1,0], nearest=True, iterations=False):
    """Run an insertion heuristic on G starting with the given initial 2-node tour.

    Args:
        G (nx.Graph): Networkx graph.
        intial (List[int]): Initial 2-node tour.
        nearest (bool): Run nearest insertion if true. Otherwise, run random.
        iterations (bool): True iff the tree at every iteration should be returned."""

    unvisited = list(range(len(G))) # list of nodes

    # start tour at initial and remove it from unvisited
    tour = list(initial)
    unvisited.remove(initial[0])
    unvisited.remove(initial[1])
    tours = [tour.copy()]

    # choose next node from unvisited
    while len(unvisited) > 0:
        d = {u : min([G[u][v]['weight'] for v in np.unique(tour)]) for u in unvisited}
        if nearest:
            min_val = min(d.values())
            possible = [k for k, v in d.items() if v==min_val]
        else:
            max_val = max(d.values())
            possible = [k for k, v in d.items() if v==max_val]
        next_node = possible[randrange(len(possible))]

        # insert node into tour at minimum cost
        increase = [G[tour[i]][next_node]['weight']
                    + G[next_node][tour[i+1]]['weight']
                    - G[tour[i]][tour[i+1]]['weight'] for i in range(len(tour)-1)]
        insert_index = increase.index(min(increase))+1
        tour.insert(insert_index, next_node)
        unvisited.remove(next_node)
        tours.append(tour.copy())

    return tours if iterations else tour


def two_opt(G, tour, iterations=False):
    """Run 2-OPT on the initial tour until no improvement can be made.

    Args:
        G (nx.Graph): Networkx graph.
        tour (List[int]): intial tour to be improved.
        iterations (bool): True iff the tree at every iteration should be returned.
    """
    def two_opt_iteration(tour,G):
        for i in range(len(tour)-1):
            for j in range(i,len(tour)-1):
                u_1, u_2 = tour[i], tour[i+1]
                v_1, v_2 = tour[j], tour[j+1]
                if len(np.unique([u_1, u_2, v_1, v_2])) == 4:
                    after_swap = G[u_1][v_1]['weight'] + G[u_2][v_2]['weight']
                    before_swap = G[u_1][u_2]['weight'] + G[v_1][v_2]['weight']
                    if after_swap < before_swap:
                        swap = tour[i+1:j+1]
                        swap.reverse()
                        tour[i+1:j+1] = swap
                        return True, [u_1, u_2, v_1, v_2]
        return False, None

    tours = [tour.copy()]
    swaps = []
    improved, swapped = two_opt_iteration(tour,G)
    while improved:
        tours.append(tour.copy())
        swaps.append(swapped.copy())
        improved, swapped = two_opt_iteration(tour,G)
    return (tours, swaps) if iterations else tour


def solve_tsp(G):
    """Use OR-Tools to get a tour of the graph G.

    Args:
        G (nx.Graph): Networkx graph.
    """
    # number of locations, number of vehicles, start location
    manager = pywrapcp.RoutingIndexManager(len(G), 1, 0)
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return G[from_node][to_node]['weight']*10000

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    def get_routes(solution, routing, manager):
        """Get vehicle routes from a solution and store them in an array."""
        routes = []
        for route_nbr in range(routing.vehicles()):
            index = routing.Start(route_nbr)
            route = [manager.IndexToNode(index)]
            while not routing.IsEnd(index):
                index = solution.Value(routing.NextVar(index))
                route.append(manager.IndexToNode(index))
            routes.append(route)
        return routes

    solution = routing.Solve()
    return get_routes(solution, routing, manager)[0]


def optimal_tour(name):
    """Return an optimal tour for some instance name."""
    with open('data/optimal_tours.pickle', 'rb') as f:
        optimal_tours = pickle.load(f)
    return optimal_tours[name]


def tour_cost(G, tour):
    """Return the cost of the tour on graph G.

    Args:
        G (nx.Graph): Networkx graph.
        tour (List[int]): ordered list of nodes visited on the tour.
    """
    return sum([G[tour[i]][tour[i+1]]['weight'] for i in range(len(tour)-1)])


# --------
# Plotting
# --------

# JAVASCRIPT

increment = """
if ((parseInt(n.text) + 1) < parseInt(k.text)) {
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

done_update = """
if (iteration == parseInt(k.text) - 1) {
    done.text = "done."
} else {
    done.text = ""
}
"""

edge_subset_update = """
edge_subset_src.data['xs'] = source.data['edge_xs'][iteration]
edge_subset_src.data['ys'] = source.data['edge_ys'][iteration]
edge_subset_src.change.emit()
"""

cost_update = """
cost.text = source.data['costs'][iteration].toFixed(1)
"""

table_update = """
table_src.data = source.data['tables'][iteration]
"""

nodes_update = """
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
"""

swaps_update = """
swaps_src.data['swaps_before_x'] = source.data['swaps_before_x'][iteration]
swaps_src.data['swaps_before_y'] = source.data['swaps_before_y'][iteration]
swaps_src.data['swaps_after_x'] = source.data['swaps_after_x'][iteration]
swaps_src.data['swaps_after_y'] = source.data['swaps_after_y'][iteration]
swaps_src.change.emit()
"""

on_hover = """
source.data['last_index'] = cb_data.index.indices[0]
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


def blank_plot(G, plot_width, plot_height, show_us=False):
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
    if show_us:
        us_outline(plot)
    return plot


def us_outline(plot):
    """Add an outline of the US to the plot."""
    plot.image_url(url=['images/us.png'],
                   x=plot.x_range.start-20,
                   y=plot.y_range.end+5,
                   w=plot.x_range.end - plot.x_range.start,
                   h=plot.y_range.end - plot.y_range.start,
                   level='image')


def set_edge_positions(G):
    """Add edge attribute with positional data."""
    nx.set_edge_attributes(G, {(u,v) : (G.nodes[u]['x'], G.nodes[v]['x']) for u,v in G.edges}, 'xs')
    nx.set_edge_attributes(G, {(u,v) : (G.nodes[u]['y'], G.nodes[v]['y']) for u,v in G.edges}, 'ys')


def set_graph_colors(G, edges=[], show_all_edges=True):
    """Add node/edge attribute with color data. Highlight edges."""
    for u in G.nodes:
        G.nodes[u]['line_color'] = '#EA8585'
        G.nodes[u]['fill_color'] = '#EA8585'
    for u,v in G.edges:
        G[u][v]['line_color'] = 'lightgray'
        if show_all_edges:
            G[u][v]['visible'] = True
        else:
            G[u][v]['visible'] = False
    for u,v in edges:
        G[u][v]['line_color'] = 'black'
        G[u][v]['visible'] = True


def graph_sources(G):
    """Return data sources for the graph G."""
    nodes_df = pd.DataFrame([G.nodes[u] for u in sorted(G.nodes())])
    nodes_src = ColumnDataSource(data=nodes_df.to_dict(orient='list'))

    edges_df = pd.DataFrame([G[u][v] for u,v in G.edges()])
    u,v = zip(*[(u,v) for u,v in G.edges])
    edges_df['u'] = u
    edges_df['v'] = v
    edges_src = ColumnDataSource(data=edges_df.to_dict(orient='list'))

    labels_src = ColumnDataSource(data={'x': [np.mean(i) for i in nx.get_edge_attributes(G, 'xs').values()],
                                        'y': [np.mean(i) for i in nx.get_edge_attributes(G, 'ys').values()],
                                        'text': list(nx.get_edge_attributes(G,'weight').values())})
    return nodes_src, edges_src, labels_src


def graph_glyphs(plot, nodes_src, edges_src, labels_src, show_edges=True, show_labels=True):
    """Add and return glyphs for nodes and edges"""
    edges_glyph = plot.multi_line(xs='xs', ys='ys',
                                  line_color='line_color', hover_line_color='black',
                                  line_width=6, nonselection_line_alpha=1,
                                  visible=show_edges,
                                  alpha='visible',
                                  level='image',
                                  source=edges_src)
    nodes_glyph = plot.circle(x='x', y='y', size=12, level='glyph',
                              line_color='line_color', fill_color='fill_color',
                              nonselection_fill_alpha=1, source=nodes_src)

    labels = LabelSet(x='x', y='y', text='text', render_mode='canvas', visible=show_labels, source=labels_src)
    plot.add_layout(labels)
    return edges_glyph, nodes_glyph


# MAIN FUNCTIONS


def plot_graph(G, show_all_edges=True, show_labels=True, edges=[], width=900, height=500, show_us=False):
    """Plot the graph G.

    Args:
        G (nx.Graph): Networkx graph.
        edges (List): Edges to highlight.
    """
    G = G.copy()
    plot = blank_plot(G, plot_width=width, plot_height=height, show_us=show_us)

    set_edge_positions(G)
    set_graph_colors(G, edges, show_all_edges=show_all_edges)

    nodes_src, edges_src, labels_src = graph_sources(G)
    edges_glyph, nodes_glyph = graph_glyphs(plot, nodes_src, edges_src, labels_src, show_labels=show_labels)
    plot.add_tools(HoverTool(tooltips=[("Node", "$index")], renderers=[nodes_glyph]))
    grid = gridplot([[plot]],
                    plot_width=width, plot_height=height,
                    toolbar_location = None,
                    toolbar_options={'logo': None})

    show(grid)


def plot_create(G, create, width=900, height=500, show_us=False):
    """Plot a graph in which you can either create a tour or spanning tree.

    Args:
        G (nx.Graph): Networkx graph.
        create (string): {'tour', 'tree'}
    """
    if create == 'tour':
        show_all_edges=False
        show_labels=False
    elif create == 'tree':
        show_all_edges=True
        show_labels=True

    G = G.copy()
    plot = blank_plot(G, plot_width=width, plot_height=height, show_us=show_us)

    set_edge_positions(G)
    set_graph_colors(G, show_all_edges=show_all_edges)

    nodes_src, edges_src, labels_src = graph_sources(G)

    source = ColumnDataSource(data={'tree_nodes': [],
                                    'tree_edges' : [],
                                    'clicked' : []})
    tour_src =  ColumnDataSource(data={'edges_x' : [],
                                       'edges_y' : []})
    cost_matrix = ColumnDataSource(data={'G' : nx.adjacency_matrix(G).todense().tolist()})
    cost = Div(text='0.0', width=int(width/3), align='center')
    error_msg = Div(text='', width=int(width/3), align='center')
    clicked = Div(text='[]', width=int(width/3), align='center')
    plot.line(x='edges_x', y='edges_y', line_color='black', line_width=6, level='image', source=tour_src)
    edges_glyph, nodes_glyph = graph_glyphs(plot, nodes_src, edges_src, labels_src, show_labels=show_labels)

    check_done = """
    if (error_msg.text == 'done.') {
        return;
    }
    """

    create_tree_on_click = """
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
        tree_edges.push([u,v])
        var prev_cost = parseFloat(cost.text)
        cost.text = (prev_cost + w).toFixed(1)
        error_msg.text = ''
    } else {
        error_msg.text = 'You have selected an invalid edge.'
    }

    if (tree_nodes.length == nodes_src.data['x'].length) {
        error_msg.text = 'done.'
    }

    clicked.text = '['
    for (let i = 0; i < tree_edges.length; i++) {
        clicked.text = clicked.text.concat('(').concat(tree_edges[i].join(',')).concat(')')
        if (!(i == tree_edges.length - 1)) {
            clicked.text = clicked.text.concat(',')
        }
    }
    clicked.text = clicked.text.concat(']')

    source.change.emit()
    nodes_src.change.emit()
    edges_src.change.emit()
    """

    create_tour_on_click = """
    var v = source.data['last_index']
    var n = nodes_src.data['line_color'].length
    var tour = source.data['clicked']

    if (tour.includes(v)) {
        error_msg.text = 'This node is already in the tour.'
        return;
    } else {
        error_msg.text = ''
    }

    function add_node(v) {
        // add to cost
        if (tour.length > 0) {
            var u = tour[tour.length - 1]
            var prev_cost = parseFloat(cost.text)
            cost.text = (prev_cost + cost_matrix.data['G'][u][v]).toFixed(1)
        }

        // add to tour
        tour.push(v)
        clicked.text = '['.concat(tour.join(',')).concat(']')

        // highlight new node
        nodes_src.data['line_color'][v] = 'steelblue'
        nodes_src.data['fill_color'][v] = 'steelblue'

        // highlight new edge
        tour_src.data['edges_x'].push(nodes_src.data['x'][v])
        tour_src.data['edges_y'].push(nodes_src.data['y'][v])
    }

    add_node(v)
    if (tour.length == n) {
        add_node(tour[0])
        error_msg.text = 'done.'
    }

    source.change.emit()
    tour_src.change.emit()
    nodes_src.change.emit()
    """

    plot.add_tools(HoverTool(tooltips=[("Node", "$index")], renderers=[nodes_glyph]),
                   HoverTool(tooltips=None,
                             callback=CustomJS(args=dict(source=source), code=on_hover),
                             renderers=[edges_glyph if create=='tree' else nodes_glyph]),
                   TapTool(callback=CustomJS(args=dict(source=source, edges_src=edges_src, nodes_src=nodes_src, tour_src=tour_src,
                                                       cost_matrix=cost_matrix, cost=cost, error_msg=error_msg, clicked=clicked),
                                             code=check_done + create_tree_on_click if create=='tree' else create_tour_on_click),
                           renderers=[edges_glyph if create=='tree' else nodes_glyph]))

    # create layout
    grid = gridplot([[plot],
                     [row(cost,error_msg,clicked)]],
                    plot_width=width, plot_height=height,
                    toolbar_location = None,
                    toolbar_options={'logo': None})

    show(grid)


def plot_graph_iterations(G, nodes=None, edges=None, costs= None, tables=None, swaps=None, show_edges=True,
                          show_labels=True, width=900, height=500, show_us=False):
    """Plot the graph G with iterations of edges, nodes, and tables.

    Args:
        G (nx.Graph): Networkx graph.
        nodes (List): Nodes to highlight at each iteration.
        edges (List): Edges to highlight at each iteration.
        tables (List): Tables at each iteration.
    """
    G = G.copy()
    plot = blank_plot(G, plot_width=width, plot_height=height, show_us=show_us)

    set_edge_positions(G)
    set_graph_colors(G)
    for u in G.nodes:
        G.nodes[u]['line_color'] = '#EA8585'
        G.nodes[u]['fill_color'] = '#EA8585'

    # build source data dictionary
    k = 0  # number of iterations
    source_data = {}
    if edges is not None:
        k = len(edges)
        edge_xs = []
        edge_ys = []
        for i in range(len(edges)):
            xs = [G[u][v]['xs'] for u,v in edges[i]]
            ys = [G[u][v]['ys'] for u,v in edges[i]]
            edge_xs.append(xs)
            edge_ys.append(ys)
        source_data['edge_xs'] = edge_xs
        source_data['edge_ys'] = edge_ys
    if nodes is not None:
        k = len(nodes)
        source_data['nodes'] = nodes
    if costs is not None:
        k = len(costs)
        source_data['costs'] = costs
    if tables is not None:
        k = len(tables)
        tables = [table.to_dict(orient='list') for table in tables]
        source_data['tables'] = tables
    if swaps is not None:
        k = len(swaps) + 1
        swaps_before_x = []
        swaps_before_y = []
        swaps_after_x = []
        swaps_after_y = []
        for swap in swaps:
            get_coord = lambda i: (G.nodes()[swap[i]]['x'], G.nodes()[swap[i]]['y'])
            (u1x, u1y) = get_coord(0)
            (u2x, u2y) = get_coord(1)
            (v1x, v1y) = get_coord(2)
            (v2x, v2y) = get_coord(3)
            swaps_before_x.append([[u1x, u2x],[v1x, v2x]])
            swaps_before_y.append([[u1y, u2y],[v1y, v2y]])
            swaps_after_x.append([[u1x, v1x],[u2x, v2x]])
            swaps_after_y.append([[u1y, v1y],[u2y, v2y]])
        swaps_before_x.append([[],[]])
        swaps_before_y.append([[],[]])
        swaps_after_x.append([[],[]])
        swaps_after_y.append([[],[]])
        source_data['swaps_before_x'] = swaps_before_x
        source_data['swaps_before_y'] = swaps_before_y
        source_data['swaps_after_x'] = swaps_after_x
        source_data['swaps_after_y'] = swaps_after_y

    # data sources and glyphs
    args_dict = {}
    nodes_src, edges_src, labels_src = graph_sources(G)
    args_dict['nodes_src'] = nodes_src
    source = ColumnDataSource(data=source_data)
    args_dict['source'] = source

    n = Div(text='0', width=width, align='center')
    k = Div(text=str(k), width=width, align='center')
    done = Div(text='', width=int(width/2), align='center')
    args_dict['n'] = n
    args_dict['k'] = k
    args_dict['done'] = done
    edges_glyph, nodes_glyph = graph_glyphs(plot, nodes_src, edges_src, labels_src,
                                            show_edges=show_edges, show_labels=show_labels)

    if edges is not None:
        edge_subset_src = ColumnDataSource(data={'xs': edge_xs[0],
                                                 'ys': edge_ys[0]})
        plot.multi_line('xs', 'ys', line_color='black', line_width=6, level='underlay', source=edge_subset_src)
        args_dict['edge_subset_src'] = edge_subset_src

    if costs is not None:
        cost = Div(text=str(costs[0]), width=int(width/2), align='center')
        args_dict['cost'] = cost

    if tables is not None:
        table_src = ColumnDataSource(data=tables[0])
        columns = ([TableColumn(field='index', title='')] +
               [TableColumn(field=str(i), title=str(i)) for i in range(len(tables[0])-1)])
        table = DataTable(source=table_src, columns=columns, height=80, width=width, background='white', index_position=None,
                          editable=False, reorderable=False, sortable=False, selectable=False)
        args_dict['table_src'] = table_src

    if swaps is not None:
        swaps_src = ColumnDataSource(data={'swaps_before_x': swaps_before_x[0],
                                           'swaps_before_y': swaps_before_y[0],
                                           'swaps_after_x': swaps_after_x[0],
                                           'swaps_after_y': swaps_after_y[0]})
        plot.multi_line(xs='swaps_before_x', ys='swaps_before_y', line_color='red', line_width=6, level='overlay', source=swaps_src)
        plot.multi_line(xs='swaps_after_x', ys='swaps_after_y', line_color='#90D7F6', line_width=6, level='overlay', source=swaps_src)
        args_dict['swaps_src'] = swaps_src

    # Javascript
    next_btn_code = increment + done_update
    prev_btn_code = decrement + done_update
    if costs is not None:
        next_btn_code += cost_update
        prev_btn_code += cost_update
    if edges is not None:
        next_btn_code += edge_subset_update
        prev_btn_code += edge_subset_update
    if tables is not None:
        next_btn_code += table_update
        prev_btn_code += table_update
    if nodes is not None:
        next_btn_code += nodes_update
        prev_btn_code += nodes_update
    if swaps is not None:
        next_btn_code += swaps_update
        prev_btn_code += swaps_update


    # buttons
    next_button = Button(label="Next", button_type="success", width_policy='fit', sizing_mode='scale_width')
    next_button.js_on_click(CustomJS(args=args_dict, code=next_btn_code))
    prev_button = Button(label="Previous", button_type="success", width_policy='fit', sizing_mode='scale_width')
    prev_button.js_on_click(CustomJS(args=args_dict, code=prev_btn_code))

    plot.add_tools(HoverTool(tooltips=[("Node", "$index")], renderers=[nodes_glyph]))

    # create layout
    layout = [[plot],
              [row(prev_button, next_button, max_width=width, sizing_mode='stretch_both')],
              [row(cost, done) if costs else row(done)]]
    if tables is not None:
        layout.insert(1, [table])

    grid = gridplot(layout,
                    plot_width=width, plot_height=height,
                    toolbar_location = None,
                    toolbar_options={'logo': None})

    show(grid)


def plot_dijkstras(G, source=0, width=900, height=500):
    """Plot Dijkstra's algorithm running on G.

    Args:
        G (nx.Graph): Networkx graph.
        s (int): Source vertex to run the algorithm from.
    """
    nodes, edges, tables = dijkstras(G, s=source, iterations=True)
    plot_graph_iterations(G, nodes=nodes, edges=edges, tables=tables, width=width, height=height)


def plot_mst_algorithm(G, alg, i=0, width=900, height=500):
    """Plot the MST algorithm running on G.

    Args:
        G (nx.Graph): Networkx graph.
        alg (str): {'prims', 'kruskals', 'reverse_kruskals'}
        source (int): Source vertex to run the algorithm from.
    """
    if alg == 'prims':
        edges = prims(G, i=i, iterations=True)
    elif alg == 'kruskals':
        edges = kruskals(G, iterations=True)
    elif alg == 'reverse_kruskals':
        edges = reverse_kruskals(G, iterations=True)
    nodes = [list(set([item for sublist in edge for item in sublist])) for edge in edges]
    costs = [spanning_tree_cost(G, tree) for tree in edges]
    plot_graph_iterations(G, nodes=nodes, edges=edges, costs=costs, width=width, height=height)


def plot_tsp_heuristic(G, alg, initial, width=900, height=500, show_us=False):
    """Plot the TSP heuristic running on G.

    Args:
        G (nx.Graph): Networkx graph.
        alg (str): {'random_neighbor', 'nearest_neighbor', 'nearest_insertion', 'furthest_insertion', '2-OPT'}
        initial (int): Starting index or tour (depending on alg)
    """
    swaps = None
    if alg == 'random_neighbor':
        tours = neighbor(G, initial=initial, nearest=False, iterations=True)
    elif alg == 'nearest_neighbor':
        tours = neighbor(G, initial=initial, nearest=True, iterations=True)
    elif alg == 'nearest_insertion':
        tours = insertion(G, initial=initial, nearest=True, iterations=True)
    elif alg == 'furthest_insertion':
        tours = insertion(G, initial=initial, nearest=False, iterations=True)
    elif alg == '2-OPT':
        tours, swaps = two_opt(G, tour=initial, iterations=True)
    nodes = tours
    edges = [[(tour[i], tour[i+1]) for i in range(len(tour)-1)] for tour in tours]
    costs = [tour_cost(G, tour) for tour in tours]
    plot_graph_iterations(G, nodes=nodes, edges=edges, costs=costs, swaps=swaps, show_edges=False,
                          show_labels=False, width=width, height=height, show_us=show_us)
