import numpy as np
import math
import random
from numba import jit 
import matplotlib
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from matplotlib import path
from numpy.core.fromnumeric import shape
from numpy.lib.function_base import _unwrap_dispatcher
import math_zone as mz


class point:

    def __init__(self,coords:np.array) -> None:
        self.point = coords
        self.x=coords[0]
        self.y=coords[1]
    
    def __repr__(self) -> str:
        
        return "{xy}\n".format(xy=[self.x,self.y]) 
 
class edge:
   
   def __init__(self,a:point,b:point) -> None:
       
       self.a=a
       self.b=b

class polygon:
    
    def __init__(self,points_amount:int,center_coordsinate:point,radius:float,angle:float) -> None:
        
        self.points_amount=points_amount
        self.center=center_coordsinate
        self.radius=radius
        self.angle=angle
        
        self.points=[]
        self.edges=[]
        
        self.triangles=np.array([])
        self.covered_edges=[]
        
        
        self.rec_edges=[]
        self.full_rec_points=np.array([])
    
    def __repr__(self) -> str:
        
        return "polygon center: {center},polygon Radius: {radius}\npolygon points:\n{points}".format(center=self.center,radius=self.radius,points=self.points)
    
    
    def pin_point(self,agg_angle)->point:
        
        return point(self.center.x+self.radius*np.cos(agg_angle),self.center.y+self.radius*np.sin(agg_angle))
      
    def manifest_polygon_triangles(self):
            
        triangles=[]
        for e in self.edges:
            pv1,pv2=e[0].coords,e[1].coords
            pc=self.center.coords
            triangles.append(np.array([[pc,pv1],[pv1,pv2],[pv2,pv1]]))
        self.triangles=np.asarray(triangles)
        
    def manifest_polygon(self):
            
        added_angle=2*np.pi/self.points_amount
        agg_angle=self.angle
        for p in range(self.points_amount):
            self.points.append(self.pin_point(agg_angle))
            agg_angle+=added_angle
        self.points.append(self.points[0])    
        self.edges=list(zip(self.points[0:-1],self.points[1:]))
        self.manifest_polygon_triangles()

    #After Numpy
    
    def manifest_outer_rectangle(self):
        x,y=[],[]
        for p in self.points:
            x.append(p.x)
            y.append(p.y)
        
        minx,miny=min(x),min(y)
        maxx,maxy=max(x),max(y)
        self.rec_edges=mz.numpy_polygon_rectangle(minx,miny,maxx,maxy)
  
    def classify_rec_points(self):
        
        points_inside=mz.check_if_all_points_inside_triangles(self.triangles,self.rec_edges)
        print(points_inside)
                  
    
   #Functionality
   
    def update_covered_edges(self,edge):
        
        self.covered_edges.append(edge)
        if len(self.covered_edges)==self.edges:
            self.covered=True
   
    def view_random_edge(self):
        
        clean_edges_list = [v for v in self.edges if v not in self.covered_edges]
        chosen_edge=random.choice(clean_edges_list)
        self.update_covered_edges(chosen_edge)
        
        return chosen_edge

class layer:
    
    def __init__(self,polygons:list)->None:
        
        self.color_scheme=[]
        self.polygons=polygons
        self.covered_polygons=[]
    
        
    
    def __repr__(self) -> str:
        
        return   "layer #{layernum}, polygons:\n{polypoints}\n".format(layernum=self.layer_num,polypoints=self.polygons)
    
       
    def add_polygon(self,center:point,radius:float)->None:
        
        new_polygon=polygon(random.randint(3,3),center,radius,random.random()*np.pi,self.layer_num)
        new_polygon.manifest_polygon()
        self.polygons.append(new_polygon)
        
        return new_polygon
          
        
    def create_color_scheme(self,gradient_amount:int)->None:
        
        color_palette=[]
        comp_color_palette=[]
        
        for c in range(gradient_amount):
            color=[random.uniform(130,255),random.uniform(130,255),random.uniform(130,255)]
            color_palette.append(color)
            comp_color_palette.append([255-color[0],255-color[1],255-color[2]])
            
        self.color_scheme=color_palette+comp_color_palette
                
class polygon_system:
    
    def __init__(self,layers:list) -> None:
        
        self.layers=[]
        self.layers.append(layer([polygon(random.randint(3,3),point(np.array([0,0])),10,0,0)]))
        self.layers[0].polygons[0].manifest_polygon()
        
        self.covered_layers=[]
    
    def __repr__(self) -> str:
                
        return "The layers:\n{layerlist}".format(layerlist=self.layers) 
    
    def new_layer(self,number_of_colors_in_layer:int)->None:
        
        self.layers.append(layer([]))
        self.layers[-1].create_color_scheme(number_of_colors_in_layer)

    def manifest_system_blueprint(self,num_of_polygons:int):
        
        for new_p in range(num_of_polygons):
            
            rl=random.Random([l for l in self.layers if l not in self.covered_layers])
            rp=random.Random([p for p in rl.polygons if p not in rl.covered_polygons])
            re=random.Random([e for e in rp.edges if e not in rp.covered_edges])
            
            if self.layers.index(rl)==len(self.layers)-1:
                
    