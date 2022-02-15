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
    
    def check_point_inside_triangles(self,point:list):
        
        px,py=point[0],point[1]
        tr=self.triangles
        x3,y3,x2,y2,x1,y1=tr['cx'],tr['cy'],tr['p1x'],tr['p1y'],tr['p2x'],tr['p2y']
        covering_triangles=self.triangles[((x2-x1)*(py-y1)-(y2-y1)*(px-x1)<0) & ((x3-x2)*(py-y2)-(y3-y2)*(px-x2)<0) & ((x1-x3)*(py-y3)-(y1-y3)*(px-x3)<0)]
        print(covering_triangles)
    
    
    #updates the possible creation interval according to sheltering polygons
    def update_parameterization_sheltering_polygons(self,polygon:polygon):
        
        pass
    
    #updates the possible creation from an edge according to neighboring polygons
    def update_parameterization_neighboring_polygons(self,polygon:polygon):
        pass
    
            
            
            
                
            
            
polysys = polygon_system(5)
polysys.generate_polygon_system()
print(polysys.triangles)

print('done')
            
            
  
        
        