from typing import Collection
import magpylib as mag3
from magpylib._lib.display.display import display
import numpy as np
import scipy as sp
from scipy.spatial.transform import Rotation as R
import math
from shapely.geometry import LineString
import random

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
        return (center_of_circle[0]+(length_of_radius*math.cos(math.radians(360-angle))),center_of_circle[1]-(length_of_radius*math.sin(math.radians(360-angle))),0)
    elif angle==0 or angle==360:
        return (center_of_circle[0]+length_of_radius,center_of_circle[1],0)
    elif angle==90:
        return (center_of_circle[0],center_of_circle[1]+length_of_radius,0)
    elif angle==180:
        return (center_of_circle[0]-length_of_radius,center_of_circle[1],0)
    elif angle==270:
        return (center_of_circle[0],center_of_circle[1]-length_of_radius,0)
    
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


#check ancgle
def find_angle(point1,point2):
        return math.degrees(math.asin((point2[1]-point1[1])/math.dist(point2,point1)))

#Creates a polygon 
def creating_polygon_on_field(num_of_points,starting_angle,center_of_shape,radius):
    
    canon_angle=360/num_of_points
    points_in_shape=[]
    agregated_angle=starting_angle
    for p in range(num_of_points):
        
        points_in_shape.append(calculate_point_in_unit_circle(radius,agregated_angle,center_of_shape))
        agregated_angle=agregated_angle+canon_angle
        
    return points_in_shape

#Creates alot of polygons
def creating_polygon_system(first_center,first_radius,num_of_polygons):
    
    polygons={}
    polygons[first_center]=creating_polygon_on_field(random.randint(3,3),0,first_center,first_radius)
    marked_poly_lines=[]
    
    for p in range(num_of_polygons-1):
        
        is_marked=True
        while is_marked==True:
            random_center=random.choice(list(polygons.keys()))
            random__poly_point=random.randint(0,len(polygons[random_center])-2)
            poly_point1=polygons[random_center][random__poly_point]
            poly_point2=polygons[random_center][random__poly_point+1]
            two_poly_list=(poly_point1,poly_point2)
            
            if two_poly_list not in marked_poly_lines:
                is_marked=False
        marked_poly_lines.append(two_poly_list)
        
        #finding angles created by poly line
        angle=find_angle(poly_point1,poly_point2)
        
        #finding mid point and angle from center
        x_mid=(poly_point1[0]+poly_point2[0])/2
        y_mid=(poly_point1[1]+poly_point2[1])/2
        angle_center_mid=find_angle(random_center,(x_mid,y_mid,0))
        
        #creating new polygon
    
        dist=random.uniform((4/5)*first_radius,first_radius)
        new_center=calculate_point_in_unit_circle(dist,angle_center_mid,(x_mid,y_mid))
        new_radius=random.uniform(first_radius/2,(3/4)*first_radius)
        
        polygons[new_center]=creating_polygon_on_field(random.randint(3,3),angle,new_center,new_radius)
        
    return polygons    
        
                
        
    
    
    

   
############################################ NEW TRY

def find_incline(point1,point2):
    if point2[1]-point1[1]==0:
        return 0
    elif point2[0]-point1[0]==0:
        return math.inf
    incline=(point2[1]-point1[1])/(point2[0]-point1[0])
    return incline

#Recieves two points and return a 4-tuple of the points, the incline and the intersection with the y axis
def build_straight_line_function(point1,point2):
    m=find_incline(point1, point2)
    if m==math.inf:
        n=-1
        return (point1,point2,m,n)
    
    n=point1[1]-m*point1[0]
    
    return (point1,point2,m,n)

