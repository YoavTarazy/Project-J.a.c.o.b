import numpy as np
import math
import random
from numba import jit 
import matplotlib
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from matplotlib import path

class point:
    
    def __init__(self,x:float,y:float) -> None:
        self.x=x
        self.y=y
        self.z=0
    
    def _str_(self) -> str:
        
        return "x: {x} y: {y}".format(x=self.x,y=self.y)   
    
    def return_coordinate(self):
        return (self.x,self.y)
    
    

class polygon:
    
    def __init__(self,points_amount:int,center_coordinate:point,radius:float,angle:float,layer:int) -> None:
        
        self.points_amount=points_amount
        self.center=center_coordinate
        self.radius=radius
        self.angle=angle
        self.layer=layer
        
        #holds all points of polygon
        self.points=[]
        
        #vertices created from points for easier testing
        self.vertices=[]
        
        #which vertices are not to be treated as worthy polygon sources
        self.covered_vertices=[]
        
        #a coarse filtering for points outside of it.
        self.poly_rec=[]
    
    def __str__(self) -> str:
        
        p_list_string=""
        for p in self.points:
            p_list_string+=str(p)
            
        return "center: {center}, points: {pointlist}\n".format(self.center.return_coordinate(),pointlist=p_list_string)    
    
    def pin_point(self,agg_angle)->point:
        
        return point(self.center.x+self.radius*np.cos(agg_angle),self.center.y+self.radius*np.sin(agg_angle))
    
    
    #Creates the coarse rectangle for first filter of points
    def find_rec(self):
        
        lstx,lsty=[],[]
        for p in self.points:
            lstx.append(p.x)
            lsty.append(p.y)
        
        self.poly_rec.append(point(min(lstx),min(lsty)))
        self.poly_rec.append(point(min(lstx),max(lsty)))
        self.poly_rec.append(point(max(lstx),max(lsty)))
        self.poly_rec.append(point(max(lstx),min(lsty)))
            
            
    
    #Manifesting points,vertices,rectangle and rules out covered vertices by upper polygons        
    def manifest_polygon(self):
            
        added_angle=2*np.pi/self.points_amount
        agg_angle=self.angle
        for p in range(self.points_amount):
            self.points.append(self.pin_point(agg_angle))
            agg_angle+=added_angle
            
        self.points.append(self.points[0])
        self.vertices=list(zip(self.points[0:-1],self.points[1:]))
        self.find_rec()


    #Returns a random vertice not including the covered ones!
    def view_random_vertice(self):
        
        clean_vertice_list = [v for v in self.vertices if v not in self.covered_vertices]
        return random.choice(clean_vertice_list)


    #This function checks for covered verices to not be used in further creation of polygons.
    def find_covered_vertices(self,other):
        
        p_list=[]
        for p in other.points:
            p_list.append(p.return_coordinate())
        p=path.Path(p_list)
        
        for v in self.vertices:
            
            p1,p2=v[0].return_coordinate(),v[1].return_coordinate()
            
            if p.contains_point(p1.return_coordinate()) and p.contains_point(p2.return_coordinate()):
                self.covered_vertices.append(v)
                       
class layer:
    
    def __init__(self,polygons:list,layer_num:int)->None:
        
        self.color_scheme=[]
        self.polygons=polygons
        self.layer_num=layer_num
        
    def __str__(self) -> str:
        p_list_string=""
        for p in self.polygons:
            p_list_string+=str(p)
            
        return "layer #{layernum}, polygon points:\n".format(layernum=self.layer_num)
    
    #adds a polygon to the polygon list of the layer while associating it with current layer and returning it for further manipulation    
    def add_polygon(self,center:point,radius:float)->None:
        
        new_polygon=polygon(random.randint(3,8),center,radius,random.random()*np.pi,self.layer_num)
        new_polygon.manifest_polygon()
        self.polygons.append(new_polygon)
        
        return new_polygon
    
    #chooses a polygon from layer
    def view_polygon(self):
        return random.choice(self.polygons)
         
    def create_color_scheme(self,gradient_amount:int)->None:
        
        color_palette=[]
        comp_color_palette=[]
        
        for c in range(gradient_amount):
            color=[random.uniform(130,255),random.uniform(130,255),random.uniform(130,255)]
            color_palette.append(color)
            comp_color_palette.append([255-color[0],255-color[1],255-color[2]])
            
        self.color_scheme=color_palette+comp_color_palette

    #Recives a new center candidate and returns the optimal radius in case there are more polygons in the same layer!
    def return_good_radius(self,new_center:point)->float:
        
        is_valid=True
        new_radius=0.0
        
        while is_valid:
            
            for p in self.polygons:
                if new_radius>math.dist(new_center.return_coordinate(),p.center.return_coordinate())-p.radius:
                    is_valid=False
            if is_valid:
                new_radius+=0.5
                
        return new_radius
                
            
        
class polygon_system:
    
    def __init__(self,manual:bool) -> None:
        
        self.Manual=manual
        
        #Building first layer and center
        self.layers=[]
        
        self.marked_vertices=[]
        self.layers.append(layer([polygon(random.randint(3,6),point(0,0),random.uniform(15,20),0,0)],0))
        self.layers[0].polygons[0].manifest_polygon()
    
    def __str__(self) -> str:
                
        l_list_string=""
        for l in self.layers:
            l_list_string+=str(l)
            
        return "The layers:\n{layerlist}".format(layerlist=l_list_string) 
    
    #Returns the center from of a vertice
    def find_center(self,vertice)->point:
        return point((vertice[0].x+vertice[1].x)/2,(vertice[0].y+vertice[1].y)/2)
    
    #Creates a new layer
    def new_layer(self,number_of_colors_in_layer:int)->None:
        self.layers.append(layer([],len(self.layers)))
        self.layers[-1].create_color_scheme(number_of_colors_in_layer)
        
    
    
    #The creation of the whole polygon system    
    def manifest_polygon_system(self,number_of_polygons:int,range_of_size:int)->None:
        
        for p in range(number_of_polygons):
            
            upper_polygon=random.choice(self.layers).view_polygon()
            upper_vertice=upper_polygon.view_random_vertice()
                
                
            if upper_polygon in self.layers[-1].polygons:
                self.new_layer((3))
                lower_polygon=self.layers[-1].add_polygon(self.find_center(upper_vertice),random.uniform(upper_polygon.radius/2,upper_polygon.radius*3/4))
            else:
                
                #a function that makes sure the radius of the polygon will not overlap with any existing polygons in the same layer.
                lower_center=self.find_center(upper_vertice)
                approved_radius=self.layers[upper_polygon.layer+1].return_good_radius(lower_center)
                lower_polygon=self.layers[upper_polygon.layer+1].add_polygon(lower_center,approved_radius)
                lower_polygon.find_covered_vertices(upper_polygon)
                
polysys=polygon_system(False)
polysys.manifest_polygon_system(1,1)
print(polysys)


                
            
            
            
        
        
        