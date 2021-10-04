import json
import numpy as np

def check_dist(point):
    
    with open('./json/distances.json') as f:
        distances=np.array(json.load(f))
    print(distances[point[1]][point[0]])
    
check_dist((380,2989))
        
    