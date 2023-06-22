#!/usr/bin/env python
# coding: utf-8

# In[7]:

import pandas as pd
import numpy as np
import math

import itertools
import datetime
import networkx as nx # tool for graphs and graph algorithms

# interactive plotting tools
from bokeh.plotting import figure, show
from bokeh.io import output_notebook
from bokeh.models import (GraphRenderer, Circle, MultiLine, StaticLayoutProvider,
                          HoverTool, TapTool, EdgesAndLinkedNodes, NodesAndLinkedEdges,
                          ColumnDataSource, LabelSet, NodesOnly
                         )


# In[1]:


def getTree(out, dfl, targets=None):
    """
    :param out: networkx shortest path output
    :param dfl: pandas dataframe for links of netwrokx
                with'start_id'and 'end_id' columns
    :return: dict  {edge_id: in_tree}, in_tree is boolean
    """
    # if not target nodes supplied select all
    if targets==None:
        targets = out[0].keys()
        
    # get {(start, end): index} edge dictionary
    temp = dfl.reset_index()  # make 'index' column
    temp.set_index(['start','end'], inplace=True)
    
    # get consecutive pairs from list
    def pairwise(iterable):
        "s -> (s0,s1), (s1,s2), (s2, s3), ..."
        a, b = itertools.tee(iterable)
        next(b, None)
        return list(zip(a, b))  
    
    # gets the set of edges ((head, tail)-tuples) for each path in SP tree
    pairs = [pairwise(out[1][i]) for i in targets]
    pairs = list(itertools.chain(*pairs))      # make one list
    pairs_org = list(set(pairs))               # get unique tuples in list
    pairs_rev = [(y, x) for x, y in pairs_org] # list of reversed tuples
    
    # mark edges used in tree
    # the graph is undirected but indices not; do both directions
    temp['in_tree'] = 0
    temp.loc[temp.index.isin(pairs_org), 'in_tree']= 1  
    temp.loc[temp.index.isin(pairs_rev), 'in_tree'] = 1 
    
    # get index to in_tree dictionary
    tree_dict = pd.Series(temp['in_tree'].values,index=temp['index']).to_dict()
    
    return tree_dict


# In[8]:


def plotNetworkTompkins(nodes, links):
    """
    Plots an interactive map of a Tomkins network.
    """
    dfn = nodes
    dfl = links
    
    # extract data
    node_ids = dfn.name.values.tolist()
    start = dfl.start.values.tolist()
    end = dfl.end.values.tolist()
    cost = dfl.cost.values.tolist()
    x = dfn.x.values.tolist()
    y = dfn.y.values.tolist()
        
    # set graph range
    min_x, max_x = min(dfn.x)-1, max(dfn.x)+1
    min_y, max_y = min(dfn.y)-1, max(dfn.y)+1
    
    plot = figure(x_range=(min_x, max_x), y_range=(min_y, max_y),
                  title="A simple graph of Tomkins County",
                  width=800, height=420
                 )
    
    graph = GraphRenderer()
    
    plot.add_tools(HoverTool(tooltips=[('Node1', '@start'),('Node2', '@end'), ('cost','@cost')]),
                   TapTool()
                  )
    

    # define nodes
    graph.node_renderer.data_source.add(node_ids, 'index')
    graph.node_renderer.glyph = Circle(line_color='steelblue', line_width=2, fill_color='lightblue', size=10)
    graph.node_renderer.hover_glyph = Circle(line_color='lightgreen', line_width=2, fill_color='yellow', size=10)
    graph.node_renderer.selection_glyph = Circle(line_color='orange', line_width=2, fill_color='yellow', size=10)
    # define edges
    graph.edge_renderer.data_source.data = dict(start=start, end=end, cost=cost)
    graph.edge_renderer.glyph = MultiLine(line_color='steelblue', line_alpha=1, line_width=5)
    graph.edge_renderer.hover_glyph = MultiLine(line_color='lightgreen', line_alpha=1, line_width=5)
    graph.edge_renderer.selection_glyph = MultiLine(line_color='orange', line_alpha=1, line_width=5)
    # set node locations
    graph_layout = dict(zip(node_ids, zip(x, y)))
    graph.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)
    

    # inspection policy
    graph.inspection_policy = EdgesAndLinkedNodes()
    # selection policy
    graph.selection_policy = NodesAndLinkedEdges()

    # labels
    source = ColumnDataSource({'x':x,'y':y,'node':node_ids})
    labels = LabelSet(x='x', y='y', text='node', level='glyph', x_offset=5, y_offset=5, source=source)
    plot.add_layout(labels)

    plot.renderers.append(graph)
    
    show(plot)


