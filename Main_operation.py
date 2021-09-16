import matplotlib.pyplot as plt
import json
import numpy as np
import Magneticfieldcalculator
import random

    

def run_multi_universe():
    
    magnetic_outcomes=Magneticfieldcalculator.calculate_magnetic_field()
    
    with open('./json/cmaps.json') as f:
       cmaps=list(json.load(f))
    
    for category in cmaps:
        for gradienttype in category[1]:
            for x in range(2,8):
                for y in range(2,8):
                    Magneticfieldcalculator.draw_and_color_magnetic_lines(category[0],gradienttype,x,y,magnetic_outcomes)
                    plt.clf()


def Randomized_Magnetic_field():
    counter=10
    amount_of_magnets=random.randint(2,16)
    list_of_currents=[]
    list_of_locations=[]
    
    with open('./json/cmaps.json') as f:
        cmaps=list(json.load(f))    
    for c in range(counter):
        for c in range(amount_of_magnets):
            
            if random.choice([True, False]):
                rand_current=-1*random.random()
            else:
                rand_current=random.random()
        
            list_of_currents.append(rand_current)
            list_of_locations.append((random.randint(-40,40),random.randint(-40,40)))
        category=random.randint(0,4)
        gradienttype=random.randint(0,len(cmaps[category][1])-1)
        Magneticfieldcalculator.calculate_randomized_magnetic_field(cmaps[category][0],cmaps[category][1][gradienttype],2,2,Magneticfieldcalculator.random_magnetic_field(amount_of_magnets,list_of_currents,list_of_locations),amount_of_magnets)
   

def Jacob_Run():
    xs,ys,density,line_width,category,gradient=50,50,10,2,'Perceptually Uniform Sequential','viridis'
    dic_plt={'size of space':(xs,ys),'density of stream plot':density,'thickness of lines in streamplot':line_width,'color category': category,'gradient': gradient}
    amountofmagnets,list_of_currents,list_of_locations=4,(10,-10,10,-10),((40,40),(-40,-40),(40,-40),(-40,40))
    dic_magnetic={'amount of magnets':amountofmagnets,'currents':list_of_currents,'locations':list_of_locations}
    
    
Randomized_Magnetic_field()