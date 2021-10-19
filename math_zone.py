from typing import Collection
import magpylib as mag3
from magpylib._lib.display.display import display
import numpy as np
import scipy as sp
from scipy.spatial.transform import Rotation as R
import math
from shapely.geometry import LineString
from shapely import geometry
import random

###Generates points on the XY plain
def build_one_point_in_circle(center:tuple,theta:float,radius:float)->list:
    
    return (center[0]+radius*np.cos(np.deg2rad(theta)),center[1]+radius*np.sin(np.deg2rad(theta)),0)

#Creating the full polygon, returns a dictionary with keys (center,radius) and values the points of polygon
def build_circle_using_vectors(num_of_points:int,center:tuple,radius:float,starting_angle:float)->tuple:
    
    theta=360/num_of_points
    agg_theta=starting_angle
    polygon_points=[]
    for p in range(num_of_points):
        polygon_points.append(build_one_point_in_circle(center,agg_theta,radius))
        agg_theta+=theta
        
    
    return polygon_points

#Rotating created polygon
def rotate_polygon_vectors(polygon_points:list,theta:float)->None:
    
    rad_theta=np.deg2rad(theta)
    rot=np.array([[np.cos(rad_theta), -np.sin(rad_theta)], [np.sin(rad_theta), np.cos(rad_theta)]])
    for point in polygon_points:
        polygon_points[polygon_points.index(point)]=np.dot(rot,point)
  
#Recieves a dictionary of polygon system and returns specifications of a random vertice chosen     
def choose_random_vertice_from_polygons(polygons:dict):
    random_layer=polygons[random.randint(0,len(list(polygons.keys())))]
    random_polygon=polygons[random_layer][random.randint(0,len(list(polygons[random_layer].keys())))]
    random_polygon_list= polygons[random_layer][random_polygon]
    random_point1=random_polygon_list[random.randint(0,len(list(random_polygon_list)))]
    if random_polygon_list[random_polygon_list.index(random_point1)]==len(random_polygon_list)-1:
        random_point2=random_polygon_list[0]
    else:
        random_point2=random_polygon_list[random_polygon_list.index(random_point1)+1]
        
    return random_layer,random_polygon,(random_point1,random_point2)

#Checks for all vertices of the new polygon created completely covered by upper polygons 
def check_overlapping_with_upper_layer(polygons:dict,new_layer:int,new_polygon:tuple)->list:
    
    overlap_vertices=[]
    new_vertices=[]
    polygon_points=polygons[new_layer][new_polygon]
    
    
    #build the vertices from our new polygon to be
    for point in polygon_points[:-1]:
        new_vertices.append((point,polygon_points[polygon_points.index(point)+1]))
    
    new_vertices.append((polygon_points[-1],polygon_points[0]))
        
    upper_polygons=polygons[new_layer-1]
    for upper_center,upper_points in upper_polygons.items():
        built_polygon=geometry.polygon(upper_points,upper_points[0])
        for vertice in new_vertices:
            if built_polygon.contains(vertice[0]) and built_polygon.contains(vertice[1]):
                overlap_vertices.append(vertice)
    
    return overlap_vertices
        
#Check overlapping in the same layer as the new polygon
def check_overlapping_same_layer(same_level_polygons:dict,new_polygon_center:tuple,suggested_radius:float)->bool:
    
    for center_and_radius in list(same_level_polygons.keys()):
        if math.dist(center_and_radius[0],new_polygon_center)<(center_and_radius[1]+suggested_radius):
            return False
    return True            
    
    
    
          
