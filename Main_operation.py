import matplotlib.pyplot as plt
import json
import numpy as np
import Magneticfieldcalculator



def run_multi_universe():
    
    magnetic_outcomes=Magneticfieldcalculator.calculate_magnetic_field()
    
    with open('./json/cmaps.json') as f:
       cmaps=list(json.load(f))
    
    for category in cmaps[1:]:
        for gradienttype in category[1]:
            x,y=2,2
            Magneticfieldcalculator.draw_and_color_magnetic_lines(category[0],gradienttype,x,y,magnetic_outcomes)
            plt.clf()


run_multi_universe()