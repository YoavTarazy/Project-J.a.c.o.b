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
       self.np_edge=np.array([a.point,b.point],dtype=np.float32)
       self.edge_interval=Interval(0,1,left_open=False,right_open=False)

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
        
        return point(np.array([self.center.x+self.radius*np.cos(agg_angle),self.center.y+self.radius*np.sin(agg_angle)],dtype=np.float32))
      
    def manifest_polygon_triangles(self):
            
        triangles=[]
        for e in self.edges:
            pv1,pv2=e[0].point,e[1].point
            pc=self.center.point
            triangles.append(np.array([[pc,pv1],[pv1,pv2],[pv2,pv1]]))
        self.triangles=np.asarray(triangles,dtype=np.float32)
        
    def manifest_polygon(self):
            
        added_angle=2*np.pi/self.points_amount
        agg_angle=self.angle
        for p in range(self.points_amount):
            self.points.append(self.pin_point(agg_angle))
            agg_angle+=added_angle
        self.points.append(self.points[0])    
        self.edges=list(zip(self.points[0:-1],self.points[1:]))
        self.manifest_polygon_triangles()

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
                
    def check_polygons(self):
        
        for p in [p for p in self.polygons if p not in self.covered_polygons]:
            
            if len(p.covered_edges)==len(p.edges):
                self.covered_polygons.append(p)
        
        
