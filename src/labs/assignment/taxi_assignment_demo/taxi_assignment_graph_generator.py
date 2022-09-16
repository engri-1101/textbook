import pandas as pd
import numpy as np
import networkx as nx
from ortools.graph import pywrapgraph
import copy
import sys

from bokeh import palettes
from bokeh.plotting import figure, show
from bokeh.tile_providers import get_provider, Vendors
from bokeh.models import (GraphRenderer, Circle, Rect, MultiLine, StaticLayoutProvider,
                          HoverTool, TapTool, EdgesAndLinkedNodes, NodesAndLinkedEdges,
                          ColumnDataSource, LabelSet, NodesOnly)

# Defines the time periods to use for pickup and dropoff, this example starts at 5:00 PM
dropoff_window_start = 1020
dropoff_window_duration = 5
gap_interval_duration = 3
pickup_window_duration = 5

# Enforces travel time to be less than the travel window. Also uses travel times as cost instead of wait time
use_travel_time_as_cost = True

# If this is True, will slide the dropoff window back until there are at least as many dropoffs as pickups
slide_dropoff_window = True

def plot(travel_window):
    global dropoff_window_start
    global dropoff_window_duration

    # Get data from the csv
    trips_df = pd.read_csv('data/2013-09-01_trip_data_manhattan.csv').drop(columns='id')
    nodes_df = pd.read_csv('data/nyc_nodes_manhattan.csv').drop(columns='Unnamed: 0')

    def get_trips(start_time, duration):
        """Returns all trips between start_time and start_time+duration"""
        end_time = start_time + duration
        trips = trips_df.copy()
        trips = trips[(trips.start_time >= start_time) &
                  (trips.start_time + trips.trip_time <= end_time)].copy()
        return trips

    # Load all pickups from the relevant window. Tuple of (Location id, pickup time, trip id, 'PU')
    PU_nodes = []
    trips = get_trips(dropoff_window_start+dropoff_window_duration+gap_interval_duration, pickup_window_duration)
    for index, row in trips.iterrows():
        s = row['start_node']
        s_t = row['start_time']
        PU_node = (int(s), s_t, index, 'PU')
        PU_nodes.append(PU_node)

    # Load all dropoffs from the relevant window. Tuple of (Location id, dropoff time, trip id, 'DO')
    sliding = True
    while sliding:
        DO_nodes = []
        trips = get_trips(dropoff_window_start, dropoff_window_duration)
        for index, row in trips.iterrows():
            t = row['end_node']
            s_t = row['start_time']
            t_t = row['trip_time']
            DO_node = (int(t), s_t + t_t, index, 'DO')
            DO_nodes.append(DO_node)
        if len(DO_nodes) >= len(PU_nodes) or not slide_dropoff_window or dropoff_window_start <= 0:
            sliding = False
        else:
            dropoff_window_start -= 1
            dropoff_window_duration += 1

    # Sort nodes by time
    DO_nodes.sort(key = lambda x: x[1])
    PU_nodes.sort(key = lambda x: x[1])

    # Assign each node a unique integer id
    identifier = 0
    for i, node in enumerate(DO_nodes):
        DO_nodes[i] = tuple(list(node) + [identifier])
        identifier += 1
    for i, node in enumerate(PU_nodes):
        PU_nodes[i] = tuple(list(node) + [identifier])
        identifier += 1

    # Generate time to travel from a DO node to a PU nodes, assumes 2 minutes per km
    # Could instead use a precomputed structure for each node pair
    def compute_time(DO, PU):
        lat1 = nodes_df.loc[DO_node[0], 'lat']
        lon1 = nodes_df.loc[DO_node[0], 'lon']
        lat2 = nodes_df.loc[PU_node[0], 'lat']
        lon2 = nodes_df.loc[PU_node[0], 'lon']
        R = 6371 # Radius of earth in km
        distance = 0.01 + R * np.sqrt((lon1 - lon2)**2 + (lat1 - lat2)**2) * np.pi / 180
        return 2 * distance

    # Create an arc from each DO node to a PU node iff the taxi can make it in time and within travel window
    # [(Start node, end node, cost), ...]
    arcs = []
    for DO_node in DO_nodes:
        for PU_node in PU_nodes:
            if PU_node[1] >= DO_node[1]:
                time = compute_time(DO_node, PU_node)
                arrival_time = DO_node[1] + time
                latest_valid_arrival = PU_node[1] + pickup_window_duration
                if arrival_time <= latest_valid_arrival and time <= travel_window:
                    cost = arrival_time - PU_node[1]
                    if use_travel_time_as_cost:
                        cost = time
                    cost = 0 if cost <= 0 else int(cost * 1000)
                    arcs.append((DO_node, PU_node, cost))

    # Uses networkx to solve a bipartite matching formulation
    B = nx.Graph()
    B.add_nodes_from(DO_nodes, bipartite=0)
    B.add_nodes_from(PU_nodes, bipartite=1)
    B.add_edges_from([arc[:2] for arc in arcs])

    top_nodes = {n for n, d in B.nodes(data = True) if d["bipartite"] == 0}

    match = nx.bipartite.maximum_matching(B, DO_nodes)
    optimal_cardinality = int(len(match) / 2)
    max_match_paths = []
    for do, pu in match.items():
        if pu[3] == 'DO':
            continue
        max_match_paths.append([(do[:4],pu[:4],False)])

    arc_dict = {(arc[0], arc[1]): arc[2] for arc in arcs}
    max_cardinality_cost = sum(arc_dict[(do,pu)] for do, pu in match.items() if pu[3] != 'DO')
    del arc_dict

    # Create a source and sink node
    source = (0,0,0,'SOURCE',identifier)
    identifier += 1
    sink = (0,0,0,'SINK',identifier)
    identifier += 1

    # Add arc from source to each dropoff with cost 0
    for node in DO_nodes:
        arcs.append((source, node, 0))

    # Add arc from each pickup to the sink with cost 0
    for node in PU_nodes:
        arcs.append((node, sink, 0))

    start_nodes = [arc[0][4] for arc in arcs]
    end_nodes = [arc[1][4] for arc in arcs]
    capacities = [1] * len(arcs)
    unit_costs = [arc[2] for arc in arcs]

    supplies = [0] * (identifier)
    supplies[source[4]], supplies[sink[4]] = optimal_cardinality, -1 * optimal_cardinality

    min_cost_flow = pywrapgraph.SimpleMinCostFlow()

    for arc in zip(start_nodes, end_nodes, capacities, unit_costs):
            min_cost_flow.AddArcWithCapacityAndUnitCost(*arc)

    for count, supply in enumerate(supplies):
            min_cost_flow.SetNodeSupply(count, supply)

    status = min_cost_flow.Solve()
    if status != min_cost_flow.OPTIMAL:
        print('There was an issue with the min cost flow input.')
        print(f'Status: {status}')

    min_cost_flow_cost = min_cost_flow.OptimalCost()

    # Find the taxi assignments
    # Creates a dictionary for fast lookups
    trip_dict = {node[4]: node for node in DO_nodes + PU_nodes}
    # Holds the path of each taxi
    min_cost_paths = []
    for i in range(min_cost_flow.NumArcs()):
        if min_cost_flow.Flow(i) == 1 and min_cost_flow.Tail(i) != source[4] and min_cost_flow.Head(i) != sink[4]:
            do = trip_dict[min_cost_flow.Tail(i)]
            pu = trip_dict[min_cost_flow.Head(i)]
            min_cost_paths.append([(do[:4], pu[:4], False)])
    # Free the lookup dictionary
    del trip_dict

    def plot_taxi_route(paths, title='Taxi Routes'):
        """Plot the path of every taxi in the given list on the Manhattan grid."""

        # parallel lists for every arc
        start = []  # start node
        end = []  # end node
        color = []  # color code by taxi
        alpha = []  # opacity lower on trip arcs

        # parallel lists for initial location nodes
        start_nodes = []
        start_colors = []

        end_nodes = []
        end_colors = []

        colors = palettes.Category10[10]
        c = 0

        for path in paths:

            # add start node information for this taxi
            start_nodes.append(path[0][0][0])
            start_colors.append(colors[c])

            # adds a colored node to the end of paths
            end_nodes.append(path[0][1][0])
            end_colors.append(colors[c])

            for comp in path:
                start.append(comp[0][0])
                end.append(comp[1][0])
                alpha.append({True : 0.3, False : 1}[comp[2]])
                color.append(colors[c])

            c = c + 1 if c < len(colors)-1 else 0

        # parallel lists for nodes
        nodes = nodes_df.loc[list(set(start + end))]
        node_ids = nodes.name.values.tolist()
        x = nodes.x.values.tolist()
        y = nodes.y.values.tolist()

        # get plot boundaries
        min_x, max_x = -8240298.040280505, -8230749.832964136
        min_y, max_y = 4968176.938664163, 4984234.650659162

        # get plot boundaries
        if len(nodes.x >= 1):
            min_x, max_x = min(nodes.x)-1000, max(nodes.x)+1000
        if len(nodes.y >= 1):
            min_y, max_y = min(nodes.y)-1000, max(nodes.y)+1000

        plot = figure(x_range=(min_x, max_x), y_range=(min_y, max_y),
                      x_axis_type="mercator", y_axis_type="mercator",
                      title=title, plot_width=600, plot_height=470)
        plot.add_tile(get_provider(Vendors.CARTODBPOSITRON_RETINA))

        graph = GraphRenderer()

        end_graph = GraphRenderer()

        # define initial location nodes
        graph.node_renderer.data_source.add(start_nodes, 'index')
        graph.node_renderer.data_source.add(start_colors, 'start_colors')
        graph.node_renderer.glyph = Circle(size=7,line_width=0,fill_alpha=1, fill_color='start_colors')

        # define end location nodes
        end_graph.node_renderer.data_source.add(end_nodes, 'index')
        end_graph.node_renderer.data_source.add(end_colors, 'end_colors')
        end_graph.node_renderer.glyph = Rect(height=7,width=7,height_units='screen',width_units='screen',line_width=0,fill_alpha=1, fill_color='end_colors')

         # define network edges
        graph.edge_renderer.data_source.data = dict(start=list(start),
                                                    end=list(end),
                                                    color=list(color),
                                                    alpha=list(alpha))
        graph.edge_renderer.glyph = MultiLine(line_color='color', line_alpha='alpha',
                                             line_width=3,line_cap='round')

        # set node locations
        graph_layout = dict(zip(node_ids, zip(x, y)))
        graph.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)

        end_graph.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)

        plot.renderers.append(graph)
        plot.renderers.append(end_graph)
        return plot

    return (plot_taxi_route(max_match_paths, f'Maximum Matching. Cost: {max_cardinality_cost / 1000}. Rides: {optimal_cardinality}.'), plot_taxi_route(min_cost_paths, f'Minimum Cost Maximum Matching. Cost: {min_cost_flow_cost / 1000}. Rides: {optimal_cardinality}.'))
