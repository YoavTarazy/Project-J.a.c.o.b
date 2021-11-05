import numpy as np
import math
import random

class point:
    
    def __init__(self,x:float,y:float) -> None:
        self.x=x
        self.y=y
        self.z=0
        
    def return_coordinate(self):
        return (self.x,self.y) 

class layer:
    
    def __init__(self,polygons:list,layer_num:int)->None:
        
        self.color_scheme=[]
        self.polygons=polygons
        self.layer_num=layer_num
        
    
    #adds a polygon to the polygon list of the layer while associating it with current layer and returning it for further manipulation    
    def add_polygon(self,center:point,radius:float)->None:
        
        new_polygon=polygon(random.randint(3,8),center,radius,random.random()*np.pi,self.layer_num).manifest_polygon()
        self.polygons.append(new_polygon)
        return new_polygon
    
    def view_polygon(self):
        return random.choice(self.polygons)
         
    def create_color_scheme(self,gradient_amount:int)->None:
        
        color_palette=[]
        comp_color_palette=[]
        
        for c in range(gradient_amount):
            color=[random.random(130,255),random.random(130,255),random.random(130,255)]
            color_palette.append(color)
            comp_color_palette.append([255-color[0],255-color[1],255-color[2]])
            
        self.color_scheme=color_palette+comp_color_palette

class polygon:
    
    def __init__(self,points_amount:int,center_coordinate:point,radius:float,angle:float,layer:int) -> None:
        
        self.points_amount=points_amount
        self.center=center_coordinate
        self.radius=radius
        self.angle=angle
        self.layer=layer
        self.points=[]
        self.vertices=[]
    
    
    def pin_point(self,agg_angle)->point:
        
        return point(self.center.x+self.radius*np.cos(agg_angle),self.center.y+self.radius*np.sin(agg_angle))
    
    def manifest_polygon(self):
            
        added_angle=2*np.pi/self.points_amount
        agg_angle=self.angle
        for p in range(self.points_amount):
            self.points.append(self.pin_point(agg_angle))
            agg_angle+=added_angle
            
        self.points.append(self.points[0])

    def view_vertice(self):
        
        chosen_point=random.choice(self.points[0:-1])
        vertice=[chosen_point,self.points[self.points.index(chosen_point)+1]]
        return vertice
        
class polygon_system:
    
    def __init__(self,manual:bool) -> None:
        
        self.Manual=manual
        
        #Building first layer and center
        self.layers=[]
        self.marked_vertices=[]
        self.layers.append(layer([polygon(random.randint(3,6),point(0,0),random.random(10,20),0,0)],0))
        self.layers[0].polygons[0].manifest_polygon()
    
    #Returns the center from of a vertice
    def find_center(self,vertice)->point:
        return point((vertice[0].x+vertice[1].x)/2,(vertice[0].y+vertice[1].y)/2)
    
    #Creates a new layer
    def new_layer(self,number_of_colors_in_layer:int)->None:
        self.layers.append(layer([],len(self.layers)).create_color_scheme(number_of_colors_in_layer))
    
    def check_if_covered(polygon)
    
    #The creation of the whole polygon system    
    def manifest_polygon_system(self,number_of_polygons:int,range_of_size:int)->None:
        
        for p in range(number_of_polygons):
            
            #This 'marked' segment is here to make sure we do not overlap lower polygons on the same upper vertice, all used vertices are added to a list
            is_marked=True
            while is_marked:
                upper_polygon=random.choice(self.layers).view_polygon()
                upper_vertice=upper_polygon.view_vertice()
                if upper_vertice not in self.marked_vertices:
                    self.marked_vertices.append(upper_vertice)
                is_marked=False
                
            if upper_polygon in self.layers[-1]:
                self.new_layer(3)
                lower_polygon=self.layers[-1].add_polygon(self.find_center(upper_vertice),random.random(upper_polygon.radius/2,upper_polygon.radius*3/4))
            else:
                
                #a function that makes sure the radius of the polygon will not overlap with any existing polygons in the same layer.
                lower_center=self.find_center(upper_vertice)
                approved_radius=return_good_radius()
                
                lower_polygon=self.layers[upper_polygon.layer+1].add_polygon(lower_center,approved_radius)
            
            
            
        
        
        