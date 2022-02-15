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
        
class polygon:
    
    def __init__(self,center,radius,num_of_vertices) -> None:
            
            self.center=center
            self.radius=radius
            self.num_of_edges=num_of_vertices
            self.vertices=[]
            self.starting_angle=0
            self.non_relevant_verticies=[]
            self.edges=pd.DataFrame(columns=['point_1','point_2','is_parent','t_initial','t_final'])
            
    def generate_vertices(self):
        edge={}
        aggregated_angle=self.starting_angle
        #creating first point
        
        initial_point=np.array([self.center[0]+np.cos(aggregated_angle)*self.radius,self.center[1]+np.sin(aggregated_angle)*self.radius],dtype=np.float64)
        self.vertices.append(initial_point)
        for e in range(self.num_of_edges-1):
           
           aggregated_angle=aggregated_angle+(2*np.pi)/self.num_of_edges
           next_point=np.array([self.center[0]+np.cos(aggregated_angle)*self.radius,self.center[1]+np.sin(aggregated_angle)*self.radius],dtype=np.float64)
           self.vertices.append(next_point)
           edge={"point_1":initial_point,"point_2":next_point,"is_parent":False,"t_initial":0.0,"t_final":1.0}
           self.edges=self.edges.append(edge,ignore_index=True) 
           initial_point=next_point
        
        self.edges=self.edges.append({"point_1":initial_point,"point_2":self.edges.loc[0,'point_1'],"is_parent":False,"t_initial":0.0,"t_final":1.0},ignore_index=True)
    
            
class layer:
    
    def __init__(self,num_of_colors,light_sfx='light_object') -> None:
        
        self.polygons=[]
        self.color_palette=[]
        self.non_relevant_polygons=[]
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
    
    def __init__(self,number_of_polygons) -> None:
        
        self.number_of_polygons=number_of_polygons
        self.layers=[layer().polygons.append(polygon(np.array([0,0],dtype=np.float64),10,3).generate_polygon())]
        self.non_relevant_layers=[]
        self.triangles=pd.DataFrame(columns=["layer","center","point_1","point_2","is_parent","t_initial","t_final"])
    
        
            
            
poly=polygon(np.array([0,0]),10,3)

poly.generate_vertices()

print(poly.edges)    
print("done")
            
            
  
        
        