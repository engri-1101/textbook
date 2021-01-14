import numpy as np
import math
import pandas as pd
from ortools.constraint_solver import pywrapcp
from random import randrange
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

def tsp_grid_instance(n, m, manhattan=True):
    """Return a distance matrix (manhattan or euclidian) on an n*m grid.
    
    Args:
        n (int): width of the grid.
        m (int): height of the grid.
        manhattan (bool): return manhattan distance matrix if true. Otherwise, return euclidian.
    """
    # create nodes of grid
    nodes = []
    nodes_df = pd.DataFrame()
    for i in range(n):
        for j in range(m):
            nodes.append((i,j))
            nodes_df = nodes_df.append({'name' : str((i,j)), 'x' : i, 'y' : j}, ignore_index=True)

    d = distance_matrix(nodes_df, manhattan=manhattan)
      
    return nodes_df, d


def distance_matrix(nodes, manhattan=True, vlsi=False):
    """Compute the distance matrix between the nodes.
    
    Args:
        nodes (pd.DataFrame): node start and end locations of the graph G.
        manhattan (bool): return manhattan distance matrix if true. Otherwise, return euclidian.
        vlsi (bool): true if and only if this is a vlsi etching instance.
    """
    if not vlsi:
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

    
def tour_cost(G, tour):
    """Return the cost of the tour on graph G.
    
    Args:
        G (np.ndarray): adjacency matrix representing a graph.
        tour (List[int]): ordered list of nodes visited on the tour.
    """
    return sum([G[tour[i],tour[i+1]] for i in range(len(tour)-1)])


# --------------
# TSP Heuristics
# --------------

def neighbor(G, initial, nearest):
    """Run a neighbor heuristic on G starting at the given initial node.
    
    Args:
        G (np.ndarray): adjacency matrix representing a graph.
        intial (int): index of the node to start from.    
        nearest (bool): run nearest neighbor if true. Otherwise, run random.
    """
    unvisited = list(range(len(G))) # list of nodes
    
    # start tour at initial and remove it from unvisited
    tour = [initial]
    unvisited.remove(initial) 
    
    # choose next node from unvisited
    while len(unvisited) > 0:
        neighbor_iteration(G, tour, unvisited, nearest)
        
    # go back to start
    tour.append(initial)
    
    return tour


def neighbor_iteration(G, tour, unvisited, nearest):
    """Do an iteration of a neighbor heuristic on G.
    
    Args:
        G (np.ndarray): adjacency matrix representing a graph.
        tour (List[int]): current tour on G
        unvisited (List[int]): node not currently visited by the tour
        nearest (bool): run nearest neighbor if true. Otherwise, run random.
    """
    if nearest:
        # dictionary from univisited nodes to their distance from current node
        d = {i : G[tour[-1]][i] for i in range(len(G[tour[-1]])) if i in unvisited}
        # randomly select next node among the nearest
        min_val = min(d.values())
        possible = [k for k, v in d.items() if v==min_val]
        next_node = possible[randrange(len(possible))]
    else:
        next_node = unvisited[randrange(len(unvisited))]
    tour.append(next_node)
    unvisited.remove(next_node)


def random_neighbor(G, initial=0):
    """Run the nearest neighbor heuristic on G starting at the given initial node.
    
    Args:
        G (np.ndarray): adjacency matrix representing a graph.
        intial (int): index of the node to start from.    
    """
    return neighbor(G, initial, False)

def nearest_neighbor(G, initial=0):
    """Run the nearest neighbor heuristic on G starting at the given initial node.
    
    Args:
        G (np.ndarray): adjacency matrix representing a graph.
        intial (int): index of the node to start from.    
    """
    return neighbor(G, initial, True)


def insertion(G, initial, nearest):
    """Run an insertion heuristic on G starting with the given initial 2-node tour."""
    
    unvisited = list(range(len(G))) # list of nodes
    
    # start tour at initial and remove it from unvisited
    tour = list(initial)
    unvisited.remove(initial[0]) 
    unvisited.remove(initial[1]) 
    
    # choose next node from unvisited
    while len(unvisited) > 0:
        insertion_iteration(G, tour, unvisited, nearest)
    
    return tour


