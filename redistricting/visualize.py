import geopandas as gpd
import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def draw_adjacency_graph(gdf, G, size=(200, 150)):
    base = gdf.plot(color='white', edgecolor='black', figsize=size, lw=.5)
    edge_colors = ['green' if G[u][v].get('inferred', False) else 'red'
                   for u, v in G.edges]
    pos = {i: (geo.centroid.x, geo.centroid.y)
           for i, geo in gdf.geometry.iteritems()}
    if len(G) == len(gdf) + 1:  # If adj graph with dummy node
        pos[len(gdf)] = (min(gdf.centroid.x), min(gdf.centroid.y))
    nx.draw_networkx(G,
                     pos=pos,
                     ax=base,
                     node_size=1,
                     width=.5,
                     linewidths=.5,
                     with_labels=False,
                     edge_color=edge_colors)
    base.axis('off')
    return base


def politics_map(gdf, politics, districting):
    # Takes a few seconds

    # block : distr num
    inv_map = {block: k for k, district in districting.items()
               for block in district}

    gdf['district'] = pd.Series(inv_map)

    shapes = []
    colors = []
    for name, group in gdf.groupby('district'):
        shapes.append(group.geometry.unary_union)
        colors.append(politics[name])
    shape_series = gpd.GeoSeries(shapes)

    map_gdf = gpd.GeoDataFrame({'geometry': shape_series,
                                'color': pd.Series(colors)})
    ax = map_gdf.plot(column='color', figsize=(15, 15), edgecolor='black', lw=1,
                      cmap='seismic', vmin=.35, vmax=.65)
    gdf.plot(ax=ax, facecolor='none', edgecolor='white', lw=.05)
    ax.axis('off')
    return map_gdf