class polygon_system:
    
    def __init__(self,layers:list) -> None:
        
        self.layers=[]
        self.layers.append(layer([polygon(random.randint(3,3),point(np.array([0,0])),10,0)]))
        self.layers[0].polygons[0].manifest_polygon()
        
        self.covered_layers=[]
    
    def __repr__(self) -> str:
                
        return "The layers:\n{layer_layerist}".format(layer_layerist=self.layers) 
    
    def new_layer(self,number_of_colors_in_layer:int)->None:
        
        self.layers.append(layer([]))
        self.layers[-1].create_color_scheme(number_of_colors_in_layer)

    def find_center_on_ue(self,upper_edge:edge,upper_poly_radius:float,existing_lower_polys:list):
        
        
        max_radius=random.uniform(0.5*upper_poly_radius,0.75*upper_poly_radius)
        former_interval=smp.sets.Interval(0,1,left_open=False,right_open=False)
        nlp_radius=max_radius
        t=symbols('t',domain=upper_edge.edge_interval)
        d=point(upper_edge.b.point-upper_edge.a.point)
        a=upper_edge.a
        
        
        for p in existing_lower_polys:
            
            pc=p.center
            in_root_exp=(a.x+t*d.x-pc.x)**2+(a.y+t*d.y-pc.y)**2
            root_exp=smp.sqrt(in_root_exp)
            func=root_exp-p.radius
            
            
            
            solution=solve_univariate_inequality(func>=0.5*upper_poly_radius,t).as_set()
            former_interval=former_interval.intersect(solution)
            
            if former_interval is EmptySet:
                return -1,-1
            
            
            current_max_radius=smp.calculus.util.maximum(func,t,domain=former_interval)
            max_radius=min(max_radius,current_max_radius)
            
            
        chosen_t=random.uniform(former_interval.left,former_interval.right)    
        
        for p in existing_lower_polys:
            
            pc=p.center
            in_root_exp=(a.x+t*d.x-pc.x)**2+(a.y+t*d.y-pc.y)**2
            root_exp=smp.sqrt(in_root_exp)
            func=root_exp-p.radius
            current_max_radius=func.subs(t,chosen_t)
            
            max_radius=min(max_radius,current_max_radius)
        
        nlp_center=point(a.point+chosen_t*d.point)
        nlp_radius=random.uniform(0.5*upper_poly_radius,max_radius)
        
        return nlp_center,nlp_radius

    def cover_new_polygon(self,new_polygon:polygon,upper_polygons:list):
        
        lt = smp.Symbol('lt')
        

        for le in new_polygon.edges:
            
           le=edge(le[0],le[1])
           la,lb=le.a,le.b
           ld=point(le.b.point-le.a.point)
           
           for upper_poly in upper_polygons:
               upx,upy=upper_poly.center.point
               
               inside_circle=smp.sqrt((la.x+lt*ld.x-upx)**2+(la.y+lt*ld.y-upy)**2)-upper_poly.radius
               inside=solve_univariate_inequality(inside_circle<=0,lt).as_set()
               
               if inside!=EmptySet:
                   
                    la_in=mz.check_point_in_triangles(upper_poly.triangles,la.point)
                    lb_in=mz.check_point_in_triangles(upper_poly.triangles,lb.point)
                   
                    if la_in==True and lb_in==True:
                       
                       new_polygon.covered_edges.append(le)
                       
                    elif la_in==True or lb_in==True:
                       
                       for ue in upper_polygons.edges:
                           
                           ue=edge(ue[0],ue[1])
                           ua,ub,ud=ue.a,ue.b,point(ue.b.point-ue.a.point)
                           t=smp.Symbol('t')
                           intersect_with_upper_edge=solveset(ua-la+t*(ud-ld),t,domain=Interval(0,1,left_open=True,right_open=True))
                           if intersect_with_upper_edge!=EmptySet:
                                if la_in==True:
                                    le.edge_interval.intersect(Interval(intersect_with_upper_edge.left,1))
                                else:
                                    le.edge_interval.intersect(Interval(0,intersect_with_upper_edge.left))
                                break;
                    break;

    def manifest_system_blueprint(self,num_of_polygons:int):
        
        p_num=0
        while p_num <= num_of_polygons:
            
         
            r_layer=random.choice([l for l in self.layers if l not in self.covered_layers])
            if r_layer!=self.layers[0]:
                two_levels_higher_layer=self.layers[self.layers.index(r_layer)-1]
            else:
                two_levels_higher_layer=layer([])
            r_polygon=random.choice([p for p in r_layer.polygons if p not in r_layer.covered_polygons])
            r_edge=random.choice([e for e in r_polygon.edges if e not in r_polygon.covered_edges])
            r_edge=edge(r_edge[0],r_edge[1])
            
            if self.layers[-1]==r_layer:
                
                
                new_lower_center,new_lower_radius=self.find_center_on_ue(r_edge,r_polygon.radius,[])
                new_polygon=polygon(random.randint(3,12),new_lower_center,new_lower_radius,random.uniform(0,2*np.pi))
                new_polygon.manifest_polygon()
                self.cover_new_polygon(new_polygon,r_layer.polygons)
                self.cover_new_polygon(new_polygon,two_levels_higher_layer.polygons)
                self.layers.append(layer([new_polygon]))
                p_num+=1
                r_polygon.covered_edges.append(r_edge)
            
            else:
                
                lower_layer=self.layers[self.layers.index(r_layer)+1]
                
                
                new_lower_center,new_lower_radius=self.find_center_on_ue(r_edge,r_polygon.radius,lower_layer.polygons)
                
                
                if new_lower_center!=-1 and new_lower_radius!=-1:
                    
                    new_polygon=polygon(random.randint(3,12),new_lower_center,new_lower_radius,random.uniform(0,2*np.pi))
                    new_polygon.manifest_polygon()
                    self.cover_new_polygon(new_polygon,r_layer.polygons)
                    self.cover_new_polygon(new_polygon,two_levels_higher_layer.polygons)
                    lower_layer.polygons.append(new_polygon)
                    p_num+=1
                    r_polygon.covered_edges.append(r_edge)
                    
                    
            
            r_layer.check_polygons()
            if len(r_layer.polygons)==len(r_layer.covered_polygons):
                self.covered_layers.append(r_layer)
            print(p_num)
                    
poly_sys=polygon_system([])
poly_sys.manifest_system_blueprint(10)
print('done')
            
            