def insertion_iteration(G, tour, unvisited, nearest):
    """Do an iteration of an insertion heuristic on G.
    
    Args:
        G (np.ndarray): adjacency matrix representing a graph.
        tour (List[int]): current tour on G
        unvisited (List[int]): node not currently visited by the tour
        nearest (bool): run nearest neighbor if true. Otherwise, run random.
    """
    # dictionary from univisited nodes to their shortest distance from tour
    d = G[:,np.unique(tour)].min(axis=1)
    d = {i : d[i] for i in range(len(d)) if i in unvisited}
    if nearest:
        min_val = min(d.values())
        possible = [k for k, v in d.items() if v==min_val]    
    else:
        max_val = max(d.values())
        possible = [k for k, v in d.items() if v==max_val] 
    next_node = possible[randrange(len(possible))]

    # insert node into tour at minimum cost
    increase = [G[tour[i], next_node]
                + G[next_node, tour[i+1]] 
                - G[tour[i], tour[i+1]] for i in range(len(tour)-1)]
    insert_index = increase.index(min(increase))+1
    tour.insert(insert_index, next_node)
    unvisited.remove(next_node) 


def nearest_insertion(G, initial=[0,1,0]):
    """Run the nearest insertion heuristic on G starting with the given initial 2-node tour.
    
    Args:
        G (np.ndarray): adjacency matrix representing a graph.
        intial (List[int]): initial 2-node tour. 
    """
    return insertion(G, initial, True)


def furthest_insertion(G, initial=None):
    """Run the furthest insertion heuristic on G starting with the given initial 2-node tour.
    
    Args:
        G (np.ndarray): adjacency matrix representing a graph.
        intial (int): initial 2-node tour.  
    """
    if initial is None:
        initial = [0,len(G)-1,0]
    return insertion(G, initial, False)


# -----
# 2-OPT
# -----

def two_opt(G, tour):
    """Run 2-OPT on the initial tour until no improvement can be made.
    
    Args:
        G (np.ndarray): adjacency matrix representing a graph.
        tour (List[int]): intial tour to be improved.
    """ 
    improved, swapped = two_opt_iteration(tour,G)
    while improved:
        improved, swapped = two_opt_iteration(tour,G)
    return tour


def two_opt_iteration(tour,G):
    """Do an interation of 2-OPT. Return true if improved.
    
    Args:
        edges (List[List[int]]): List of edges in the current tour.
        tour_matrix (np.ndarray): Adjacency matrix representing the tour.
        G (np.ndarray): adjacency matrix representing a graph. 
    """
    for i in range(len(tour)-1):
        for j in range(i,len(tour)-1):
            u_1, u_2 = tour[i], tour[i+1]
            v_1, v_2 = tour[j], tour[j+1]
            if len(np.unique([u_1, u_2, v_1, v_2])) == 4:
                if G[u_1,v_1] + G[u_2,v_2] < G[u_1,u_2] + G[v_1,v_2]:
                    swap = tour[i+1:j+1]
                    swap.reverse()
                    tour[i+1:j+1] = swap
                    return True, [u_1, u_2, v_1, v_2]
    return False, None


# ----------
# TSP Solver
# ----------

def solve_tsp(G):
    """Use OR-Tools to get an optimal tour of the graph G.
    
    Args:
        G (np.ndarray): adjacency matrix representing a graph.
    """
    # number of locations, number of vehicles, start location
    manager = pywrapcp.RoutingIndexManager(len(G), 1, 0)
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return G[from_node, to_node]*10000

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


# --------
# Plotting
# --------

def blank_plot(x, y, plot_width, plot_height, show_us=False):
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
    if show_us:
        us_outline(plot)
    return plot


def graph_range(x, y):
    """Return graph range for given points."""
    min_x, max_x = min(x), max(x)
    x_margin = 0.085*(max_x - min_x)
    min_x, max_x = min_x - x_margin, max_x + x_margin
    min_y, max_y = min(y), max(y)
    y_margin = 0.085*(max_y - min_y)
    min_y, max_y = min_y - y_margin, max_y + y_margin
    return min_x, max_x, min_y, max_y


def us_outline(plot):
    """Add an outline of the US to the plot."""
    plot.image_url(url=['images/us.png'],x=plot.x_range.start-20,
                                         y=plot.y_range.end+5,
                                         w=plot.x_range.end - plot.x_range.start,
                                         h=plot.y_range.end - plot.y_range.start)