# In[6]:


def plotTreeTompkins(dfn, dfl):
    """
    plot a shortest path tree
    """
    # extract data
    node_ids = dfn.name.values.tolist()
    start = dfl.start.values.tolist()
    end = dfl.end.values.tolist()
    x = dfn.x.values.tolist()
    y = dfn.y.values.tolist()

    # graph range
    min_x, max_x = min(dfn.x)-1, max(dfn.x)+1
    min_y, max_y = min(dfn.y)-1, max(dfn.y)+1

    plot = figure(x_range=(min_x, max_x), y_range=(min_y, max_y),
                  title="A simple graph of Tompkins County", width=800, height=420) 

    graph = GraphRenderer()

    plot.add_tools(HoverTool(tooltips=[('Name', '@index'), ('cost','@cost')]))
    
    # load data
    opacity = {1: 1, 0:0.1}
    in_tree = dfl.in_tree.map(opacity).values.tolist()
    label = dfn.label.values.tolist()
    graph.node_renderer.data_source.data = dict(index=node_ids, cost=label)
    graph.edge_renderer.data_source.data = dict(start=start, end=end, in_tree=in_tree)
    graph_layout = dict(zip(node_ids, zip(x, y)))

    # style nodes
    graph.node_renderer.glyph = Circle(line_color='green', line_width=2, fill_color='lightgreen', size=10)
    graph.node_renderer.hover_glyph = Circle(line_color='lightgreen', line_width=2, fill_color='yellow', size=10)
    graph.node_renderer.selection_glyph = Circle(line_color='orange', line_width=2, fill_color='yellow', size=10)
    # style edges
    graph.edge_renderer.glyph = MultiLine(line_color='green', line_alpha='in_tree', line_width=5)
    graph.edge_renderer.hover_glyph = MultiLine(line_color='lightgreen', line_alpha=1, line_width=5)
    graph.edge_renderer.selection_glyph = MultiLine(line_color='orange', line_alpha=1, line_width=5)
    # set node locations

    graph.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)

    # inspection policy
    graph.inspection_policy = NodesOnly()

    plot.renderers.append(graph)

    show(plot)





