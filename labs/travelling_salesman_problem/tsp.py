import pickle
import networkx as nx
import vinal
from vinal.plot import _blank_plot
from vinal.algorithms import tour_cost
from ortools.constraint_solver import pywrapcp
from bokeh.plotting import figure, Figure
from bokeh.models.widgets.markups import Div
from bokeh.models.widgets.tables import TableColumn, DataTable
from bokeh.models.renderers import GlyphRenderer
from bokeh.layouts import row, gridplot, GridBox
from bokeh.models import (HoverTool, TapTool, ColumnDataSource, LabelSet,
                          Button, CustomJS)
from PIL import Image
import numpy as np

def new_add_image(plot:figure, image:str):
    im = Image.open(image).convert('RGBA')
    xdim, ydim = im.size

    img = np.empty((ydim, xdim), dtype=np.uint32)
    view = img.view(dtype=np.uint8).reshape((ydim, xdim, 4))

    view[:,:,:] = np.flipud(np.asarray(im))

    plot.image_rgba(image=[img],
                    x=plot.x_range.start,
                    y=plot.y_range.start,
                    dw=plot.x_range.end - plot.x_range.start,
                    dh=plot.y_range.end - plot.y_range.start,
                    level="image")

vinal.plot._add_image = new_add_image

def optimal_tour(name):
    """Return an optimal tour for some instance name."""
    with open('data/optimal_tours.pickle', 'rb') as f:
        optimal_tours = pickle.load(f)
    return optimal_tours[name]


def solve_tsp(G):
    """Use OR-Tools to get a tour of the graph G.

    Args:
        G (nx.Graph): Networkx graph.

    Returns:
        List[int]: Tour of the graph G
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


def etching_tour_plot(G, tour, **kw):
    """Return plot of the tour on the etching problem.

    Args:
        G (nx.Graph): Networkx graph.
        tour (List[int]): Tour of the graph
    """
    # nodes
    x_start = list(nx.get_node_attributes(G,'x_start').values())
    x_end = list(nx.get_node_attributes(G,'x_end').values())
    y_start = list(nx.get_node_attributes(G,'y_start').values())
    y_end = list(nx.get_node_attributes(G,'y_end').values())

    node_xs = [(G.nodes[i]['x_start'], G.nodes[i]['x_end']) for i in G.nodes]
    node_ys = [(G.nodes[i]['y_start'], G.nodes[i]['y_end']) for i in G.nodes]

    # tour edges
    xs = []
    ys = []
    for i in range(len(tour)-1):
        xs.append((G.nodes[tour[i]]['x_end'], G.nodes[tour[i+1]]['x_start']))
        ys.append((G.nodes[tour[i]]['y_end'], G.nodes[tour[i+1]]['y_start']))
        
    x = x_start + x_end
    x_margin = (max(x) - min(x))*0.085
    x_range = (min(x) - x_margin, max(x) + x_margin)
    y = y_start + y_end
    y_margin = (max(y) - min(y))*0.085
    y_range = (min(y) - y_margin, max(y) + y_margin)

    plot = _blank_plot(G, x_range=x_range, y_range=y_range, **kw)

    cost_text = '%.1f' % tour_cost(G, tour)
    cost = Div(text=cost_text, width=plot.plot_width, align='center')
    plot.multi_line(xs=node_xs, ys=node_ys, line_color='black', line_width=2)
    plot.multi_line(xs=xs, ys=ys, line_color='black', line_width=2,
                    line_dash='dashed')
    plot.circle(x_start, y_start, size=5, line_color='steelblue',
                fill_color='steelblue')
    plot.circle(x_end, y_end, size=5, line_color='#DC0000',
                fill_color='#DC0000')

    # create layout
    grid = gridplot([[plot],[cost]],
                    plot_width=plot.plot_width, plot_height=plot.plot_height,
                    toolbar_location=None,
                    toolbar_options={'logo': None})

    return grid


