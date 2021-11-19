import numpy as np
import math
import random
from numba import jit 
import matplotlib
import matplotlib.patches as patches
import matplotlib.pyplot as plt
from matplotlib import path
from numpy.lib.function_base import _unwrap_dispatcher

class point:
    
    def __init__(self,x:float,y:float) -> None:
        self.x=x
        self.y=y
    
    def __repr__(self) -> str:
        
        return "{xy}\n".format(xy=[self.x,self.y]) 
    def return_coordinates(self):
        return [self.x,self.y]
 

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
        self.rec_vertices=[]
        self.full_rec_points=np.array([])
    
    def __repr__(self) -> str:
        
        return "Polygon center: {center},Polygon Radius: {radius}\nPolygon points:\n{points}".format(center=self.center,radius=self.radius,points=self.points)
    
    #pinpoints a new point around the radius of the polygon
    def pin_point(self,agg_angle)->point:
        
        return point(self.center.x+self.radius*np.cos(agg_angle),self.center.y+self.radius*np.sin(agg_angle))
    
    #Creates the coarse rectangle for first filter of points
    def find_rec(self):
        x,y=[],[]
        for p in self.points:
            x.append(p.x)
            y.append(p.y)
        
        minx,miny=min(x),min(y)
        maxx,maxy=max(x),max(y)
        self.rec_vertices.append(point(minx,miny))
        self.rec_vertices.append(point(minx,maxy))
        self.rec_vertices.append(point(maxx,miny))
        self.rec_vertices.append(point(maxx,maxy))
        
    
    #finds the length of a specific vertice
    def length_of_vertice(self,vertice:list)->float:
        
        return math.dist(vertice[0].return_coordinates(),vertice[1].return_coordinates())   
    
    #returns the new lower center that can be created from the vertice given
    def find_center_coordinates(self,vertice):
        
        p1,p2=vertice[0],vertice[1]
        return point((p1.x+p2.x)/2,(p1.y+p2.y)/2)
            
    #Manifesting points,vertices,rectangle and rules out covered vertices by upper polygons        
    def manifest_polygon(self):
            
        added_angle=2*np.pi/self.points_amount
        agg_angle=self.angle
        for p in range(self.points_amount):
            self.points.append(self.pin_point(agg_angle))
            agg_angle+=added_angle
            
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
            p_list.append(p.return_coordinates())
        p_path=path.Path(p_list)
        
        for v in self.vertices:
                        
            if p_path.contains_point(self.find_center_coordinates(v).return_coordinates()) and (v not in self.covered_vertices):
                self.covered_vertices.append(v)
        if len(self.covered_vertices)==len(self.vertices):
            return True 
class layer:
    
    def __init__(self,polygons:list,layer_num:int)->None:
        
        self.color_scheme=[]
        self.polygons=polygons
        self.layer_num=layer_num
        self.covered_polygons=[]
    
    def __repr__(self) -> str:
        
        return   "layer #{layernum}, polygons:\n{polypoints}\n".format(layernum=self.layer_num,polypoints=self.polygons)
    
    
    #adds a polygon to the polygon list of the layer while associating it with current layer and returning it for further manipulation    
    def add_polygon(self,center:point,radius:float)->None:
        
        new_polygon=polygon(random.randint(3,3),center,radius,random.random()*np.pi,self.layer_num)
        new_polygon.manifest_polygon()
        self.polygons.append(new_polygon)
        
        return new_polygon
    
    #chooses a polygon from layer
    def choose_random_polygon(self):
        
        clean_poly_list=[]
        for p in self.polygons:
            if len(p.vertices) != len(p.covered_vertices):
                clean_poly_list.append(p)
                
        random_poly=random.choice(clean_poly_list)
        
        return random_poly

              
    
            
            
        
        
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
            
            for p in [x for x in self.polygons if new_center!=x.center]:
                if new_radius>math.dist([new_center.x,new_center.y],[p.center.x,p.center.y])-p.radius:
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
        self.layers.append(layer([polygon(random.randint(3,3),point(0,0),10,0,0)],0))
        self.layers[0].polygons[0].manifest_polygon()
        
        self.covered_layers=[]
    
    def __repr__(self) -> str:
                
        return "The layers:\n{layerlist}".format(layerlist=self.layers) 
    
    #Creates a new layer
    def new_layer(self,number_of_colors_in_layer:int)->None:
        self.layers.append(layer([],len(self.layers)))
        self.layers[-1].create_color_scheme(number_of_colors_in_layer)
    
    def cover_all_elements(self,upper_polygon:polygon,lower_polygon:polygon):
        
        layer_list=[l for l in self.layers if l not in self.covered_layers]
        for l in layer_list:
            l.mark_covered(upper_polygon,lower_polygon)
            

        
           
           
    #The creation of the whole polygon system    
    def manifest_polygon_system(self,number_of_polygons:int,range_of_size:int)->None:
        
        for p in range(number_of_polygons):
            
            
            upper_polygon=random.choice(list(set(self.layers)-set(self.covered_layers))).choose_random_polygon()
            upper_vertice=upper_polygon.view_random_vertice()
                
                
            if upper_polygon in self.layers[-1].polygons:
                self.new_layer((3))
                upper_vertice_length=upper_polygon.length_of_vertice(upper_vertice)
                lower_polygon=self.layers[-1].add_polygon(upper_polygon.find_center_coordinates(upper_vertice),random.uniform(upper_vertice_length*(5/6),upper_vertice_length*1.05))

            else:
                
                #a function that makes sure the radius of the polygon will not overlap with any existing polygons in the same layer.
                lower_center=upper_polygon.find_center_coordinates(upper_vertice)
                approved_radius=self.layers[upper_polygon.layer+1].return_good_radius(lower_center)
                lower_polygon=self.layers[upper_polygon.layer+1].add_polygon(lower_center,approved_radius)
                
            self.cover_all_elements(upper_polygon,lower_polygon) 
            
                

poly_sys=polygon_system(False)
poly_sys.manifest_polygon_system(8,10)
print(poly_sys)


            
            
            
        
        
        