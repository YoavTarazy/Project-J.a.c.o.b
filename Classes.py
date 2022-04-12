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
    
    def __init__(self,center,radius,num_of_vertices) -> None:
            
            self.center=center
            self.radius=radius
            self.num_of_edges=num_of_vertices
            self.vertices=[]
            self.starting_angle=0
            self.non_relevant_verticies=[]
            self.edges=pd.DataFrame(columns=['cx','cy','p1x','p1y','p2x','p2y','is_parent','t_initial','t_final'])
            
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
           edge={"cx":self.center[0],"cy":self.center[1],"p1x":initial_point[0],"p1y":initial_point[1],"p2x":next_point[0],"p2y":next_point[1],"is_parent":False,"t_initial":0.0,"t_final":1.0}
           self.edges=self.edges.append(edge,ignore_index=True) 
           initial_point=next_point
        
        fx,fy=self.edges.loc[0,['p1x','p1y']]
        self.edges=self.edges.append({"cx":self.center[0],"cy":self.center[1],"p1x":initial_point[0],"p1y":initial_point[1],"p2x":fx,"p2y":fy,"is_parent":False,"t_initial":0.0,"t_final":1.0},ignore_index=True)
    
            
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
    
    def __init__(self,number_of_polygons) -> None:
        
        self.number_of_polygons=number_of_polygons
        self.layers=[]
        self.triangles=pd.DataFrame(columns=["layer","cx","cy","p1x","p1y","p2x","p2y","is_parent","t_initial","t_final"])
        
    def add_polygon_to_df(self,layer_number:int,polygon:polygon):
        
        new_df=polygon.edges
        new_df['layer']=layer_number
        self.triangles=pd.concat([self.triangles,new_df])
    
    def check_for_sheltered_edges(self,polygon:polygon):
        print(self.triangles)
        print(polygon.edges)
        true1=mz.check_point_in_triangles(polygon.edges['p1x'].to_numpy(dtype=np.float64),polygon.edges['p1y'].to_numpy(dtype=np.float64),self.triangles['cx'].to_numpy(dtype=np.float64),self.triangles['cy'].to_numpy(dtype=np.float64),self.triangles['p1x'].to_numpy(dtype=np.float64),self.triangles['p1y'].to_numpy(dtype=np.float64),self.triangles['p2x'].to_numpy(dtype=np.float64),self.triangles['p2y'].to_numpy(dtype=np.float64))
        true2=mz.check_point_in_triangles(polygon.edges['p2x'].to_numpy(dtype=np.float64),polygon.edges['p2y'].to_numpy(dtype=np.float64),self.triangles['cx'].to_numpy(dtype=np.float64),self.triangles['cy'].to_numpy(dtype=np.float64),self.triangles['p1x'].to_numpy(dtype=np.float64),self.triangles['p1y'].to_numpy(dtype=np.float64),self.triangles['p2x'].to_numpy(dtype=np.float64),self.triangles['p2y'].to_numpy(dtype=np.float64))
        print(true1)
        print(true2)

        
       
            
                
            
poly1=polygon(np.array([2,0]),8.4,3)
poly1.generate_vertices()
poly2=polygon(np.array([0,0]),10,3)   
poly2.generate_vertices()        
polysys = polygon_system(5)
polysys.add_polygon_to_df(0,poly2)
print(polysys.triangles)
polysys.check_for_sheltered_edges(poly1)
print('done')
            
            
  
        
        