def plotNetwork(nodes, links, title='Plot of Graph', targets=None, on_map=False):
    """
    Plots a static map of a network = (nodes, links).
    :param nodes: pandas df with 'name', 'x', 'y' cols
                  'x' and 'y' treated as mercator coords
    :param links: pandas df with 'start' and 'end' cols
                  with entries matching nodes' names
    :param title: str of graph title
    :param target: list of node names
    :param on_map: boolean for map background
    """
    
    dfn = nodes
    dfl = links
    
    # extract data
    node_ids = dfn.name.values.tolist()
    start = dfl.start.values.tolist()
    end = dfl.end.values.tolist()
    x = dfn.x.values.tolist()
    y = dfn.y.values.tolist()
    
    if targets != None:
        # get a small dataframe of target nodes
        dfp = dfn.loc[dfn['name'].isin(targets)]
        
    # get plot boundaries
    min_x, max_x = min(dfn.x)+2000, max(dfn.x)-2000
    min_y, max_y = min(dfn.y)+2000, max(dfn.y)-2000
    
    plot = figure(x_range=(min_x, max_x), y_range=(min_y, max_y),
                  x_axis_type="mercator", y_axis_type="mercator",
                  title=title,
                  width=600, height=470,
                  toolbar_location=None, tools=[]
                 )
    
    graph = GraphRenderer()
    
    if on_map == True:
        # add map tile
        plot.add_tile("CARTODBPOSITRON_RETINA")
    
    # define nodes
    graph.node_renderer.data_source.add(node_ids, 'index')
    graph.node_renderer.glyph = Circle(line_color='green', line_alpha=0,
                                       fill_color='green', size=3.5,
                                       fill_alpha=0
                                      )
    # define edges
    graph.edge_renderer.data_source.data = dict(start=list(start),
                                                end=list(end)
                                               )
    graph.edge_renderer.glyph = MultiLine(line_color='steelblue',
                                          line_alpha=1, line_width=.6
                                         )
    # set node locations
    graph_layout = dict(zip(node_ids, zip(x, y)))
    graph.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)
    
    plot.renderers.append(graph)

    # add POIS
    source = ColumnDataSource(dfp)
    poi = Circle(x="x", y="y", size=7, line_color='black',
                 fill_color="orange", line_width=1
                )
    
    plot.add_glyph(source, poi)
    
    show(plot)


# In[4]:


def plotShortestPathTree(dfn, dfl, out, targets=None):
    
    in_tree = pd.Series(np.ones(dfl.shape[0]))
    
    if targets != None:
        tree_dict = getTree(out, dfl, targets)
        in_tree = dfl.index.map(tree_dict)
    
    # get raw data as lists
    node_ids = dfn.name.values.tolist()
    start = dfl.start.values.tolist()
    end = dfl.end.values.tolist()
    x = dfn.x.values.tolist()
    y = dfn.y.values.tolist()
    
    # get plot boundaries
    min_x, max_x = min(dfn.x)+2000, max(dfn.x)-2000
    min_y, max_y = min(dfn.y)+2000, max(dfn.y)-2000
    
    # define plot
    plot = figure(x_range=(min_x, max_x), y_range=(min_y, max_y),
                  x_axis_type="mercator", y_axis_type="mercator",
                  title="The NYC road network", width=600, height=470,
                  toolbar_location=None, tools=[]) 

    graph = GraphRenderer()

    # load background tile
    plot.add_tile("CARTODBPOSITRON_RETINA")

    # define categorical mappers for 0-1 variable
    o_map = {1:1, 0:0.6}
    c_map = {1:'orange', 0:'steelblue'}
    w_map = {1:3, 0:0.6}
    e_oct = in_tree.map(o_map).values.tolist()
    e_clr = in_tree.map(c_map).values.tolist()
    e_wth = in_tree.map(w_map).values.tolist()

    # define nodes
    graph.node_renderer.data_source.add(node_ids, 'index')
    graph.node_renderer.glyph = Circle(line_color='green', line_alpha=0, fill_color='green',
                                       size=3.5, fill_alpha=0)

    # define edges
    graph.edge_renderer.data_source.data = dict(start=start, end=end, e_oct=e_oct,
                                                e_clr=e_clr, e_wth=e_wth)
    graph.edge_renderer.glyph = MultiLine(line_color='e_clr', line_alpha='e_oct',
                                          line_width='e_wth')
    # set node locations
    graph_layout = dict(zip(node_ids, zip(x, y)))
    graph.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)

    # appendgraph to plot
    plot.renderers.append(graph)

    # add POIs
    if targets != None:
        # get a small dataframe of pois only
        dfp = dfn.loc[dfn['name'].isin(targets)]
        source = ColumnDataSource(dfp)
        pois = Circle(x="x", y="y", size=7, line_color='orange',
                      fill_color="yellow", line_width=1)
        plot.add_glyph(source, pois)

    show(plot)

