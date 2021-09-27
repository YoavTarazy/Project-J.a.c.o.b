from typing import Collection
import magpylib as mag3
from magpylib._lib.display.display import display
import numpy as np
import scipy as sp
from scipy.spatial.transform import Rotation as R
import math


###Generates points on the XY plain 

def find_points_in_circle(num_of_points,center_of_circle,length_of_radius):
    angle=360/num_of_points
    aggregated_angle=0
    list_of_points=[]
    list_of_points.append((center_of_circle[0]+length_of_radius,center_of_circle[1],0))
    for p in range(num_of_points-1):
        aggregated_angle=aggregated_angle+angle
        list_of_points.append(calculate_point_in_unit_circle(length_of_radius,aggregated_angle,center_of_circle))
    
    return list_of_points

#Calculates a point through a unit circle.        
def calculate_point_in_unit_circle(length_of_radius,angle,center_of_circle):
    if angle<90 and angle>0:
        return (center_of_circle[0]+(length_of_radius*math.cos(math.radians(angle))),center_of_circle[1]+(length_of_radius*math.sin(math.radians(angle))),0)
    elif angle>90 and angle<180:
        return (center_of_circle[0]-(length_of_radius*math.cos(math.radians(180-angle))),center_of_circle[1]+(length_of_radius*math.sin(math.radians(180-angle))),0)
    elif angle>180 and angle<270:
        return (center_of_circle[0]-(length_of_radius*math.cos(math.radians(angle-180))),center_of_circle[1]-(length_of_radius*math.sin(math.radians(angle-180))),0)
    elif angle>270 and angle<360:
        return ((center_of_circle[0]+(length_of_radius*math.cos(math.radians(360-angle)))),center_of_circle[1]-(length_of_radius*math.sin(math.radians(360-angle))),0)
    elif angle==0 or angle==360:
        return (center_of_circle[0]+length_of_radius,center_of_circle[1],0)
    elif angle==90:
        return (center_of_circle[0],center_of_circle[1]+length_of_radius,0)
    elif angle==180:
        return (center_of_circle[0]-length_of_radius,center_of_circle[1],0)
    elif angle==270:
        return (center_of_circle[0],center_of_circle[1]-length_of_radius,0)
    
