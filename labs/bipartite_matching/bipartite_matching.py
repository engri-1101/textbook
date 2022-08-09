import math 
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
import copy
import pickle
from bokeh import palettes
from bokeh.plotting import figure, show
from bokeh.io import output_notebook
from bokeh.tile_providers import get_provider, Vendors
from bokeh.models import (GraphRenderer, Circle, MultiLine, StaticLayoutProvider,
                          HoverTool, TapTool, EdgesAndLinkedNodes, NodesAndLinkedEdges,
                          ColumnDataSource, LabelSet, NodesOnly)

def pu_do_nodes(trips):
    # Intialize nodes and edges
    DO_nodes = list()
    PU_nodes = list()
    # Initialize a dict that maps a PU node to a DO node
    PUtoDO = dict()
    for index, row in trips.iterrows():
        s = row['start_node']
        t = row['end_node']
        s_t = row['start_time']
        t_t = s_t + row['trip_time']
        DO_node = (int(t), t_t, index, 'DO')
        PU_node = (int(s), s_t, index, 'PU')
        DO_nodes.append(DO_node)
        PU_nodes.append(PU_node)
        PUtoDO[PU_node] = DO_node
    return DO_nodes, PU_nodes, PUtoDO
    
def match_to_path(match, trips):
    """Get the taxis paths according to the bipartite matching"""
    DO_nodes, PU_nodes, PUtoDO = pu_do_nodes(trips)
    unmatch_PU = list(set(PU_nodes) - set(match.keys()))
    # track the paths of the taxis
    opt_paths = []
    for PU_node in unmatch_PU:
        path = []
        # Find the drop-off node corresponding to the first unmatched pick-up node
        next_node = PUtoDO[PU_node]
        path.append((PU_node, next_node, True))
        while next_node in match.keys():
            if next_node[-1] == 'PU':
                cur_node = copy.deepcopy(next_node)
                next_node = PUtoDO[cur_node]
                path.append((cur_node, next_node, True))
            else:
                cur_node = copy.deepcopy(next_node)
                next_node = match[cur_node]
                path.append((cur_node, next_node, False))
        opt_paths.append(path)
    return opt_paths
    
def get_og_path(trips):
    """Get the original taxi paths based on the trip information"""
    taxi_list = pd.unique(trips.medallion)
    og_paths = []
    for taxi_id in taxi_list:
        taxi_trips = trips[trips.medallion == taxi_id]
        path = []
        # Append the first trip to the path
        first_row = taxi_trips.iloc[0]
        first_index = taxi_trips.index[0]
        PU_node = (first_row['start_node'], first_row['start_time'], first_index, 'PU')
        DO_node = (first_row['end_node'], first_row['start_time'] + first_row['trip_time'], first_index, 'DO')
        path.append((PU_node, DO_node, True))
        prev_DO = copy.deepcopy(DO_node)
        # Iterate through the rest of the trips
        for index, row in taxi_trips.iloc[1:].iterrows():
            PU_node = (row['start_node'], row['start_time'], index, 'PU')
            DO_node = (row['end_node'], row['start_time'] + row['trip_time'], index, 'DO')
            path.append((prev_DO, PU_node, False))
            path.append((PU_node, DO_node, True))
            prev_DO = copy.deepcopy(DO_node)
        og_paths.append(path)
    return og_paths
    
def street_network(nodes_df, arcs_df):
    # Construct the street network
    G = nx.Graph()
    for l in range(len(nodes_df)):
        G.add_node(l)
    for index, row in arcs_df.iterrows():
        i = row['start']
        j = row['end']
        G.add_edge(i, j, weight = row['trip_time'])
    return G

def get_taxi_stats(taxi_paths, trips_df):
    """Get statistics of every taxi."""
    paths_stats =[]
    for paths in taxi_paths:
        path_stats = []
        for path in paths:
            tail = path[1]
            head = path[0]
            time = tail[1] - head[1]
            moving = (tail[0] != head[0])
            not_empty = path[2]
            trip_id = head[2]
            path_stats.append((time, moving, not_empty, trip_id))
        paths_stats.append(path_stats)

    taxi_stats = []
    for path in paths_stats:
        unzipped = list(zip(*path))
        total_time = sum(np.array(unzipped[0]))
        moving_time = sum(np.array(unzipped[0])[list(unzipped[1])])
        trip_time = sum(np.array(unzipped[0])[list(unzipped[2])])
        trip_IDs = list(np.array(unzipped[3])[list(unzipped[2])])
        num_trips = len(trip_IDs)
        taxi_stats.append({'moving_pct' : moving_time / total_time,
                           'on_trip_pct' : trip_time / total_time,
                           'num_trips' : num_trips,
                          'total_time': total_time / 60,
                          'total_empty': (total_time - trip_time)/60})
    return taxi_stats

