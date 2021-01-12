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

    # create distance matrix
    d = np.zeros((len(nodes),len(nodes)))
    for i in range(len(nodes)):
        for j in range(len(nodes)):
            if manhattan:
                d[i][j] = abs(nodes[i][0] - nodes[j][0]) + abs(nodes[i][1] - nodes[j][1])
            else:
                d[i][j] = math.sqrt((nodes[i][0] - nodes[j][0])**2 + (nodes[i][1] - nodes[j][1])**2)
    
    return nodes_df, d


def create_G(nodes, manhattan=True):
    """Create the adjacency/distance matrix G for the given nodes dataframe.
    
    Args:
        nodes (pd.DataFrame): node locations of the graph G.
    """
    d = np.zeros((len(nodes),len(nodes)))
    for i, node_i in nodes.iterrows():
        for j, node_j in nodes.iterrows():
            if manhattan:
                d[i][j] = abs(node_i['x'] - node_j['x']) + abs(node_i['y'] - node_j['y'])
            else:
                d[i][j] = math.sqrt((node_i['x'] - node_j['x'])**2 + (node_i['y'] - node_j['y'])**2)
    return d


def create_vlsi_G(nodes, manhattan=True):
    """Create the adjacency/distance matrix G for the given VLSI nodes dataframe.
    
    Args:
        nodes (pd.DataFrame): node start and end locations of the graph G.
    """
    d = np.zeros((len(nodes),len(nodes)))
    for i, node_i in nodes.iterrows():
        for j, node_j in nodes.iterrows():
            if manhattan:
                d[i][j] = abs(node_i['x_end'] - node_j['x_start']) + abs(node_i['y_end'] - node_j['y_start'])
            else:
                d[i][j] = math.sqrt((node_i['x_end'] - node_j['x_start'])**2 
                                    + (node_i['y_end'] - node_j['y_start'])**2)
    return d


def tour_cost(G, tour):
    """Return the cost of the tour on graph G.
    
    Args:
        G (np.ndarray): adjacency matrix representing a graph.
        tour (List[int]): ordered list of nodes visited on the tour.
    """
    return sum([G[tour[i],tour[i+1]] for i in range(len(tour)-1)])


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


def two_opt(G, tour):
    """Run 2-OPT on the initial tour until no improvement can be made.
    
    Args:
        G (np.ndarray): adjacency matrix representing a graph.
        tour (List[int]): intial tour to be improved.
    """ 
    improved = two_opt_iteration(tour,G)
    while improved:
        improved = two_opt_iteration(tour,G)
    return tour

def two_opt_iteration(tour,G):
    """Do an interation of 2-OPT. Return true if improved.
    
    Args:
        edges (List[List[int]]): List of edges in the current tour.
        tour_matrix (np.ndarray): Adjacency matrix representing the tour.
        G (np.ndarray): adjacency matrix representing a graph. 
    """
    for i in range(len(tour)-1):
        for j in range(len(tour)-1):
            u_1, u_2 = tour[i], tour[i+1]
            v_1, v_2 = tour[j], tour[j+1]
            if len(np.unique([u_1, u_2, v_1, v_2])) == 4:
                if G[u_1,v_1] + G[u_2,v_2] < G[u_1,u_2] + G[v_1,v_2]:
                    if i < j:
                        swap = tour[i+1:j+1]
                        swap.reverse()
                        tour[i+1:j+1] = swap
                    else:
                        swap = tour[j+1:i+1]
                        swap.reverse()
                        tour[j+1:i+1] = swap
                    return True
    return False


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


def plot_tour(nodes, G, tour):
    """Plot the tour on the nodes."""
    edges_x = []
    edges_y = []
    for i in tour:
        edges_x.append(nodes.loc[i]['x'])
        edges_y.append(nodes.loc[i]['y'])
    x = nodes.x.values.tolist()
    y = nodes.y.values.tolist()

    # set graph range
    min_x, max_x = min(x), max(x)
    x_margin = 0.05*(max_x - min_x)
    min_x, max_x = min_x - x_margin, max_x + x_margin
    min_y, max_y = min(y), max(y)
    y_margin = 0.05*(max_y - min_y)
    min_y, max_y = min_y - y_margin, max_y + y_margin

    # make plot
    plot = figure(x_range=(min_x, max_x), 
                  y_range=(min_y, max_y), 
                  title="", 
                  plot_width=500,
                  plot_height=500)
    plot.toolbar.logo = None
    plot.toolbar_location = None
    plot.xgrid.grid_line_color = None
    plot.ygrid.grid_line_color = None
    plot.xaxis.visible = False
    plot.yaxis.visible = False 
    plot.background_fill_color = None
    plot.border_fill_color = None
    plot.outline_line_color = None
    
    # label
    cost = Div(text=str(round(tour_cost(G, tour),3)), width=400, align='center')
    plot.line(x=edges_x, y=edges_y, line_color='black', line_width=4)
    plot.circle(x, y, size=8, line_color='steelblue', fill_color='steelblue')

    
    # create layout
    grid = gridplot([[plot],[cost]], 
                    plot_width=400, plot_height=400,
                    toolbar_location = None,
                    toolbar_options={'logo': None})
    
    show(grid)
    
    
