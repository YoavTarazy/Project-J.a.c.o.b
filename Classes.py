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
    
    def __init__(self,x:float,y:float) -> None:
        self.x=x
        self.y=y
    
    def __repr__(self) -> str:
        
        return "{xy}\n".format(xy=[self.x,self.y]) 
    
    def return_coordinates(self):
        return [self.x,self.y]
    
    def return_coordinates_numpy(self):
        return np.array([self.x,self.y])
 

class polygon:
    
    def __init__(self,points_amount:int,center_coordinate:point,radius:float,angle:float,layer:int) -> None:
        
        self.points_amount=points_amount
        self.center=center_coordinate
        self.radius=radius
        self.angle=angle
        self.layer=layer
        
        #holds all points of polygon
        self.points=[]
        
        #edges created from points for easier testing
        self.edges=[]
        self.triangles=np.array([])
        
        #which edges are not to be treated as worthy polygon sources
        self.covered_edges=[]
        self.covered=False
        
        #a coarse filtering for points outside of it.
        self.rec_vertices=[]
        self.full_rec_points=np.array([])
    
    def __repr__(self) -> str:
        
        return "Polygon center: {center},Polygon Radius: {radius}\nPolygon points:\n{points}".format(center=self.center,radius=self.radius,points=self.points)
    
    
    
    #Before Numpy
    
    def pin_point(self,agg_angle)->point:
        
        return point(self.center.x+self.radius*np.cos(agg_angle),self.center.y+self.radius*np.sin(agg_angle))
      
    def manifest_polygon_triangles(self):
            
        triangles=[]
        for v in self.edges:
            pv1=v[0].return_coordinates_numpy()
            pv2=v[1].return_coordinates_numpy()
            pc=self.center.return_coordinates_numpy()
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

        #This function checks for covered verices to not be used in further creation of polygons.
    
    def find_covered_edges(self,other):
        
        p_list=[]
        for p in other.points:
            p_list.append(p.return_coordinates())
        p_path=path.Path(p_list)
        
        for v in self.edges:
                        
            if p_path.contains_point(self.find_center_coordinates(v).return_coordinates()) and (v not in self.covered_edges):
                self.covered_edges.append(v)
        if len(self.covered_edges)==len(self.edges):
            return True 


     #finds the length of a specific vertice
    
    def length_of_vertice(self,vertice:list)->float:
        
        return math.dist(vertice[0].return_coordinates(),vertice[1].return_coordinates())   

    def find_center_coordinates(self,vertice):
        
        p1,p2=vertice[0],vertice[1]
        return point((p1.x+p2.x)/2,(p1.y+p2.y)/2)

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
            if len(p.edges) != len(p.covered_edges):
                clean_poly_list.append(p)
                
        random_poly=random.choice(clean_poly_list)
        
        return random_poly
                
              
    def rule_out_edges_dueto_lower_poly(self,lower_polygon:polygon):
        
        for polys in self.polygons:
            for edge in polys.edges:
                if mz.check_point_in_triangles(np.asarray(lower_polygon.triangles),np.asarray(edge[0])) and mz.check_point_in_triangles(np.asarray(lower_polygon.triangles),np.asarray(edge[1])):
                    
                    polys.update_covered_edges(edge)
                    if polys.covered:
                        self.covered_polygons.append(polys)
                    
            
                  
        
        
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
        
<<<<<<< Updated upstream
        layer_list=[l for l in self.layers if l not in self.covered_layers]
        for l in layer_list:
            l.mark_covered(upper_polygon,lower_polygon)
            

=======
        polygon.edges[(self.check_point_inside_triangles)]
        
        t=symbols('t',,Real=True)
        outcome=solveset((t**2+2)<0,t,S.Reals)
        
        
>>>>>>> Stashed changes
    
    
    def manifest_polygon_system_blueprint(self,number_of_polygons:int):
        
        for poly in range(number_of_polygons):
            
            upper_polygon=random.choice(list(set(self.layers)-set(self.covered_layers))).choose_random_polygon()
            upper_edge=upper_polygon.view_random_edge()    
            
            if upper_polygon in self.layers[-1].polygons:
                
                self.new_layer(3)
                upper_edge_length=upper_polygon.length_of_vertice(upper_edge)
                
                
                lower_polygon=self.layers[-1].add_polygon(upper_polygon.find_center_coordinates(upper_edge),random.uniform(upper_edge_length*(5/6),upper_edge_length*1.05))
                upper_polygon
            
            else:
              ##THIS needs to change to running on radiuses and working with intersection of circle functions and ruling out according to cone  
              
                lower_center=upper_polygon.find_center_coordinates(upper_edge)
                radius=random.uniform(upper_edge_length*(5/6),upper_edge_length*1.05)
                
                #Now this needs a section of adding to a layer and into th complete system
                
                
    #The creation of the whole polygon system    
    def manifest_polygon_system(self,number_of_polygons:int,range_of_size:int)->None:
        
        for p in range(number_of_polygons):
            
            
            upper_polygon=random.choice(list(set(self.layers)-set(self.covered_layers))).choose_random_polygon()
            upper_edge=upper_polygon.view_random_edge()
                
                
            if upper_polygon in self.layers[-1].polygons:
                self.new_layer((3))
                upper_edge_length=upper_polygon.length_of_vertice(upper_edge)
                lower_polygon=self.layers[-1].add_polygon(upper_polygon.find_center_coordinates(upper_edge),random.uniform(upper_edge_length*(5/6),upper_edge_length*1.05))

            else:
                
                #a function that makes sure the radius of the polygon will not overlap with any existing polygons in the same layer.
                lower_center=upper_polygon.find_center_coordinates(upper_edge)
                approved_radius=self.layers[upper_polygon.layer+1].return_good_radius(lower_center)
                lower_polygon=self.layers[upper_polygon.layer+1].add_polygon(lower_center,approved_radius)
                
            self.cover_all_elements(upper_polygon,lower_polygon) 
            
                
        
poly=polygon(3,point(0,0),10,0,0)
poly.manifest_polygon()
poly.manifest_polygon_triangles()
poly.classify_rec_points()
print('done')