def agg_stats(taxi_stats):
    B_max = len(taxi_stats)
    avg_moving_pct = sum([stat['moving_pct'] for stat in taxi_stats]) / B_max
    avg_trip_pct = sum([stat['on_trip_pct'] for stat in taxi_stats]) / B_max
    avg_trip_time = sum([stat['total_time'] for stat in taxi_stats]) / B_max
    avg_empty_time = sum([stat['total_empty'] for stat in taxi_stats]) / B_max
    avg_num_trip = sum([stat['num_trips'] for stat in taxi_stats]) / B_max
    
    print('Summary Statistics')
    print('Total Taxis: ', B_max)
    print('Avg. Moving Pct.: %.2f' % (avg_moving_pct))
    print('Avg. On Trip Pct.: %.2f' % (avg_trip_pct))
    print('Avg. Total Trip Time: %.2f hr' % (avg_trip_time))
    print('Avg. Empty Trip Time: %.2f hr' % (avg_empty_time))
    print('Avg. Number of Trips: %.2f' % (avg_num_trip))

def plot_ex_bipartite(B, match, paths, with_labels = False):
    """Plot the example bipartite graph;
    color the maximum cardinality matching in red and
    color the nodes according to their paths"""
    DO_nodes = {n for n, d in B.nodes(data = True) if d["bipartite"] == 0}
    PU_nodes = set(B) - DO_nodes
    # Sort the nodes by trip_id
    DO_nodes = sorted(DO_nodes, key = lambda x: x[2], reverse = True)
    PU_nodes = sorted(PU_nodes, key = lambda x: x[2], reverse = True)
    # Edge colored in red if it belongs to the max card matching
    edge_color = []
    for edge in B.edges:
        if (edge[0], edge[1]) in match.items():
            edge_color.append('tab:red')
        else:
            edge_color.append('black')
    # Decide node colors based on the correspong paths
    color_map = []
    colors = palettes.Plasma[len(paths)]
    for node in B:
        for i in range(len(paths)):
            if node in list(zip(*paths[i]))[0] + list(zip(*paths[i]))[1]:
                color_map.append(colors[i])
                
    plt.figure(figsize=(8, 6), dpi = 100)
    plt.margins(x=0.3)
    pos = dict()
    pos.update((n, (1, i+1)) for i, n in enumerate(DO_nodes)) 
    pos.update((n, (5, i+1)) for i, n in enumerate(PU_nodes)) 
    nx.draw(B, pos=pos , with_labels = with_labels, node_size = 500, node_color = color_map,alpha = 0.75, edge_color = edge_color, width = 2, linewidths = 2, edgecolors = 'black',font_size=10)
    plt.show()

def plot_taxi_route(G, paths, nodes_df, title = 'Taxi Routes'):
    """Plot the path of every taxi in the given list on the Manhattan grid."""
    # parallel lists for every arc
    start = []  # start node
    end = []  # end node
    color = []  # color code by taxi
    alpha = []  # opacity lower on trip arcs

    # parallel lists for initial location nodes
    start_nodes = []
    start_colors = []

    colors = palettes.Plasma[len(paths)]
    c = 0

    for path in paths:
        # add start node information for this taxi
        start_nodes.append(path[0][0][0])
        start_colors.append(colors[c])
        for comp in path:
            try:
                shortest_path = nx.shortest_path(G, source= comp[0][0], target= comp[1][0], weight = 'weight')
                for i in range(0, len(shortest_path) - 1):
                    start.append(shortest_path[i])
                    end.append(shortest_path[i + 1])
                    alpha.append({True : 1, False : 0.3}[comp[2]])
                    color.append(colors[c])
            except nx.NetworkXNoPath:
                start.append(comp[0][0])
                end.append(comp[1][0])
                alpha.append({True : 1, False : 0.3}[comp[2]])
                color.append(colors[c])
        c = c + 1 if c < len(colors)-1 else 0

    # parallel lists for nodes
    nodes = nodes_df.loc[list(set(start + end))]
    node_ids = nodes.name.values.tolist()
    x = nodes.x.values.tolist()
    y = nodes.y.values.tolist()

    # get plot boundaries
    min_x, max_x = min(nodes.x)-1000, max(nodes.x)+1000
    min_y, max_y = min(nodes.y)-1000, max(nodes.y)+1000

    plot = figure(x_range=(min_x, max_x), y_range=(min_y, max_y),
                  x_axis_type="mercator", y_axis_type="mercator",
                  title= title, plot_width=600, plot_height=470)
    plot.add_tile(get_provider(Vendors.CARTODBPOSITRON_RETINA))

    graph = GraphRenderer()

    # define initial location nodes
    graph.node_renderer.data_source.add(start_nodes, 'index')
    graph.node_renderer.data_source.add(start_colors, 'start_colors')
    graph.node_renderer.glyph = Circle(size=10,line_width=1,fill_alpha=1, fill_color='start_colors', line_color='black')

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

    plot.renderers.append(graph)
    show(plot)

