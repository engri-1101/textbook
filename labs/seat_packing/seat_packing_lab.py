# same imports as in Jupyter Notebook
import pandas as pd
import numpy as np
import math, itertools
import matplotlib.pyplot as plt
import networkx as nx
from ortools.linear_solver import pywraplp as OR
import shapely, shapely.affinity
from shapely.geometry import Polygon, Point

# example 1 visualization
def ex1(nodes,edges):
    # graph creation
    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    # node placement
    pos = {}
    for n in nodes:
        if (n%4)%2 == 0:
            pos.update({n:((n-1)%4,-math.ceil(n/4)-0.25)})
        else:
            pos.update({n:((n-1)%4,-math.ceil(n/4))})

    options = {
    'node_color': 'lightblue',
    'node_size': 500,
    }

    nx.draw_networkx(G, pos=pos, **options)
    plt.axis('off')
    plt.show()


# example 2 image
def ex2(nodes,edges):
    # graph creation
    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    # node placement
    pos = {1:(1,1),2:(3,1),3:(5,1),4:(2,2),5:(4,2),6:(3,3)}

    options = {
    'node_color': 'lightblue',
    'node_size': 500,
    }

    nx.draw_networkx(G, pos=pos, **options)
    plt.axis('off')
    plt.show()


# plant sciences 233 initial image  (code by Sander Aarts)
def ex_room():
    # Defines a chair shape
    arr = np.array([(370, 396), (390, 396), (390, 407), (395, 407), (395, 422), (390, 422),
       (390, 427), (370, 427), (370, 422), (365, 422), (365, 407), (370, 407)])
    
    # Define one row's locations
    locs = list()

    # bulk of rows
    for k in range(0, 11):
        y = (k+1)*42
        # left row locations
        for i in range(0,6):
            locs.append((i*26 -228, y))
        # middle row locations
        for i in range(0,8):
            locs.append((i*26,y))
        # right row locations
        for i in range(0,6):
            locs.append((i*26 + 280, y)) 
            
    # row 1 regular seats
    for i in range(0,3):
        locs.append((i*26 -228, -42))
    for i in range(0,3):
        locs.append(((i+3)*26 + 280, -42))
    # middle row locations
    for i in range(0,7):
        locs.append((i*30,-43))
            
    # row 2 regular seats
    for i in range(0,5):
        locs.append((i*26 -228, 0))
    for i in range(0,5):
        locs.append(((i+1)*26 + 280, 0)) 
    # middle row locations
    for i in range(0,8):
        locs.append((i*26,0))
            
    # row 14 regular seats
    y = 12*42
    for i in range(0,5):
        locs.append((i*26 -228, y))
    for i in range(0,5):
        locs.append(((i+1)*26 + 280, y)) 
    # middle row locations
    for i in range(0,6):
        locs.append((i*28+20,y))
            
    # row 14 regular seats
    y = 13*42+10
    for i in range(0,4):
        locs.append((i*26 -228, y))
    for i in range(0,4):
        locs.append(((i+2)*29 + 268, y)) 
    
    # Generate list of polygons and points
    polys = list()
    points = list()

    for i in range(len(locs)):
        polys.append(Polygon(arr + np.array([locs[i]]*12)))
        points.append(Point(np.array([379, 414] + np.array([locs[i][0], locs[i][1]]))))

    # define a yardstick (seen as orange rectangle in plot below)
    stick_points = np.array([(400, 186), (420, 186), (420, 327), (400, 327)])
    stick = Polygon(stick_points)
    
    # plot the model
    img = plt.imread("images-lab/floorplan.jpg")
    fig, ax = plt.subplots(dpi=300)
    plt.xticks(size = 3.5)
    plt.yticks(size = 3.5)

    for i in range(len(polys)):
        x,y = polys[i].exterior.xy
        ax.plot(x, y, color='blue', alpha=1, linewidth=0.25, solid_capstyle='round', zorder=2)

    # plot yardstick
    x,y = stick.exterior.xy
    ax.fill(x, y, alpha=.5, fc='orange', ec='none', linewidth=0.25, zorder=2)
    
    # plot points
    xs = [point.x for point in points]
    ys = [point.y for point in points]
    plt.scatter(xs, ys, s=0.2, color='blue', alpha=1)

    ax.axhline(y=0, color='k')
    ax.axvline(x=0, color='k')
    ax.imshow(img)

    return polys, points


# plant sciences 233 image w/ solution  (code by Sander Aarts)
def ex_room_sol(df, sol):
    # map solution to dataframe
    df['index_string'] = df.index.astype(str)     # get index as strings, dict is {'id': val}
    df['in_solution'] = df['index_string'].map(sol)

    # plot solutions (airline seat booking style)
    img = plt.imread("images-lab/floorplan.jpg")
    fig, ax = plt.subplots(dpi=300)
    plt.xticks(size = 3.5)
    plt.yticks(size = 3.5)

    # plot chairs
    for i in range(df.shape[0]):
        if (df['in_solution'][i] == 0):
            x,y = df['polygon'][i].exterior.xy
            ax.fill(x, y, alpha=0.8, fc='lightblue', ec='darkblue', linewidth=0.35, zorder=2)
        else:
            x,y = df['polygon'][i].exterior.xy
            ax.fill(x, y, alpha=0.9, fc='orange', ec='darkred', linewidth=0.35, zorder=2)

    # plot circles
    sol_ids = df[df['in_solution']==1].index.values # get points in solution
    for i in sol_ids:
        draw_circle = plt.Circle((df['point'][i].x, df['point'][i].y), 85, fill=False,
                            ec='purple', ls='--', lw=0.2, zorder=4)
        ax.add_artist(draw_circle)

    ax.imshow(img)