# --------------
# CUSTOM JS CODE
# --------------

increment = """
if ((parseInt(n.text) + 1) < source.data['edges_y'].length) {
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

auto_complete_tour = """
if (iteration == source.data['edges_y'].length - 2) {
    iteration = iteration + 1
}
"""

auto_incomplete_tour = """
if (iteration == source.data['edges_y'].length - 2) {
    iteration = iteration - 1
}
"""


def plot_tour(nodes, G, tour, width=400, height=400, show_us=False):
    """Plot the tour on the nodes."""
    edges_x = []
    edges_y = []
    for i in tour:
        edges_x.append(nodes.loc[i]['x'])
        edges_y.append(nodes.loc[i]['y'])
    x = nodes.x.values.tolist()
    y = nodes.y.values.tolist()

    plot = blank_plot(x, y, width, height, show_us=show_us)
    
    # label
    cost = Div(text=str(round(tour_cost(G, tour),1)), width=width, align='center')
    plot.line(x=edges_x, y=edges_y, line_color='black', line_width=4)
    plot.circle(x, y, size=8, line_color='steelblue', fill_color='steelblue')

    # create layout
    grid = gridplot([[plot],[cost]], 
                    plot_width=width, plot_height=height,
                    toolbar_location = None,
                    toolbar_options={'logo': None})
    
    show(grid)
    
    
def plot_vlsi_tour(nodes, G, tour, width=800, height=400, show_us=False):
    """Plot the vlsi tour on the nodes."""
    edges_x = []
    edges_y = []
    for i in tour:
        edges_x.append(nodes.loc[i]['x_start'])
        edges_y.append(nodes.loc[i]['y_start'])
        edges_x.append(nodes.loc[i]['x_end'])
        edges_y.append(nodes.loc[i]['y_end'])

    lines_x = []
    lines_y = []
    for index, row in nodes.iterrows():
        lines_x.append([row['x_start'],row['x_end']])
        lines_y.append([row['y_start'],row['y_end']])
        
    x_start = nodes.x_start.values.tolist()
    y_start = nodes.y_start.values.tolist()
    x_end = nodes.x_end.values.tolist()
    y_end = nodes.y_end.values.tolist()
        
    plot = blank_plot(x_start + x_end, y_start + y_end, width, height, show_us=show_us)
    
    # label
    cost = Div(text=str(round(tour_cost(G, tour),1)), width=width, align='center')
    plot.multi_line(xs=lines_x, ys=lines_y, line_color='black', line_width=2)
    plot.line(x=edges_x, y=edges_y, line_color='black', line_width=2, line_dash='dashed')
    plot.circle(x_start, y_start, size=5, line_color='steelblue', fill_color='steelblue')
    plot.circle(x_end, y_end, size=5, line_color='#DC0000', fill_color='#DC0000')
    
    # create layout
    grid = gridplot([[plot],[cost]], 
                    plot_width=width, plot_height=height,
                    toolbar_location = None,
                    toolbar_options={'logo': None})
    
    show(grid)
    

def plot_create_tour(nodes, G, width=400, height=400, show_us=False):
    """Allow the user to construct a tour.
    
    Args:
        nodes (pd.DataFrame): node locations of the graph G.
        G (np.ndarray): adjacency matrix of the graph G.
    """  
    # node data
    x = nodes.x.values.tolist()
    y = nodes.y.values.tolist()

    plot = blank_plot(x, y, width, height, show_us=show_us)
    
    # label
    cost = Div(text=str(0.0), width=int(width/2), align='center') 
    done = Div(text='', width=int(width/2), align='center')  
        
    # tour and edges
    source = ColumnDataSource(data={'G': G.tolist()})
    tour = ColumnDataSource(data={'edges_x': [],
                                  'edges_y' : [],
                                  'indices' : []})
    plot.line(x='edges_x', y='edges_y', line_color='black', line_width=4, source=tour)
    pts = plot.circle(x, y, size=10, line_color='steelblue', fill_color='steelblue', nonselection_fill_alpha=1)
    
    # --------------
    # CUSTOM JS CODE
    # --------------
    
    on_hover = """
    source.data['last_index'] = cb_data.index.indices[0]   
    """
     
    on_click = """
    var node = source.data['last_index']
    
    if (node.toString() != -1) {
        if (!(tour.data['indices'].includes(node))) {
            if (tour.data['indices'].length > 0) { 
                var prev = tour.data['indices'][tour.data['indices'].length - 1]
            } else {
                var prev = -1
            }

            var tmp_edges_x = tour.data['edges_x']
            var tmp_edges_y = tour.data['edges_y']
            var tmp_indices = tour.data['indices']

            tmp_edges_x.push(pts.data['x'][node])
            tmp_edges_y.push(pts.data['y'][node])
            tmp_indices.push(node)

            tour.data['edges_x'] = tmp_edges_x
            tour.data['edges_y'] = tmp_edges_y
            tour.data['indices'] = tmp_indices

            if (prev == -1) {
                cost.text = '0.0'
            } else {
                var before = parseFloat(cost.text)
                var increase = source.data['G'][prev][node]
                cost.text = (before + increase).toFixed(1)   
            }
            
            if (tour.data['indices'].length == source.data['G'].length) {
                var tmp_edges_x = tour.data['edges_x']
                var tmp_edges_y = tour.data['edges_y']
                var tmp_indices = tour.data['indices']

                tmp_edges_x.push(tmp_edges_x[0])
                tmp_edges_y.push(tmp_edges_y[0])
                tmp_indices.push(tmp_indices[0])

                tour.data['edges_x'] = tmp_edges_x
                tour.data['edges_y'] = tmp_edges_y
                tour.data['indices'] = tmp_indices

                var before = parseFloat(cost.text)
                var increase = source.data['G'][node][tmp_indices[0]]
                cost.text = (before + increase).toFixed(1) 
            }    
        }
    }
    done.text = '['.concat(tour.data['indices'].join(',')).concat(']')
    tour.change.emit()
    """
    
    plot.add_tools(HoverTool(tooltips=None,
                             callback=CustomJS(args=dict(source=source), code=on_hover),
                             renderers=[pts]),
                   TapTool(callback=CustomJS(args=dict(source=source, tour=tour, pts=pts.data_source,
                                                       cost=cost, done=done), code=on_click),
                           renderers=[pts]))
    
    # create layout
    grid = gridplot([[plot],
                     [row(cost,done)]], 
                    plot_width=width, plot_height=height,
                    toolbar_location = None,
                    toolbar_options={'logo': None})
    
    show(grid)
    

def plot_tsp_heuristic(nodes, G, heuristic, initial, width=400, height=400, show_us=False):
    """Plot the heuristic executed on graph G.
    
    Args:
        nodes (pd.DataFrame): node locations of the graph G.
        G (np.ndarray): adjacency matrix of the graph G.
        heuristic (str): the heuristic to be run on the graph G.
        initial (List[int]): the initial tour / node for heuristic.
    """
    assert heuristic in ['random_neighbor', 'nearest_neighbor', 'nearest_insertion', 'furthest_insertion']
    
    # maintain tour and cost at every iteration
    tours = []
    costs = []
    
    unvisited = list(range(len(G))) # list of nodes
    
    # set initial tour
    if heuristic in ['random_neighbor', 'nearest_neighbor']:
        tour = [initial]
        unvisited.remove(initial) 
    else:
        tour = list(initial)
        unvisited.remove(initial[0]) 
        unvisited.remove(initial[1]) 
        
    tours.append(list(tour))
    costs.append(tour_cost(G, tour))
    
    # choose next node from unvisited
    while len(unvisited) > 0:
        if heuristic == 'random_neighbor':
            neighbor_iteration(G, tour, unvisited, nearest=False)
        if heuristic == 'nearest_neighbor':
            neighbor_iteration(G, tour, unvisited, nearest=True)
        if heuristic == 'nearest_insertion':
            insertion_iteration(G, tour, unvisited, nearest=True)
        if heuristic == 'furthest_insertion':
            insertion_iteration(G, tour, unvisited, nearest=False)
        tours.append(list(tour))
        costs.append(tour_cost(G, tour))
    
    # back to start
    if heuristic in ['random_neighbor', 'nearest_neighbor']:
        tour.append(initial) 
    
    tours.append(list(tour))
    costs.append(tour_cost(G, tour))
    
    tour_list = list(tour)
    
    # data for every tour and nodes
    edges_x = []
    edges_y = []
    for tour in tours:      
        edges_x.append([nodes.loc[i]['x'] for i in tour])
        edges_y.append([nodes.loc[i]['y'] for i in tour])
    x = nodes.x.values.tolist()
    y = nodes.y.values.tolist()

    plot = blank_plot(x, y, width, height, show_us=show_us)
    
    # label
    cost = Div(text=str(round(costs[0],1)), width=int(width/2), align='center')
    done = Div(text='', width=int(width/2), align='center')  
    n = Div(text='0', width=width, align='center')
        
    # tour and edges
    source = ColumnDataSource(data={'edges_x': edges_x,
                                    'edges_y': edges_y,
                                    'costs': costs})
    tour = ColumnDataSource(data={'edges_x': edges_x[0],
                                  'edges_y' : edges_y[0]})
    plot.line(x='edges_x', y='edges_y', line_color='black', line_width=4, source=tour)
    plot.circle(x, y, size=8, line_color='steelblue', fill_color='steelblue')
    
    # --------------
    # CUSTOM JS CODE
    # --------------
      
    update = """
    cost.text = source.data['costs'][iteration].toFixed(1)
    
    if (iteration == source.data['edges_y'].length - 1) {
        done.text = "done."
    } else {
        done.text = ""
    }

    tour.data['edges_x'] = source.data['edges_x'][iteration]
    tour.data['edges_y'] = source.data['edges_y'][iteration]
    tour.change.emit()
    """
       
    next_btn_code = increment + auto_complete_tour + update
    prev_btn_code = decrement + auto_incomplete_tour + update
    
    # add buttons
    next_button = Button(label="Next", button_type="success", width_policy='fit', sizing_mode='scale_width')
    next_button.js_on_click(CustomJS(args=dict(tour=tour, source=source, cost=cost, 
                                               done=done, n=n), code=next_btn_code))
    prev_button = Button(label="Previous", button_type="success", width_policy='fit', sizing_mode='scale_width')
    prev_button.js_on_click(CustomJS(args=dict(tour=tour, source=source, cost=cost, 
                                               done=done, n=n), code=prev_btn_code))
    
    # create layout
    grid = gridplot([[plot],
                     [row(prev_button, next_button, max_width=width, sizing_mode='stretch_both')],
                     [row(cost,done)]], 
                    plot_width=width, plot_height=height,
                    toolbar_location = None,
                    toolbar_options={'logo': None})
    
    show(grid)
    
    return tour_list
    
    
def plot_two_opt(nodes, G, tour, width=400, height=400, show_us=False):
    """Plot the execution of two-opt on the given tour.
    
    Args:
        nodes (pd.DataFrame): node locations of the graph G.
        G (np.ndarray): adjacency matrix of the graph G.
        tour (List[int]): inital feasible tour.
    """    
    # maintain at every iteration
    tours = []
    swaps = []
    costs = []
    
    # run 2-OPT
    tours.append(list(tour))
    costs.append(tour_cost(G, tour))
    improved, swapped = two_opt_iteration(tour,G)
    if improved:
        swaps.append([] if swapped is None else list(swapped))
    while improved:
        tours.append(list(tour))
        costs.append(tour_cost(G, tour))
        improved, swapped = two_opt_iteration(tour,G)
        if improved:
            swaps.append([] if swapped is None else list(swapped))
     
    tour_list = list(tour)
    
    # data for every tour and nodes
    edges_x = []
    edges_y = []
    swaps_before_x = []
    swaps_before_y = []
    swaps_after_x = []
    swaps_after_y = []
    for tour in tours:      
        edges_x.append([nodes.loc[i]['x'] for i in tour])
        edges_y.append([nodes.loc[i]['y'] for i in tour])
    for swap in swaps:
        (u1x, u1y) = nodes.loc[swap[0]][['x','y']]
        (u2x, u2y) = nodes.loc[swap[1]][['x','y']]
        (v1x, v1y) = nodes.loc[swap[2]][['x','y']]
        (v2x, v2y) = nodes.loc[swap[3]][['x','y']]
        swaps_before_x.append([[u1x, u2x],[v1x, v2x]])
        swaps_before_y.append([[u1y, u2y],[v1y, v2y]])   
        swaps_after_x.append([[u1x, v1x],[u2x, v2x]])
        swaps_after_y.append([[u1y, v1y],[u2y, v2y]])  
    x = nodes.x.values.tolist()
    y = nodes.y.values.tolist()
    

    plot = blank_plot(x, y, width, height, show_us=show_us)
    
    # label
    cost = Div(text=str(round(costs[0],1)), width=int(width/2), align='center')
    done = Div(text='', width=int(width/2), align='center')  
    n = Div(text='0', width=width, align='center')
        
    # tour and edges
    source = ColumnDataSource(data={'edges_x': edges_x,
                                    'edges_y': edges_y,
                                    'costs': costs})
    tour = ColumnDataSource(data={'edges_x': edges_x[0],
                                  'edges_y' : edges_y[0]})
    swaps_source = ColumnDataSource(data={'swaps_before_x' : swaps_before_x,
                                          'swaps_before_y' : swaps_before_y,
                                          'swaps_after_x' : swaps_after_x,
                                          'swaps_after_y' : swaps_after_y})
    if len(swaps_before_x) > 0:
        swaps = ColumnDataSource(data={'swaps_before_x' : swaps_before_x[0],
                                       'swaps_before_y' : swaps_before_y[0],
                                       'swaps_after_x' : swaps_after_x[0],
                                       'swaps_after_y' : swaps_after_y[0]})
    
    plot.line(x='edges_x', y='edges_y', line_color='black', line_width=4, source=tour)
    if len(swaps_before_x) > 0:
        plot.multi_line(xs='swaps_before_x', ys='swaps_before_y', line_color='red', line_width=4, source=swaps)
        plot.multi_line(xs='swaps_after_x', ys='swaps_after_y', line_color='#90D7F6', line_width=4, source=swaps)
    plot.circle(x, y, size=8, line_color='steelblue', fill_color='steelblue')
    
    # --------------
    # CUSTOM JS CODE
    # --------------
      
    update = """
    cost.text = source.data['costs'][iteration].toFixed(1)
    
    if (iteration == source.data['edges_y'].length - 1) {
        done.text = "done."
        swaps.data['swaps_before_x'] = [[]]
        swaps.data['swaps_before_y'] = [[]]
        swaps.data['swaps_after_x'] = [[]]
        swaps.data['swaps_after_y'] = [[]]
    } else {
        done.text = ""
        swaps.data['swaps_before_x'] = swaps_source.data['swaps_before_x'][iteration]
        swaps.data['swaps_before_y'] = swaps_source.data['swaps_before_y'][iteration]
        swaps.data['swaps_after_x'] = swaps_source.data['swaps_after_x'][iteration]
        swaps.data['swaps_after_y'] = swaps_source.data['swaps_after_y'][iteration]
    }

    tour.data['edges_x'] = source.data['edges_x'][iteration]
    tour.data['edges_y'] = source.data['edges_y'][iteration]
    tour.change.emit()
    swaps.change.emit()
    """
       
    next_btn_code = increment + update
    prev_btn_code = decrement + update
    
    # add buttons
    next_button = Button(label="Next", button_type="success", width_policy='fit', sizing_mode='scale_width')
    next_button.js_on_click(CustomJS(args=dict(tour=tour, source=source, cost=cost, 
                                               swaps_source=swaps_source, swaps=swaps,
                                               done=done, n=n), code=next_btn_code))
    prev_button = Button(label="Previous", button_type="success", width_policy='fit', sizing_mode='scale_width')
    prev_button.js_on_click(CustomJS(args=dict(tour=tour, source=source, cost=cost, 
                                               swaps_source=swaps_source, swaps=swaps,
                                               done=done, n=n), code=prev_btn_code))
   
    # create layout
    grid = gridplot([[plot],
                     [row(prev_button, next_button, max_width=width, sizing_mode='stretch_both')],
                     [row(cost,done)]], 
                    plot_width=width, plot_height=height,
                    toolbar_location = None,
                    toolbar_options={'logo': None})
    
    show(grid)
    
    return tour_list
