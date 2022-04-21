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
    
    def __init__(self,layer_num,num_of_colors,light_sfx='light_object') -> None:
        
        self.layer_num=layer_num
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
        
        self.layers={}
        self.edges=pd.DataFrame(columns=["layer","cx","cy",'radius',"p1x","p1y","p2x","p2y",'rel'])
        
    def add_polygon_to_df(self,layer_number:int,polygon:polygon):
        
        x,y=polygon.vertices[0],polygon.vertices[1]
        new_df=pd.DataFrame(columns=['p1x'])
        new_df['p1x']=x
        new_df['p1y']=y
        new_df['p2x']=[x[-1]]+x[0:-1]
        new_df['p2y']=[y[-1]]+y[0:-1]
        new_df['cx'],new_df['cy']=polygon.center
        new_df['radius']=polygon.radius
        new_df['layer']=layer_number
        new_df['rel']=True
        
        self.edges=pd.concat([self.edges,new_df])
    
    def manifest_origin_polys(self,num_of_polys):
        
        new_layer=layer(0,3,0)
        new_polygon=polygon([0,0],10,3,0)
        self.layers[new_layer]=[new_polygon]
        self.add_polygon_to_df(0,new_polygon)
                
    def generate_lower_layer(self):
        
        new_layer=layer(self.edges['layer'].max()+1,6)
        
        self.layers[new_layer]=[]
        
        return new_layer
    
    def generate_lower_polygon(self,edge:pd,lowest:bool)->bool:
        
        
        
        if lowest:
            
            new_radius=random.uniform(0.5*edge.radius.values[0],0.8*edge.radius.values[0])
            lowest_layer=self.generate_lower_layer()
            rel_edges=self.edges.loc[(self.edges.layer+1==lowest_layer.layer_num) & 
                                     (self.edges['cx'] != 0) & (self.edges['cy'] != 0)]
            
            
            if rel_edges.empty:
               new_center=mz.pinpoint_polygon(0.5,edge)
            else:    
                constr=mz.create_constraint_dic(edge,rel_edges)
                result=mz.t_min_max_lowest(constr)
                
                if result.success:
                    new_center=mz.pinpoint_polygon(result.x[0],edge)
                else:
                    return False
                
            new_poly=polygon(new_center,new_radius,random.randint(3,8),random.uniform(0,2*np.pi))
            self.add_polygon_to_df(lowest_layer.layer_num,new_poly)
            self.layers[lowest_layer]=[new_poly]
        
        else:
            
            for l in self.layers:
                if l.layer_num==edge.layer.values[0]:
                    lower_layer=l
                    break
                
            rel_cr=self.edges.loc[(self.edges.layer+1==lower_layer.layer_num) & 
                                     (self.edges['cx'] != 0) & (self.edges['cy'] != 0)]
            rel_constr=self.edges.loc[(self.edges.layer==lower_layer.layer_num)]
            constr=mz.create_constraint_dic(edge,rel_constr)
            result=mz.calculate_desired_radius(edge,rel_cr,constr)
            
            if result.success!=True:
                    return False                    
            
            new_radius=-result.fun
            new_center=mz.pinpoint_polygon(result.x[0],edge)
            new_poly=polygon(new_center,new_radius,random.randint(3,8),random.uniform(0,2*np.pi))
            self.add_polygon_to_df(lower_layer.layer_num,new_poly)
            self.layers[lower_layer]=[new_poly]
                
            
                
        return True
            
    def manifest_polygon_system(self,num_of_polygons):
        
        self.manifest_origin_polys(1)
        i=0
        while i in range(num_of_polygons):
            
            chosen_edge=self.edges[self.edges['rel']!=False].sample()
            self.edges.loc[self.edges.index==chosen_edge.index[0],'rel']=False
            is_lowest=chosen_edge['layer'].values[0]== self.edges['layer'].max() 
            success=self.generate_lower_polygon(chosen_edge,is_lowest)
            
            if success:
                i=i+1
                
        print(self.edges)
            
        

        
       

poly_sys=polygon_system()
poly_sys.manifest_polygon_system(10)      
                

            
            
  
        
        