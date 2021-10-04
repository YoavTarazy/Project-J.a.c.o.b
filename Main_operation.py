import matplotlib.pyplot as plt
import json
import numpy as np
import Magneticfieldcalculator
import random
import os
import jsonrunner
from PIL import Image
import Jacobprocessing
import math_zone

def Randomized_Magnetic_field(Counter,current):
    
    
    with open('./json/cmaps.json') as f:
        cmaps=list(json.load(f))  
    
    #Randomize gradient type and
    for c in range(Counter):
        category=random.randint(0,4)
        gradienttype=random.randint(0,len(cmaps[category][1])-1)
        #Creating The Module + Blueprint mode
        b_img_path,n_img_path=Magneticfieldcalculator.calculate_randomized_magnetic_field(current*((-1)**c),cmaps[category][0],cmaps[category][1][gradienttype],2,2,Magneticfieldcalculator.module_magnetic_polygons(10,10,1,3,2000,current))
        plt.clf()
        print('finished creating the modules')
        #Getting Distances from each white point to the closest polygon using blueprint mode
        
        ##Creating a numpy array of the blackend pic
        pix=np.array(Image.open(b_img_path+'.png'))
        print('finished creating the numpy array for blueprint pic')
        
        ##Understanding where red lines are
        dist,max_dist=jsonrunner.find_reddots_Bluedots_and_distances(b_img_path)
        
        ##Converting numpy array to color pic
        pix=np.array(Image.open(n_img_path+'.png'))
        print('finished creating the colored pic numpy array')
        
        #Coloring
        print('finished creating the arrays, pulling colors and calculating distances')
        
        Jacobprocessing.color_image(pix,dist,3,8,max_dist,n_img_path)
        print('done coloring!')
    
    
Randomized_Magnetic_field(1,0.1)