# rhodes 571 initial image  (code by Sander Aarts)
def ex_lab():
    floor = 'images-lab/labclassroom.png'

    yardstick = np.array([(295, 231), (305, 231), (305, 316), (295, 316)])
    stick = Polygon(yardstick)

    feet10 = max(yardstick[:,1]) - min(yardstick[:,1])
    feet6 = feet10*(6/10)

    # Define a chair shape (can be rotated later)
    arr = np.array([[ 0,  0], [11,  0], [11, 14.5], [0, 14.5]])
    p = Polygon(arr) # define polygon

    # Define one row's locations
    locs = list()
    rotations = list()

    crs = 1 # coarseness

    y_inc = 16

    # Left wings
    for k in (range(0, 5)):
        y = 51 + k*38
        x_inc = 0
        if (k==4):
            y = y + y_inc
            x_inc = 5
        g = 8/30
        for i in range(0, math.floor((16 - 1*k)/crs)):
            locs.append((31.5 + x_inc + 10*k + i*5*crs , y - i*5*g*crs ))
            rotations.append(-15)
            
    # Right wings
    for k in (range(0, 4)):
        k = k+1
        y = 51 + k*38
        x_inc = 0
        if (k==4):
            y = y + y_inc
            x_inc = -5
        g = 8/30
        for i in range(0, math.floor((16 - 1*k)/crs)):
            locs.append((563 + x_inc - 10*k - i*5*crs , y - i*5*g*crs ))
            rotations.append(15)
            
    # Middle left
    for k in range(0, 5):
        y = 29 + k*39
        if (k==4):
            y = y + y_inc + 2
        for i in range(0, math.floor((19 - 1.2*k)/crs)):
            locs.append((120 + 6*k + i*5*crs , y))
            rotations.append(0)

    # Middle right
    for k in range(0, 5):
        y = 29 + k*39
        if (k==4):
            y = y + y_inc + 2
        if (k != 0):
            n = 20
        if (k == 0):
            n = 18
        for i in range(0, math.floor((n - 1.5*k)/crs)):
            locs.append((382 + i*5*crs , y))
            rotations.append(0)
            
    # Middle
    for k in range(0, 5):
        y = 29 + k*39
        if (k==4):
            y = y + y_inc + 2
        for i in range(0, math.floor((20)/crs)):
            locs.append((248 + i*5*crs , y))
            rotations.append(0)
            
    rotations.append(0)

    # generate list of polygons and points
    polys = list()

    for i in range(len(locs)):
        p = Polygon(arr + np.array([locs[i]]*4))
        p = shapely.affinity.scale(p, xfact=1, yfact=1, origin='center')
        p = shapely.affinity.rotate(p, rotations[i], origin='center')
        polys.append(p)

    # get points centered at each seat polygon
    points = list()
    for i in range(len(polys)):
        p = polys[i].centroid
        p = shapely.affinity.translate(p, xoff=0, yoff=-1, zoff=0.0)
        points.append(p)

    # plot solutions (airline seat booking style)
    img = plt.imread(floor)
    fig, ax = plt.subplots(dpi=300)

    for i in range(len(polys)):
        x,y = polys[i].exterior.xy
        ax.plot(x, y, color='blue', alpha=0.5, linewidth=0.4, solid_capstyle='round', zorder=2)
        
    # plot points    
    xs = [point.x for point in points]
    ys = [point.y for point in points]
    plt.scatter(xs, ys, s=0.1, color='blue', alpha=1, linewidth=0.3)

    # plot stick
    x,y = stick.exterior.xy
    ax.fill(x, y, alpha=0.5, fc='orange', ec='none', linewidth=0.5, zorder=2)

    ax.imshow(img)

    return polys, points


# rhodes 571 image w/ solution  (code by Sander Aarts)
def ex_lab_sol(df, sol):
    # map solution to dataframe
    df['index_string'] = df.index.astype(str) # get index as strings, dict is {'id': val}
    df['in_solution'] = df['index_string'].map(sol)

    # plot all points to verify the matching worked
    img = plt.imread('images-lab/labclassroom.png')

    # set axis tick size
    plt.rc('xtick', labelsize=4) 
    plt.rc('ytick', labelsize=4) 
    fig, ax = plt.subplots(dpi=300)

    # set axis line size
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(0.5)

    # plot chairs
    for i in range(df.shape[0]):
        if (df['in_solution'][i] == 1):
            xs,ys = df['polygon'][i].exterior.xy
            ax.fill(xs, ys, alpha=0.9, fc='orange', ec='darkred', linewidth=0.15, zorder=3)
        
    # plot circles
    sol_ids = df[df['in_solution']==1].index.values # get points in solution
    for i in sol_ids:
        draw_circle = plt.Circle((df['point'][i].x, df['point'][i].y), 51-1, fill=False,
                            ec='purple', ls='--', lw=0.3, zorder=4)
        ax.add_artist(draw_circle)

    ax.imshow(img)