def build_polygon_system(Amount_of_polygons:int):
    polygons={}
    layer=1
    #Creating the first layer of polygons, the main polygon
    upper_num_of_points,upper_center,upper_radius,upper_angle=random.randint(3,3),np.array([0,0]),random,random.random(10,10),0
    polygons[layer]=build_circle_using_vectors(upper_num_of_points,upper_center,upper_radius,upper_angle)
    
    #Starting to create more polygons that derive from first polygon
    for run in range(Amount_of_polygons-1):
        
        used_vertices=[]
        occupied_vertice=True
        
        #chooses a viable vertice to build upon
        while occupied_vertice:
            upper_layer,upper_polygon,upper_vertice=choose_random_vertice_from_polygons(polygons)
            
            
            if upper_vertice not in used_vertices:
                used_vertices.append(upper_vertice)
                occupied_vertice=True
                
        #finding the lower polygon specifications and making sure no overlapping occours with same level polygons
        lower_center=((upper_vertice[0][0]+upper_vertice[1][0])/2,(upper_vertice[0][1]+upper_vertice[1][1])/2)

        k=0
        radius_ok=False
        while not radius_ok:
            lower_radius=random.random((1-(k/10))*upper_radius,((k/10)+1)*upper_radius)
            if check_overlapping_same_layer(polygons[upper_layer-1],lower_center,lower_radius):
                radius_ok=True
            k+=0.1
        
        
        polygons[(lower_center,lower_radius)]=build_circle_using_vectors(num_of_points, center, radius, starting_angle)
        used_vertices.append(check_overlapping_with_upper_layer(polygons,upper_layer-1,))
            
        
        
        #Making sure no over-lapping occours, CRUDE! needs to add overlapping wasteful calculations on lower layers recursivly.
        if lower_radius>math.dist(upper_vertice[0],upper_vertice[1]):
            upper_polygon_points =polygons[upper_layer][upper_center]
            if upper_polygon_points.index(upper_vertice[0])==0:
                used_vertices.append(upper_polygon_points[-1])
            else:
                used_vertices.append(upper_polygon_points[upper_polygon_points.index(upper_vertice[0])-1])
                                     
            if upper_polygon_points.index(upper_vertice[1])==(len(upper_polygon_points)-1):
                used_vertices.append(upper_polygon_points[0])
            else:
                used_vertices.append(upper_polygon_points[upper_polygon_points.index(upper_vertice[1])+1])
        
               
                
        
            
        
        
          
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
    if angle<0:
        angle=360+angle
    if angle>360:
        angle=angle-360*(angle/360)
            
    if angle<90 and angle>0:
        return (center_of_circle[0]+(length_of_radius*math.cos(math.radians(angle))),center_of_circle[1]+(length_of_radius*math.sin(math.radians(angle))),0)
    elif (angle>90 and angle<180) :
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
    
    if point1[0]==point2[0]:
        if point1[1]>point2[1]:
            return -90
        else:
            return 90
    elif point1[1]==point2[1]:
        if point1[0]>point2[0]:
            return 180
        else:
            return 0
    
    y=point2[1]-point1[1]
    x=point2[0]-point1[0]
    angle=math.degrees(math.atan(y/x))
    return angle

#find closest point from a list to a point
def find_closest_point(points,point_inquired):
    closest_point=points[0]
    dist=math.dist(closest_point,point_inquired)
    for point in points[1:]:
        dist2=math.dist(point,point_inquired)
        if dist>dist2:
            closest_point=point
            dist=dist2
    return closest_point

#Creates a polygon 
def creating_polygon_on_field(num_of_points,starting_angle,center_of_shape,radius):
    
    canon_angle=360/num_of_points
    points_in_shape=[]
    agregated_angle=starting_angle
    for p in range(num_of_points):
        
        points_in_shape.append(build_circle_using_vectors(num_of_points,center_of_shape,radius,starting_angle))
        agregated_angle=agregated_angle+canon_angle
        
    return points_in_shape


def find_points_to_align(main_poly_point,sec_poly_point1,sec_poly_point2,point_in_upper_polygon):
    
    #building lines
    
    main_to_poly_point1=LineString([main_poly_point,sec_poly_point1])
    main_to_poly_point2=LineString([main_poly_point,sec_poly_point2])
    poly_point1_to_upper_poly=LineString([sec_poly_point1,point_in_upper_polygon])
    poly_point2_to_upper_poly=LineString([sec_poly_point2,point_in_upper_polygon])
    two_point_list=[]
    two_point_list.append(main_poly_point)
    
    #Check to see which point will be returned
    if not main_to_poly_point1.intersects(poly_point2_to_upper_poly) and main_to_poly_point2.intersects(poly_point1_to_upper_poly):
        two_point_list.append(sec_poly_point2)
        return two_point_list
    elif not main_to_poly_point2.intersects(poly_point1_to_upper_poly)and main_to_poly_point2.intersects(poly_point1_to_upper_poly):
        two_point_list.append(sec_poly_point1)
        return two_point_list
    else:
        if math.dist(sec_poly_point1,point_in_upper_polygon)<math.dist(sec_poly_point2,point_in_upper_polygon):
            two_point_list.append(sec_poly_point1)
            return two_point_list
        else:
            two_point_list.append(sec_poly_point2)
            return two_point_list
    
    