def find_polygons_by_points(centers,polygon_points):
    dic_polypoints_connected_to_center={}
    for center in centers:
        dic_polypoints_connected_to_center[center]={}
    for poly_point in polygon_points:
        first_dist=math.dist(poly_point,centers[0])
        chosen_center=centers[0]
        for center in centers[1:]:
            sec_dist=math.dist(poly_point,center)
            if first_dist>sec_dist:
                first_dist=sec_dist
                chosen_center=center
        dic_polypoints_connected_to_center[chosen_center][poly_point]=[]
    
    for center in dic_polypoints_connected_to_center.keys():
        poly_points=list(dic_polypoints_connected_to_center[center].keys())
        for main_poly_point in poly_points:
            two_poly_list=[]
            i=0
            while len(two_poly_list)<2 and i<len(poly_points):
                    if main_poly_point!=poly_points[i] and poly_points[i] not in dic_polypoints_connected_to_center[center][main_poly_point]:
                        is_valid=True
                        Line_poly_points=LineString([main_poly_point,poly_points[i]])
                        for poly in poly_points:
                            if (poly!=main_poly_point and poly!=poly_points[i]):
                                Line_center_poly=LineString([center,poly])
                                if Line_poly_points.intersects(Line_center_poly):
                                    is_valid=False
                        if is_valid:
                            two_poly_list.append(poly_points[i])       
                    i=i+1
            dic_polypoints_connected_to_center[center][main_poly_point].append(two_poly_list[0])
            dic_polypoints_connected_to_center[center][main_poly_point].append(two_poly_list[1])
    return dic_polypoints_connected_to_center 
                     
                     
                     
          
def calculate_minimal_distance_from_polygon_points(point,point_dic_centers_polygons,poly_points):
    two_poly_points=[]
    smallest_polly=poly_points[0]
    dist0=math.dist(smallest_polly,point)
    for poly in poly_points[1:]:
        dist1=math.dist(poly,point)
        if dist0>dist1:
            smallest_polly=poly
            dist0=dist1
    two_poly_points.append(smallest_polly) 
    
    for center in point_dic_centers_polygons.keys():
        
        if smallest_polly in list(point_dic_centers_polygons[center].keys()):
            
            neighbour_poly_list=point_dic_centers_polygons[center][smallest_polly]
            dist0=math.dist(point,neighbour_poly_list[0])
            dist1=math.dist(point,neighbour_poly_list[1])
            Line_point_to_secondary_poly1=LineString([point,neighbour_poly_list[0]])
            Line_point_to_secondary_poly2=LineString([point,neighbour_poly_list[1]])
            Line_main_poly_to_sec_poly1=LineString([smallest_polly,neighbour_poly_list[0]])
            Line_main_poly_to_sec_poly2=LineString([smallest_polly,neighbour_poly_list[1]])
            
            if Line_point_to_secondary_poly1.intersects(Line_main_poly_to_sec_poly2):
                two_poly_points.append(neighbour_poly_list[1])
            elif Line_point_to_secondary_poly2.intersects(Line_main_poly_to_sec_poly1):
                two_poly_points.append(neighbour_poly_list[0])     
            else:
                if dist0>=dist1:
                    two_poly_points.append(neighbour_poly_list[1]) 
                else:
                    two_poly_points.append(neighbour_poly_list[0])  
                     
            return two_poly_points,center 
            
                



          
def find_intersection_point_and_dist(point,two_poly_list):
    
    polyfunc=build_straight_line_function(two_poly_list[0],two_poly_list[1])
    
    if polyfunc[2]==math.inf:
        x=abs(polyfunc[0][0])
        y=point[1]
        return math.dist((x,y),point)
    if polyfunc[2]==0:
        y=abs(polyfunc[0][1])
        x=point[0]
        return math.dist((x,y),point)
    
    inv_incline=(-1)/polyfunc[2]
    n=point[1]-inv_incline*point[0]
    
    x_intersect=(n-polyfunc[3])/(polyfunc[2]-inv_incline)
    y_intersect=inv_incline*x_intersect+n
    return math.dist((x_intersect,y_intersect),point)



#Recives the image as numpy array, a dictionary of centers and their relevant poly points and a list of all poly points
#and returns a 2-tuple numpy array of distances and rev center  and the max distance in said numpy array   
def calculate_all_distances_and_find_max_distance(pix,dic_polygons_to_centers,poly_points):
    max_dist=0
    h,w,rgba=pix.shape
    dist=np.zeros((h,w),dtype=float)
    for py in range(h):
        for px in range(w):
            two_point_list,rev_center=calculate_minimal_distance_from_polygon_points((px,py),dic_polygons_to_centers,poly_points)
            dist_point_polyfunc=find_intersection_point_and_dist((px,py),two_point_list)
            if max_dist<dist_point_polyfunc:
                max_dist=dist_point_polyfunc
            dist[py][px]=dist_point_polyfunc
            if py==rev_center[1] and px==rev_center[0]:
                print('stop')    
    return dist,max_dist