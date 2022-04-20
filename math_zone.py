from typing import Collection
import magpylib as mag3
from magpylib._lib.display.display import display
from numba.np.ufunc import parallel
from numpy.lib.function_base import _rot90_dispatcher

import scipy as sp
from scipy.spatial.transform import Rotation as R
import math
from shapely.geometry import LineString
from shapely import geometry
import random
from matplotlib import path
import sys
import numpy as np
import numba as nb
from numba import cuda
from numba.typed import Dict
import time
import pandas as pd
from scipy.optimize import minimize





###################### General Mathematical Functions ######################

def triangle_area(x1,y1,x2,y2,x3,y3):
    
    return abs((x1 * (y2 - y3) + x2 * (y3 - y1)
                + x3 * (y1 - y2)) / 2.0)

def point_inside_triangle(t,segment_points,tp1,tp2,tp3):
     
    x1,y1=tp1
    x2,y2=tp2
    x3,y3=tp3
    if len(segment_points)==1:
        x,y=segment_points
    else:
        x,y=segment_points[0][0]+t*(segment_points[1][0]-segment_points[0][0]),segment_points[0][1]+t*(segment_points[1][1]-segment_points[0][1])
    
    A = triangle_area(x1, y1, x2, y2, x3, y3)
    A1 = triangle_area(x, y, x2, y2, x3, y3)
    A2 = triangle_area(x1, y1, x, y, x3, y3)
    A3 = triangle_area(x1, y1, x2, y2, x, y)
    
    return float(np.isclose(A,A1+A2+A3))


def manifest_polygon_from_circle(center_point:np,radius:float,num_of_points:int,angle:float):
    
    agg_angle=np.radians(angle)
    cut_angle=2*np.pi/num_of_points
    vertices=[]
    
    for i in range(num_of_points):
        
        vertices.append([center_point[0]+np.cos(agg_angle)*radius,center_point[1]+np.sin(agg_angle)*radius])
        agg_angle=agg_angle+cut_angle
    
    vertices.append(vertices[0])
    return vertices

print(manifest_polygon_from_circle([0,0],10,3,0))

        
    
    


###################### POLYGON SYSTEM GENERATOR ###############################


#Creating new polygon with regard s to existing ones -> needs refactoring, no need to create new columns in dataframe to perform the calculation!

def t_min_max(t,edge,centers_radiuses):
       
       cr=centers_radiuses
       cr['edge1_x'],cr['edge1_y'],cr['edge2_x'],cr['edge2_y']=edge['p1x'],edge['p1y'],edge['p2x'],edge['p2y']
       cr['t_min']= (np.sqrt((cr['edge1_x']+t*(cr['edge2_x']-cr['edge1_x'])-cr['cx'])**2\
                     +(cr['edge1_y']+t*(cr['edge2_y']-cr['edge1_y'])-cr['cy'])**2)-cr['radius'])
       
       return -cr['t_min'].min() 


def create_constraint_dic(rel_edges:pd):
    
    rel_edges['type']='ineq'
    rel_edges['fun']=point_inside_triangle

    records=list(rel_edges[['cx','cy','p1x','p1y','p2x','p2y','radius']].to_records(index=False))
    rel_edges['args']=records
    constraint=rel_edges[['type','fun','args']].to_dict('records')
    
    return constraint

def calculate_desired_radius(edge:pd,rel_cr:pd,constr:list):
    
    
    bnds=((0,1),)
    
    return minimize(t_min_max,x0=(0.5),args=(edge,rel_cr),constraints=constr,bounds=bnds,method='trust-constr')


##########Test







######################## Physics Calculations ########################



######################### Matplotlib to Image domain matrix function #########################







######################## Distance Calculations ########################







    
                
        
            
  