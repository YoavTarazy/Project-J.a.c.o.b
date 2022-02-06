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
import math_zone as mz
import sympy as smp
from sympy import *
from sympy import symbols
import time

class vertice: #Represents each verrtice for each polygon created
    
    def __init__(self, two_points) -> None:
        
        self.points=two_points
        self.birthing_interval=np.array([0.0,1.0])
        
            
            
    def __repr__(self) -> str:
        
        return "Vertice: {points} , Is relevant: {parent}".format(points=self.points,parent=self.is_relevant)
 

class polygon:
    
    def __init__(self,center,radius,num_of_edges) -> None:
            
            self.center=center
            self.radius=radius
            self.num_of_edges=num_of_edges
            self.vertices=[]
            self.square_influence=[]
            self.starting_angle=0
            self.non_relevant_verticies=[]
            
    def generate_vertices(self):
       
        aggregated_angle=self.starting_angle
        #creating first point
        
        initial_point=np.array([self.center[0]+np.cos(aggregated_angle)*self.radius,self.center[1]+np.sin(aggregated_angle)*self.radius])
        
        for e in range(self.num_of_edges-1):
           
           aggregated_angle=aggregated_angle+(2*np.pi)/self.num_of_edges
           next_point=np.array([self.center[0]+np.cos(aggregated_angle)*self.radius,self.center[1]+np.sin(aggregated_angle)*self.radius])
           self.vertices.append(vertice(np.array([initial_point,next_point])))
           initial_point=next_point

        self.vertices.append(vertice(np.array([initial_point,self.vertices[0].points[0]])))
    
    def generate_square_of_influence(self):
     
     first_v=self.vertices[0]
     minx,miny,maxx,maxy=first_v.points[0][0],first_v.points[0][1],first_v.points[0][0],first_v.points[0][1]
     for v in self.vertices:
         point=v.points[1]
         
         if point[0]<minx:
             minx=point[0]
             
         if point[0]>maxx:
             maxx=point[0]
             
         if point[1]<miny:
             miny=point[1]
             
         if point[1]>maxy:
             maxy=point[1]
     
     self.square_influence=[np.array([[minx,miny],[minx,maxy],[maxx,miny],[maxx,maxy]])]   
            
    def generate_polygon(self):
        
        self.generate_vertices()
        self.generate_square_of_influence()
                    
    def choose_vertice(self,vertice):
        
        chosen_vertice= {v in self.vertices and not in self.non_relevant_verticies}
        self.non_relevant_verticies.append(vertice)
                
class layer:
    
    def __init__(self) -> None:
        
        self.polygons=[]
        self.color_palette=[]
        self.non_relevant_polygons=[]
    
    def exclude_polygon(self,polygon):
        
        if len(polygon.non_relevant_vertices)==len(polygon.vertices):
            
            self.non_relevant_polygons.append(polygon)
        
    def choose_polygon(self):
        
        return {for poly in self.polygons and not in self.non_relevant_polygons}
        
        
    

class polygon_system:
    
    def __init__(self,number_of_polygons) -> None:
        
        self.number_of_polygons=number_of_polygons
        self.layers=[layer().polygons.append(polygon(np.array([0,0]),10,3).generate_polygon())]
        self.non_relevant_layers=[]
    
        
    
    def generate_system(self):
        
        
        for p in range(number_of_polygons-1):
            
            chosen_layer=random.randint(0,len(self.layers))
            
            
            
            
        
        