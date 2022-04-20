import numpy as np
import math
import random
import matplotlib
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from matplotlib import path
from numpy.core.fromnumeric import shape
from numpy.lib.function_base import _unwrap_dispatcher
from sympy.polys.domains import domain
import sympy as smp
from sympy import *
from sympy import symbols
import time
import pandas as pd
import math_zone as mz
        
class polygon:
    
    def __init__(self,center,radius,num_of_vertices,angle) -> None:
            
            self.center=center
            self.radius=radius
            self.num_of_vertices=num_of_vertices
            self.angle=angle
            self.vertices=mz.manifest_polygon_from_circle(self.center,self.radius,self.num_of_vertices,self.angle)
            
            
class layer:
    
    def __init__(self,num_of_colors,light_sfx='light_object') -> None:
        
        self.polygons=[]
        self.color_palette=[]
        self.num_of_colors=num_of_colors
        self.light_sfx=light_sfx
        self.color_scheme=[]
    
    def generate_color_scheme(self,gradient_amount):
        
        color_palette=[]
        comp_color_palette=[]
        
        for c in range(gradient_amount):
            color=[random.uniform(130,255),random.uniform(130,255),random.uniform(130,255)]
            color_palette.append(color)
            comp_color_palette.append([255-color[0],255-color[1],255-color[2]])
            
        self.color_scheme=color_palette+comp_color_palette
    

class polygon_system:
    
    def __init__(self) -> None:
        
        self.layers=[]
        self.edges=pd.DataFrame(columns=["layer","cx","cy",'radius',"p1x","p1y","p2x","p2y",'rel'])
        
    def add_polygon_to_df(self,layer_number:int,polygon:polygon):
        
        new_df=pd.DataFrame(columns=['p1x'])
        new_df['p1x']=polygon.vertices
        new_df['p1y']=polygon.vertices[-1]+polygon.vertices[1:-1]
        new_df['cx'],new_df['cy']=polygon.center
        new_df['radius']=polygon.radius
        new_df['layer']=layer_number
        
        self.edges=pd.concat([self.edges,new_df])
    
    
    def manifest_polygon_system(self,num_of_polygons)

        
       
            
                
            
poly1=polygon(np.array([2,0]),8.4,3)
poly1.generate_vertices()
poly2=polygon(np.array([0,0]),10,3)   
poly2.generate_vertices()        
polysys = polygon_system(5)
polysys.add_polygon_to_df(0,poly2)
print(polysys.triangles)
polysys.check_for_sheltered_edges(poly1)
print('done')
            
            
  
        
        