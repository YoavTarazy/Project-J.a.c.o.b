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
        return (int(center_of_circle[0]+(length_of_radius*math.cos(math.radians(angle)))),int(center_of_circle[1]+(length_of_radius*math.sin(math.radians(angle)))),0)
    elif angle>90 and angle<180:
        return (int(center_of_circle[0]-(length_of_radius*math.cos(math.radians(180-angle)))),int(center_of_circle[1]+(length_of_radius*math.sin(math.radians(180-angle)))),0)
    elif angle>180 and angle<270:
        return (int(center_of_circle[0]-(length_of_radius*math.cos(math.radians(angle-180)))),int(center_of_circle[1]-(length_of_radius*math.sin(math.radians(angle-180)))),0)
    elif angle>270 and angle<360:
        return (int(center_of_circle[0]+(length_of_radius*math.cos(math.radians(360-angle)))),int(center_of_circle[1]-(length_of_radius*math.sin(math.radians(360-angle)))),0)
    elif angle==0 or angle==360:
        return (int(center_of_circle[0]+length_of_radius),int(center_of_circle[1]),0)
    elif angle==90:
        return (int(center_of_circle[0]),int(center_of_circle[1]+length_of_radius),0)
    elif angle==180:
        return (int(center_of_circle[0]-length_of_radius),int(center_of_circle[1]),0)
    elif angle==270:
        return (int(center_of_circle[0]),int(center_of_circle[1]-length_of_radius),0)
    
#checks to see if circles intersect, returns bool. also recives a 2-n tuple that consists of 1 2-tuple list of center coord and radius
def check_if_circles_intersect(list_of_prior_circles,center,radius):
    intersect=False
    for pc in list_of_prior_circles:
        distsq=(pc[0][0]-center[0])**2+(pc[0][1]-center[1])**2
        radsumsq=(radius+pc[1])**2
        if distsq<1.5*radsumsq:
            intersect=True
            
    return intersect

def find_incline(point1,point2):
    incline=(point2[1]-point1[1])/(point2[0]-point1[0])
    return incline

def find_connecting_point(point1,point2,point3):
    incline=find_incline(point1,point2)
    rev_incline=-(1/incline)
    
     
    