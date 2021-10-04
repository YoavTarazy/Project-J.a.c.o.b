import json
import numpy as np
import math_zone

def check_dist(point):
    
    with open('./json/distances.json') as f:
        distances=np.array(json.load(f))
    print(distances[point[1]][point[0]])

def check_polygon_centers_dic(centers,polypoints):
    
    dic=math_zone.find_polygons_by_points(centers,polypoints)
    print(dic)
    return dic

    
dic=check_polygon_centers_dic([(3386,750)],[(3386,503),(2989,750),(3783,750),(3386,997)])
