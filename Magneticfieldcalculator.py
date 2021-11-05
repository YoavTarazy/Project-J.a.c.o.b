import magpylib as mag3
from magpylib import current
from magpylib._lib.obj_classes.class_Collection import Collection
from magpylib._lib.display.display import display
import matplotlib
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import json
import os
import random
import jsonrunner
import Jacobprocessing
from PIL import Image
import math_zone

  

#Creates one polygon with a given center, amount of points in polygon and radius from circle
def create_magnetic_shape(num_of_points,center_coords,length_of_radius,Current):
    
    #List that holds the wires creating magnetic field in polygon.
    list_of_currents=[]
    
    #This list holds all coordinates of points created in the polygon.
    list_of_points_coords=math_zone.find_points_in_circle(num_of_points,center_coords,length_of_radius)
    for p in list_of_points_coords:
        list_of_currents.append(mag3.current.Line(current=(Current/num_of_points),vertices=[(p[0],p[1],1),(p[0],p[1],-1)]))
    
    c=Collection(list_of_currents)
    return c,list_of_points_coords

#Generates mutliple magnetic polygons in space
def create_multiple_randomized_magnetic_shapes(x_axis,y_axis,min_radius,max_radius,current):
    
    #Amount of polygons to create
    num_of_shapes=1
    #list containing all magnet objects created in plot
    list_of_magnet_polygons=[]
    #list containing all centers and their respective radius for each polygon
    list_of_centers_and_radiuses=[]
    #a list that holds a list of coordinates that represent a polygon.
    list_of_poly=[]
    #counter
    s=0
    
    while len(list_of_magnet_polygons) <num_of_shapes:
        num_of_points=8
        center_coords=(random.randint(-x_axis+(int(0.3*x_axis)),x_axis-(int(0.3*x_axis))),random.randint(-y_axis+(int(0.3*y_axis)),y_axis-(int(0.3*y_axis))),0)
        length_of_radius=random.randint(min_radius,max_radius)
        magnet,poly=create_magnetic_shape(num_of_points,center_coords,length_of_radius,current)
        if len(list_of_centers_and_radiuses)<1:
            list_of_centers_and_radiuses.append((center_coords,length_of_radius))
            list_of_magnet_polygons.append(magnet)
            list_of_poly.append(poly)
        else:
            if not math_zone.check_if_circles_intersect(list_of_centers_and_radiuses,center_coords,length_of_radius):
                list_of_poly.append(poly)
                list_of_centers_and_radiuses.append((center_coords,length_of_radius))
                list_of_magnet_polygons.append(magnet)
                
    c=Collection(list_of_magnet_polygons)
    return c,list_of_poly,list_of_centers_and_radiuses

#Modules magnetic system
def module_magnetic_polygons(x_axis,y_axis,min_radius,max_radius,steps_on_axis,current):
    #Creating the magnetic module
    c,polys,centers_and_radius=create_multiple_randomized_magnetic_shapes(x_axis,y_axis,min_radius,max_radius,current)
    
    #Building matplotlib UI
    steps=steps_on_axis
    xs=np.linspace(-x_axis,x_axis,steps)
    ys=np.linspace(-y_axis,y_axis,steps)
    
    #Performing the calculations
    POS=np.array([(x,y,0) for y in ys for x in xs])
    Bs = c.getB(POS).reshape(steps ,steps,-1)
    
    return xs,ys,Bs,polys,centers_and_radius

    

#Grants a graphic expression to magnetic module and saves the picture    
def calculate_randomized_magnetic_field(current,category,gradienttype,t1,t2,magentic_calculations):
    
    xs,ys,Bs,polys,centers=magentic_calculations[0],magentic_calculations[1],magentic_calculations[2],magentic_calculations[3],magentic_calculations[4]
    
    
    
    ##Create the figure that holds the streamplot
    w=40
    h=25
    dpi=100
    fig=plt.figure(figsize=(w,h),dpi=dpi,frameon=True)
    
    #Creating and painting the subplot
    ax2=fig.add_subplot()
    X,Y=np.meshgrid(xs,ys)
    U,V=Bs[:,:,0], Bs[:,:,1]

    
    #defining the subplot - streamplot
    dens=4
    lw=4
    
    #Create Colored Picture.
    formula=np.log(U**t1+V**t2) #2 * np.log(np.hypot(U, V)) 
    ax2.streamplot(X,Y,U,V,density=dens,linewidth=lw,cmap=gradienttype,arrowsize=0,color=formula)   
    plt.tight_layout(pad=0)
    plt.axis('off')   
    
    path1='./images/universe/magnetic_emotion/{current}_{category}_{gradient_type}_x_{x}_y_{y}'.format(current=current,category=category,gradient_type=gradienttype,x=t1,y=t2)
    dirpath='./images/universe/magnetic_emotion'
    path_exists= os.path.exists(dirpath)
    if not path_exists:
        os.makedirs(dirpath)
    
    plt.savefig(path1+'.png',transparent=False,bbox_inches='tight')
        
    print('finished - {category}/{gradient_type}/x_{x}_y_{y}.png'.format(category=category,gradient_type=gradienttype,x=t1,y=t2)) 
    
    ##Bluleprint Mode
    ax2.streamplot(X,Y,U,V,density=dens,linewidth=lw,arrowsize=0,color='Black')
    
    for poly in polys:
        for rec in poly:
            rectangle=patches.Rectangle((rec[0],rec[1]),0.03,0,color='red')
            ax2.add_patch(rectangle)
    for center in centers:
        rec_center=patches.Rectangle(center[0],0.03,0,color='Blue')
        ax2.add_patch(rec_center)
        
    path2='./images/universe/magnetic_emotion/{current}_{category}_{gradient_type}_x_{x}_y_{y}_blackend'.format(current=current,category=category,gradient_type=gradienttype,x=t1,y=t2)
    plt.tight_layout(pad=0)
    plt.axis('off') 
    plt.savefig(path2+'.png',transparent=False,bbox_inches='tight')    
    plt.clf()
    
    return path2,path1
    
    
    #Create blackend pic
    #jsonrunner.imageload_blacklines(path+".png")
    #with open('./json/reddots2.json') as f:
        #list_of_dots=list(json.load(f))
    
    #color the pic given                      
    #jsonrunner.distances_to_Json(np.array(Image.open(path+"_blackend.png")))
    #with open('./json/distances.json') as f:
        #dist=np.array(json.load(f))
        
    #Jacobprocessing.color_tiles(np.array(Image.open(path+'png')),dist,10,10,Jacobprocessing.random_color_pallete(jsonrunner.pull_colours(),10))
    
    