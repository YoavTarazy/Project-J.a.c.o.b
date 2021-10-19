import json
import numpy as np
import math_zone
import math


def check_find_points_in_circle(num_of_points,center_of_circle, length_of_radius):
    return math_zone.find_points_in_circle(num_of_points,center_of_circle, length_of_radius)

def check_straight_line_function():
    
    print(math_zone.build_straight_line_function((1401,133),(1996,133)))

def check_dist(point,two_poly_list):
    dist=math_zone.find_intersection_point_and_dist(point,two_poly_list)
    print(dist)

def check_polygon_centers_dic(centers,polypoints):
    
    dic=math_zone.find_polygons_by_points(centers,polypoints)
    print(dic)
    return dic

def test_infinity():
    return 1/math.inf

def check_intersection_point_linear_algebra():
    print(math_zone.find_intersection_point(((133,1401),(133,1996)),((180,1500),(100,1401))))
 

def check_calculate_minimal_distance_from_polygon_points(centers,poly_points,point):
    return math_zone.calculate_minimal_distance_from_polygon_points(point,math_zone.find_polygons_by_points(centers,poly_points),poly_points)

def check_polygon_creation(first_center,first_radius,num_of_polygons):
    
    print(math_zone.creating_polygon_system(first_center,first_radius,num_of_polygons))


#center= [(1368,805)]
#poly_points=[(1244,607),(1244,1004),(1368,408),(1368,1202),(1491,607),(1491,1004)]#
#for p in poly_points:
#    print(check_valid_intersection(center[0],p,poly_points[4],poly_points[2]))


#check_polygon_centers_dic(center,poly_points)

#point=(1400,608)
#two_poly_list,rev_center=check_calculate_minimal_distance_from_polygon_points(center,poly_points,point)
#print(two_poly_list)
#check_dist(point,two_poly_list)

#print(check_find_points_in_circle(5,(0,1),1))

check_polygon_creation((0,0,0),10,4)

