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
        
        #The 1.5 was chosen arbitrarly to space out the polygons when created even further.
        if distsq<1.5*radsumsq:
            intersect=True
            
    return intersect

def find_incline(point1,point2):
    if point2[1]-point1[1]==0:
        return 0
    elif point2[0]-point1[0]==0:
        return 'x_parralel'
    incline=(point2[1]-point1[1])/(point2[0]-point1[0])
    return incline

#A function that finds the closest intersection point
def find_intersect_point(point1,point2,point_inquired):
    
    #Create line function between the two polygon dots
    incline=find_incline(point1,point2)
    if incline=='y_parralel':
        return point_inquired[0],point1[1]
    elif incline=='x_parralel':
        return point1[0],point_inquired[1]
        
    n=point1[1]-incline*point1[0]
    
    #Create line function normal to the polygon line one
    rev_incline=-(1/incline)
    b=point_inquired[1]-(point_inquired[0]*(-rev_incline))
    
    #find point f intersection
    x_intersect=(incline*point1[0]-incline*point1[1]+point_inquired[0]+incline*point_inquired[1])/(incline**2+1)
    y_intersect=incline*x_intersect+n
    
    return x_intersect,y_intersect

#A function to find the two closest points from the polygon points avaidable
def find_two_closest_points_from_point(point_list,point_inquired):
    point1=point_list[0]
    point2=point_list[1]
    dist1=math.dist(point1,point_inquired)
    dist2=math.dist(point2,point_inquired)
    if dist1<dist2:
        dist1,dist2=dist2,dist1
        
    for point in point_list[2:]:
        dist3=math.dist(point,point_inquired)
        if dist3<dist1:
            dist1=dist3
            point1=point
        elif dist3>dist1 and dist3<dist2:
            dist2=dist3
            point2=point
    
    return point1,point2
            

def find_max_distance_in_image(polygon_points):
    dist=math.dist(polygon_points[0],(0,0))
    for polypoint in polygon_points[1:]:
        dist2=math.dist(polypoint,(0,0))
        if dist<dist2:
            dist=dist2
    return dist
    
#Recieves a list of centers and return the closest one to the point with the distance
def find_closest_center_to_inquired_point(list_of_centers,incquired_point):
    dist=math.dist(list_of_centers[0],incquired_point)
    closest_center=list_of_centers[0]
    for center in list_of_centers[1:]:
        dist2=math.dist(center,incquired_point)
        if dist>dist2:
            dist=dist2
            closest_center=center
            
    return dist,closest_center

#Recieves two points and return a 4-tuple of the points, the incline and the intersection with the y axis
def build_straight_line_function(point1,point2):
    m=find_incline(point1, point2)
    if m=='y_parralel':
        n=-1
        return (point1,point2,m,n)
    n=point1[1]-m*point1[0]
    
    return (point1,point2,m,n)



#build all line function between the polygon dots
def build_line_funcitons_in_designated_polygon(list_of_polygon_points):
    list_of_line_functions_in_polygon=[]
    for p in range(len(list_of_polygon_points)-1):
        line_function=build_straight_line_function(list_of_polygon_points[p],list_of_polygon_points[p+1])
        list_of_line_functions_in_polygon.append(line_function)
    return list_of_line_functions_in_polygon

#Returns whether or not an intersection point exists and if so, its coordinates
def find_intersection_point(line_function1,line_function2):
    is_special=False
    is_intersect=False
    #Checking end points where lines are parralel to axis
    if line_function2[2]=='x_parralel':
        x=line_function2[0][0]
        if line_function1[2]=='x_parralel':
            y=-1
            return is_special,is_intersect,x,y
        y=line_function1[2]*x+line_function1[3]
        is_special=True
        is_intersect=True
        return is_special,is_intersect,x,y
    
    if line_function1[2]=='x_parralel':
        x=line_function1[0][0]
        if line_function1[2]=='x_parralel':
            y=-1
            return is_special,is_intersect,x,y
        y=line_function2[2]*x+line_function2[3]
        is_intersect=True
        return is_special,is_intersect,x,y
    if line_function1[2]+line_function2[2]==0:
        x,y=-1,-1
        return is_special,is_intersect,x,y
    
    is_intersect=True
    x=(line_function2[3]-line_function1[3])/line_function1[2]-line_function2[2]
    y=line_function1[2]*x+line_function1[3]
    return is_special,is_intersect,x,y
        

#Check if a point that represents intersection is on the line function of the polygon
def check_if_point_is_a_valid_intersection(point_intersection,line_function):
    dist_total=math.dist(line_function[0],line_function[1])
    dist_modular=math.dist(line_function[0],point_intersection)+math.dist(line_function[1],point_intersection)
    if math.isclose(dist_total,dist_modular):
        return True
    return False


#finds the best possible intersection point and returns its corresponding poligon funcitons
def find_intersect_line_return_dist(point,center_to_point_function,list_of_line_functions_in_polygon):
    p=0
    while p<range(list_of_line_functions_in_polygon):
        is_special,is_intersect,x,y=find_intersection_point(center_to_point_function,list_of_line_functions_in_polygon[p])
        if is_intersect:
            if check_if_point_is_a_valid_intersection((x,y),list_of_line_functions_in_polygon[p]):
                if is_special:
                    return math.abs(point[0]-list_of_line_functions_in_polygon[p][0])
                else:
                    rev_incline=-(1/list_of_line_functions_in_polygon[p][2])
                    n=point[1]-rev_incline*point[0]
                    
                    x_new=(list_of_line_functions_in_polygon[p][3]-n)/(rev_incline-list_of_line_functions_in_polygon[p][2])
                    y_new=rev_incline*x_new+n
                    
                    return math.dist((x_new,y_new),point)
                    
        p=p+1

    
    
        
        
    
              
    
    
    
     
    