def plot_vlsi_tour(nodes, G, tour, labels=True):
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
        
    x = x_start + x_end
    y = y_start + y_end

    # set graph range
    min_x, max_x = min(x), max(x)
    x_margin = 0.05*(max_x - min_x)
    min_x, max_x = min_x - x_margin, max_x + x_margin
    min_y, max_y = min(y), max(y)
    y_margin = 0.05*(max_y - min_y)
    min_y, max_y = min_y - y_margin, max_y + y_margin

    # make plot
    plot = figure(x_range=(min_x, max_x), 
                  y_range=(min_y, max_y), 
                  title="", 
                  plot_width=1000,
                  plot_height=500)
    plot.toolbar.logo = None
    plot.toolbar_location = None
    plot.xgrid.grid_line_color = None
    plot.ygrid.grid_line_color = None
    plot.xaxis.visible = False
    plot.yaxis.visible = False 
    plot.background_fill_color = None
    plot.border_fill_color = None
    plot.outline_line_color = None
    
    # label
    cost = Div(text=str(round(tour_cost(G, tour),3)), width=800, align='center')
    plot.multi_line(xs=lines_x, ys=lines_y, line_color='black', line_width=2)
    plot.line(x=edges_x, y=edges_y, line_color='black', line_width=2, line_dash='dashed')
    plot.circle(x_start, y_start, size=5, line_color='steelblue', fill_color='steelblue')
    plot.circle(x_end, y_end, size=5, line_color='#DC0000', fill_color='#DC0000')
    
    source = ColumnDataSource(data=dict(x_end=x_end,
                                        y_end=y_end,
                                        name=list(range(len(y_start)))))
    
    if labels:
        labels = LabelSet(x='x_end', y='y_end', text='name', level='glyph',
                  x_offset=5, y_offset=0, render_mode='canvas', source=source)
        plot.add_layout(labels)

    
    # create layout
    grid = gridplot([[plot],[cost]], 
                    plot_width=800, plot_height=400,
                    toolbar_location = None,
                    toolbar_options={'logo': None})
    
    show(grid)


def plot_tsp_heuristic(nodes, G, heuristic, initial):
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
    
    # data for every tour and nodes
    edges_x = []
    edges_y = []
    for tour in tours:      
        edges_x.append([nodes.loc[i]['x'] for i in tour])
        edges_y.append([nodes.loc[i]['y'] for i in tour])
    x = nodes.x.values.tolist()
    y = nodes.y.values.tolist()
    
    # set graph range
    min_x, max_x = min(x), max(x)
    x_margin = 0.05*(max_x - min_x)
    min_x, max_x = min_x - x_margin, max_x + x_margin
    min_y, max_y = min(y), max(y)
    y_margin = 0.05*(max_y - min_y)
    min_y, max_y = min_y - y_margin, max_y + y_margin

    # make plot
    plot = figure(x_range=(min_x, max_x), 
                  y_range=(min_y, max_y), 
                  title="", 
                  plot_width=500,
                  plot_height=500)
    plot.toolbar.logo = None
    plot.toolbar_location = None
    plot.xgrid.grid_line_color = None
    plot.ygrid.grid_line_color = None
    plot.xaxis.visible = False
    plot.yaxis.visible = False 
    plot.background_fill_color = None
    plot.border_fill_color = None
    plot.outline_line_color = None
    
    # label
    cost = Div(text=str(costs[0]), width=350, align='center')
    done = Div(text='', width=300, align='center')  
    n = Div(text='0', width=400, align='center')
        
    # tour and edges
    source = ColumnDataSource(data={'edges_x': edges_x,
                                    'edges_y': edges_y,
                                    'costs': costs})
    tour = ColumnDataSource(data={'edges_x': edges_x[0],
                                  'edges_y' : edges_y[0]})
    plot.line(x='edges_x', y='edges_y', line_color='black', line_width=4, source=tour)
    
    # nodes
    plot.circle(x, y, size=8, line_color='steelblue', fill_color='steelblue')
    
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
      
    update = """
    cost.text = source.data['costs'][iteration].toFixed(3)
    
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
                     [row(prev_button, next_button, max_width=400, sizing_mode='stretch_both')],
                     [row(cost,done)]], 
                    plot_width=400, plot_height=400,
                    toolbar_location = None,
                    toolbar_options={'logo': None})
    
    show(grid)
