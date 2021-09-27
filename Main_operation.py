import matplotlib.pyplot as plt
import json
import numpy as np
import Magneticfieldcalculator
import random
          

def Randomized_Magnetic_field(Counter,current):
    
    with open('./json/cmaps.json') as f:
        cmaps=list(json.load(f))  
    
    #Randomize gradient type and
    for c in range(Counter):
        category=random.randint(0,4)
        gradienttype=random.randint(0,len(cmaps[category][1])-1)
        Magneticfieldcalculator.calculate_randomized_magnetic_field(current,cmaps[category][0],cmaps[category][1][gradienttype],2,2,Magneticfieldcalculator.module_magnetic_polygons(50,50,5,8,2000))
        plt.clf()

Randomized_Magnetic_field(10)