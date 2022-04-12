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







    
                
        
            
  