def plot_stats(og_taxi_stats, opt_taxi_stats):
    """Plot statistics using matplotlib."""        
    fig, axs = plt.subplots(2, 2, tight_layout=True, figsize=(15,10))
    FONT_SIZE = 15
    plt.rcParams.update({'font.size': FONT_SIZE})
    
    def plot_histogram(stat, title, x_label, i, j):
        x = [i[stat] for i in og_taxi_stats]
        y = [i[stat] for i in opt_taxi_stats]
        axs[i,j].hist(x, label = 'Original', alpha = 0.8)
        axs[i,j].hist(y, color ='tab:red', label = 'Optimal', alpha = 0.7)
        axs[i,j].axvline(np.mean(x), color='blue', linestyle='dashed', linewidth=1)
        axs[i,j].axvline(np.mean(y), color='red', linestyle='dashed', linewidth=1)
        axs[i,j].legend(loc="best", prop={'size': FONT_SIZE});
        
        axs[i,j].set_xlabel(x_label)
        axs[i,j].set_ylabel('Frequency')
        axs[i,j].set_title(title)

    plot_histogram(stat='on_trip_pct',
                   title='Histogram of On Trip Percentage',
                   x_label='Percent of time a taxi was on a trip', i=0, j=0)

    plot_histogram(stat='num_trips',
                   title='Histogram of Trips Accommodated',
                   x_label='Number of trips given', i=0, j=1)

    plot_histogram(stat='total_empty',
                   title='Histogram of Total Empty Trip Time',
                   x_label='Total Empty Trip Time (hr)', i=1, j=0)

    plot_histogram(stat='total_time',
                   title='Histogram of Total Trip Time',
                   x_label='Total Trip Time (hr)', i=1, j=1)
    plt.show(fig)

def get_day_dist(og_paths, opt_paths, times):
    """ 
    Distribution of the orignal taxi fleets and the minimum taxi fleets over one day
    Return a dictionary where keys are seconds and values are the list of taxi data
    at that time (original # taxis, minimum # taxis, # taxis with passengers, 
    # taxis driving to pickup, # taxis waiting to pickup).
    """
    day_data = dict()
    for time in np.arange(0, 1441):
        time_data = list()
        # Original total number of taxis
        total_count = 0
        for i in og_paths:
            start_time = i[0][0][1]
            end_time = i[-1][1][1]
            if start_time <= time and end_time >= time:
                total_count += 1
        # Minimum number of taxis required
        min_fleet = 0
        with_pass = 0
        do2pu = 0
        wait = 0
        for i in opt_paths:
            start_time = i[0][0][1]
            end_time = i[-1][1][1]
            if start_time <= time and end_time >= time:
                min_fleet += 1
                for comp in i:
                    if comp[0][1] <= time and comp[1][1] >= time:
                        if comp[2]:
                            with_pass += 1
                        else: 
                            start_wait_time = comp[0][1] + times[(comp[0][0], comp[1][0])]
                            if time < start_wait_time:
                                do2pu += 1
                            else:
                                wait += 1
                        break
        time_data.extend((total_count, min_fleet, with_pass, do2pu, wait))
        day_data[time] = time_data
    return day_data

def plot_taxi_dist(day_data):
    """Plot taxi distribution over a day""" 
    plt.rcParams.update({'font.size': 25})
    fig, ax= plt.subplots(1,1, figsize=(25, 15))
    unzipped = list(zip(*day_data.values()))
    og_avg = np.mean(unzipped[0]) 
    opt_avg = np.mean(unzipped[1])
    plt.plot(day_data.keys(), [og_avg] *1441, 'black', linestyle='dashed', label = 'Original Average Fleet Size')
    plt.plot(day_data.keys(), [opt_avg] * 1441, 'red', linestyle='dashed', label = 'Optimal Average Fleet Size')
    c = ['black', 'red', 'orange', 'blue', 'green']
    legends = ['Original Total On the Road', 'Optimal Total On the Road', 'With Passengers', 'Driving to Pickup', 'Waiting to Pickup']
    i = 0
    for data in unzipped:
        plt.plot(day_data.keys(), data, c[i], label = legends[i], linewidth= 3)
        i = i + 1

    ax.xaxis.set_minor_locator(MultipleLocator(6))
    ax.set_xlim([0, 1440])
    ax.set_xticks(np.arange(0, 1450, 60))
    ax.set_xticklabels(['%s:00'%str(i) for i in (list(np.arange(0, 24)) + [0])]);
    ax.tick_params(axis="x",direction="in", which ='major', size= 10, rotation = 45)
    ax.tick_params(axis="y",direction="in", which ='major', size= 10)
    ax.legend(loc="best", prop={'size': 25})
    ax.set_xlabel('Time')
    ax.set_ylabel('Number of Taxis');

def num_circulating(day_data):
    unzipped = list(zip(*day_data.values()))
    print('original number of circulating taxis', round(np.mean(unzipped[0])))
    print('optimal number of circulating taxis', round(np.mean(unzipped[1])))

