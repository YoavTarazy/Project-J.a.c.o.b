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
        return 'y_parralel'
    incline=(point2[1]-point1[1])/(point2[0]-point1[0])
    return incline

    
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
    
    
    #checking if line from center to point is y_parralel
    if line_function1[2]=='y_parralel':
        x=line_function1[0][0]
        if line_function2[2]==0:
            y=line_function2[0][1]
            is_intersect=True
            is_special=True
            return is_special,is_intersect,x,y
        #This checks if the incline is different than 0
        else:
            y=line_function2[2]*x+line_function2[3]
            is_intersect=True
            return is_special,is_intersect,x,y
        
    #Checking if the line of the polygon function is y_parralel
    if line_function2[2]=='y_parralel':
        x=line_function2[0][0]
        if line_function1[2]==0:
            y=line_function1[0][1]
            is_intersect=True
            is_special=True
            return is_special,is_intersect,x,y
        else:
            y=line_function1[2]*x+line_function1[3]
            is_intersect=True
            return is_special,is_intersect,x,y
    
    #Checking if the incline is the same
    if math.isclose(line_function1[2],line_function2[2]):
        return is_special,is_intersect,-1,-1
    
    #Checks if only polygon line is 0 incline
    if line_function2[2]==0:
        y=line_function2[0][1]
        x=(y-line_function1[3])/line_function1[2]
        is_intersect=True
        return is_special,is_intersect,x,y   
        
    is_intersect=True
    try:
        x=(line_function2[3]-line_function1[3])/line_function1[2]-line_function2[2]
    except ZeroDivisionError:
        print('center to point function:',line_function1)
        print('polygon function: ',line_function2)
        print('error')
        
    y=line_function1[2]*x+line_function1[3]
    return is_special,is_intersect,x,y
        

#Check if a point that represents intersection is on the line function of the polygon
def check_if_point_is_a_valid_intersection(point_intersection,line_function):
    dist_total=math.dist(line_function[0],line_function[1])
    dist_modular=math.dist(line_function[0],point_intersection)+math.dist(line_function[1],point_intersection)
    if abs(dist_total-dist_modular)<5:
        return True
    return False


#finds the best possible intersection point and returns its corresponding poligon funcitons
def find_intersect_line_return_dist(point,center_to_point_function,list_of_line_functions_in_polygon):
    p=0
    while p<len(list_of_line_functions_in_polygon):
        is_special,is_intersect,x,y=find_intersection_point(center_to_point_function,list_of_line_functions_in_polygon[p])
        if is_intersect:
            if check_if_point_is_a_valid_intersection((x,y),list_of_line_functions_in_polygon[p]):
                if is_special:
                    return abs(point[0]-list_of_line_functions_in_polygon[p][0][0])
                if list_of_line_functions_in_polygon[p][2]==0:
                    return abs(list_of_line_functions_in_polygon[p][0][1]-point[1])
                
                rev_incline=-(1/list_of_line_functions_in_polygon[p][2])
                n=point[1]-rev_incline*point[0]
                    
                x_new=(list_of_line_functions_in_polygon[p][3]-n)/(rev_incline-list_of_line_functions_in_polygon[p][2])
                y_new=rev_incline*x_new+n
                    
                return math.dist((x_new,y_new),point)
                    
        p=p+1

#Calculate all points
def find_all_distances_from_polygon_line(point,list_of_centers,list_of_polygon_dots):
    
    #First, we will build all needed functions
    list_of_line_functions_between_polygon_dots=build_line_funcitons_in_designated_polygon(list_of_polygon_dots)
    dist_closest_center,center=find_closest_center_to_inquired_point(list_of_centers,point)
    closest_center_to_point_function=build_straight_line_function(point,center)
    
    #Secondly, check for the best intersection point
    return find_intersect_line_return_dist(point,closest_center_to_point_function,list_of_line_functions_between_polygon_dots)

       
    
############################################ NEW TRY


def find_polygons_by_points(centers,polygon_points):
    dic={}
    for center in centers:
        dic[center]=[]
    for poly_point in polygon_points:
        first_dist=math.dist(poly_point,centers[0])
        chosen_center=centers[0]
        for center in centers[1:]:
            sec_dist=math.dist(poly_point,center)
            if first_dist>sec_dist:
                first_dist=sec_dist
                chosen_center=center
        dic[chosen_center].append(poly_point)
    print(dic)
    return dic

def create_all_poly_functions(dic_centers_polygons):
    #Create all straight line functions between polygon points to center
    poly_to_centers={}
    poly_to_poly={}
    for center in dic_centers_polygons.keys():
        poly_to_centers[center]=[]
        for poly_point in dic_centers_polygons[center]:
            poly_to_centers[center].append(build_straight_line_function(poly_point,center))
    
    for center in dic_centers_polygons.keys():
        poly_to_poly[center]=[]
        poly_to_poly[center].append(build_straight_line_function(dic_centers_polygons[center][0],dic_centers_polygons[center][1]))
        for poly_point in dic_centers_polygons[center][1:-1]:
            poly_to_poly[center].append(build_straight_line_function(poly_point,dic_centers_polygons[center][dic_centers_polygons[center].index(poly_point)+1]))
        poly_to_poly[center].append(build_straight_line_function(dic_centers_polygons[center][0],dic_centers_polygons[center][-1]))
           
    print("this is all center to polygon points functions:")
    print(poly_to_centers)
    print("this is all poly to poly functions")
    print(poly_to_poly)
    return poly_to_centers,poly_to_poly
            
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
        if smallest_polly in point_dic_centers_polygons[center]:
            if point_dic_centers_polygons[center][0]==two_poly_points[0]:
                smallest_polly=point_dic_centers_polygons[center][1]
                dist0=math.dist(smallest_polly,point)
                for poly in point_dic_centers_polygons[center][2:]:
                    dist1=math.dist(poly,point)
                    if dist0>dist1:
                        dist0=dist1
                        smallest_polly=poly
                two_poly_points.append(smallest_polly)
                relevant_center=center
            else:
                smallest_polly=point_dic_centers_polygons[center][0]
                dist0=math.dist(smallest_polly,point)
                for poly in point_dic_centers_polygons[center][1:]:
                    if poly!=two_poly_points[0]:
                        dist1=math.dist(poly,point)
                        if dist0>dist1:
                            dist0=dist1
                            smallest_polly=poly
                two_poly_points.append(smallest_polly)
                relevant_center=center

    return two_poly_points,relevant_center
                
def find_poly_func(poly_to_poly,two_poly_list):
    for center in poly_to_poly.keys():
        for polyfunc in poly_to_poly[center]:
            if poly_to_poly[center][0]==two_poly_list[0] and poly_to_poly[center][1]==two_poly_list[1] or poly_to_poly[center][1]==two_poly_list[0] and poly_to_poly[center][0]==two_poly_list[1]:
                return polyfunc                  
                
def find_intersection_point_and_dist(point,two_poly_list):
    polyfunc=build_straight_line_function(two_poly_list[0],two_poly_list[1])
    if polyfunc[2]=='y_parralel':
        x=abs(point[0]-polyfunc[0][0])
        y=point[1]
        return math.dist((x,y),point)
    elif polyfunc[2]==0:
        y=abs(point[1]-polyfunc[0][1])
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