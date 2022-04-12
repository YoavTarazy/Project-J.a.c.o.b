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
<<<<<<< Updated upstream
import time 

##Singular point test
@nb.njit()
def check_point_in_triangles(triangles:np.array,point:np.array):
    
    inside=True
    for t in triangles:
            for v in t:
                p0,p1=v[0],v[1]
                if (point[0]-p0[0])*(p1[1]-p0[1])-(point[1]-p0[1])*(p1[0]-p0[0])<0:
                        inside=False
                        break
    return inside#



#Full numba powered point containing checker
@nb.njit()
def check_if_all_points_inside_triangles(triangles:np.array,points:np.array):
    
    inside_or_not=np.ones(points.shape[0],dtype=np.bool_)
    
    for p in range(points.shape[0]):
        inside_or_not[p]=check_point_in_triangles(triangles,points[p])
    return inside_or_not
               
def numpy_polygon_rectangle(minx,miny,maxx,maxy)->np.array:
    
    x_rec=np.linspace(minx,maxx,1000)
    y_rec=np.linspace(miny,maxy,1000)
    rec_dim1,rec_dim2=np.meshgrid(x_rec,y_rec)
    rec=np.asarray(np.meshgrid(x_rec,y_rec))
    rec_dim1_flat=rec_dim1.ravel()
    rec_dim2_flat=rec_dim2.ravel()
    rec_coordinates=np.c_[rec_dim1_flat,rec_dim2_flat]
    return np.asarray(rec_coordinates)

def find_numpy_center_coords(numpy_pic:np.array)->float:
    y,x,rgba=numpy_pic.shape
    return y/2,x/2
 
    
    
    












=======
from numba.typed import Dict
import time
import pandas as pd
from scipy.optimize import minimize




###################### General Mathematical Functions ######################

@nb.vectorize
def check_point_in_triangles(px:float,py:float,x1:float,y1:float,x2:float,y2:float,x3:float,y3:float):
    
    if ((x2-x1)*(py-y1)-(y2-y1)*(px-x1)<0) & ((x3-x2)*(py-y2)-(y3-y2)*(px-x2)<0) & ((x1-x3)*(py-y3)-(y1-y3)*(px-x3)<0):
        return True
    return False



def manifest_polygon_from_circle():
    pass


###################### POLYGON SYSTEM GENERATOR ###############################


#Creating new polygon with regard s to existing ones -> needs refactoring, no need to create new columns in dataframe to perform the calculation!

def t_min_max(t,edge_point1_x,edge_point1_y,edge_point2_x,edge_point2_y,centers_radiuses):
       
       cr=centers_radiuses
       cr['edge1_x'],cr['edge1_y'],cr['edge2_x'],cr['edge2_y']=edge_point1_x,edge_point1_y,edge_point2_x,edge_point2_y
       cr['t_min']= (np.sqrt((cr['edge1_x']+t*(cr['edge2_x']-cr['edge1_x'])-cr['cx'])**2\
                     +(cr['edge1_y']+t*(cr['edge2_y']-cr['edge1_y'])-cr['cy'])**2)-cr['radius'])
       
       return -cr['t_min'].min() 

def calculate_desired_radius(edge:pd,rel_cr:pd,):
    
    
    bnds=((edge['ti'],edge['tf']),)
    
    return minimize(t_min_max,x0=(0.5),args=(edge['p1x'],edge['p1y'],edge['p2x'],edge['p2y'],rel_cr),bounds=bnds)


#Re-parameterizing new polygon's edges

# checks if the parameterized point is inside a triangle - returns: (-1) if outside all triangles and (0) if inside even one triangle
def parameter_point_in_triangle(t,edge,rel_cr):
    pass
    

#Using the function above, i'll minimize it and if the minimize return the value 0, i know theres no t that satisfies. if it is 01 then ill choose the first and last one that represent my new boundries.  
def recalculate_new_titf(edge:pd,rel_cr):
    
    pass





######################## Physics Calculations ########################



######################### Matplotlib to Image domain matrix function #########################







######################## Distance Calculations ########################







    
                
        
            
  