def find_align_angle_and_vertice_according_to_orientation(upper_center,lower_center,upper_poly_angle,main_lower_point,lower_polygon):
    
    angle_between_centers=find_angle(lower_center,upper_center)
    two_point_list=[main_lower_point]
    
    if angle_between_centers<0:
        angle_between_centers=360+angle_between_centers
    
    if angle_between_centers>=0 or angle_between_centers==360  and angle_between_centers<=90:
        two_point_list.append(lower_polygon[lower_polygon.index(main_lower_point)-1])
        lower_poly_angle=find_angle(two_point_list[0],two_point_list[1])
        return upper_poly_angle+abs(lower_poly_angle),two_point_list
    
    elif angle_between_centers>90 and angle_between_centers<=180:
        two_point_list.append(lower_polygon[lower_polygon.index(main_lower_point)+1])
        lower_poly_angle=find_angle(two_point_list[0],two_point_list[1])
        return upper_poly_angle-lower_poly_angle,two_point_list
    
    elif angle_between_centers>180 and angle_between_centers<=270:
        two_point_list.append(lower_polygon[lower_polygon.index(main_lower_point)-1])
        lower_poly_angle=find_angle(two_point_list[0],two_point_list[1])
        return upper_poly_angle+lower_poly_angle,two_point_list
    
    elif angle_between_centers>270 and angle_between_centers<360:
        two_point_list.append(lower_polygon[lower_polygon.index(main_lower_point)-1])
        lower_poly_angle=find_angle(two_point_list[0],two_point_list[1])
        return abs(lower_poly_angle)+upper_poly_angle,two_point_list
            


#Creates alot of polygons
def creating_polygon_system(first_center,first_radius,num_of_polygons):
    
    #Creating first polygon in the system
    polygons={}
    polygons[(first_center,first_radius)]=build_circle_using_vectors(random.randint(3,3),first_center,first_radius,0)
    marked_poly_lines=[]
    
    #Runs as much as needed to create polygons in the system
    
    for p in range(num_of_polygons-1):
        
        is_marked=True
        while is_marked:
            
            upper_center_and_radius=random.choice(list(polygons.keys()))
            random_poly_point=random.randint(0,len(polygons[upper_center_and_radius])-1)
            poly_point1=polygons[upper_center_and_radius][random_poly_point]
            
            if random_poly_point==len(polygons[upper_center_and_radius])-1:
                poly_point2=polygons[upper_center_and_radius][0]
            else:
                poly_point2=polygons[upper_center_and_radius][random_poly_point+1]
            two_poly_list_upper=(poly_point1,poly_point2)
            
            #Checking to see if the points chosen are above or below the horizon for later calculating
            if two_poly_list_upper not in marked_poly_lines:
                is_marked=False
        
        marked_poly_lines.append(two_poly_list_upper)
        
        #finding angles created by poly line
        
        angle_of_selected_poly_line=find_angle(two_poly_list_upper[0],two_poly_list_upper[1])
                
        
        #finding mid point and angle from center
        x_mid=(poly_point1[0]+poly_point2[0])/2
        y_mid=(poly_point1[1]+poly_point2[1])/2
        angle_center_mid=find_angle(upper_center_and_radius[0],(x_mid,y_mid,0))
        
        #creating new polygon     
        new_poly_dots=random.randint(3,4)
        lower_radius=random.uniform(upper_center_and_radius[1]/2,(3/4)*upper_center_and_radius[1])
        dist=random.uniform((4/5)*upper_center_and_radius[1],upper_center_and_radius[1])
        
        ###Using numpy's methods to create the new polygon
        lower_center=build_one_point_in_circle((x_mid,y_mid),angle_center_mid,dist)        
        new_polygon_placeholder=build_circle_using_vectors(new_poly_dots,lower_center,lower_radius,0)
        
        #finds closest point in the lower polygon to the second point from upper polygon
        lower_center_poly_point=find_closest_point(new_polygon_placeholder,poly_point2)
                
        overall_angle,two_poly_list_lower=find_align_angle_and_vertice_according_to_orientation(upper_center_and_radius[0],lower_center,angle_of_selected_poly_line,lower_center_poly_point,new_polygon_placeholder)
        polygons[(lower_center,lower_radius)]=rotate_polygon_vectors(new_polygon_placeholder,overall_angle)
        polygons[(tuple(lower_center),lower_radius)]="d"
        marked_poly_lines.append(two_poly_list_lower)
        if None in polygons[(tuple(lower_center),lower_radius)]:
            print('halt')
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






################## Linear Algebra


