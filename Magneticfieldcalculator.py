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
def create_magnetic_shape(num_of_points,center_coords,length_of_radius):
    list_of_currents=[]
    list_of_recs_one_polygon=[]
    list_of_points_coords=math_zone.find_points_in_circle(num_of_points,center_coords,length_of_radius)
    print(list_of_points_coords)
    for p in list_of_points_coords:
        list_of_currents.append(mag3.current.Line(current=10/num_of_points,vertices=[(p[0],p[1],1),(p[0],p[1],-1)]))
        list_of_recs_one_polygon.append(patches.Rectangle((p[0],p[1]),0.1,0.1,color='red'))
    
    c=Collection(list_of_currents)
    return c,list_of_recs_one_polygon

#Generates mutliple magnetic polygons in space
def create_multiple_randomized_magnetic_shapes(x_axis,y_axis,min_radius,max_radius):
    num_of_shapes=random.randint(8,10)
    list_of_magnet_polygons=[]
    list_of_centers_and_radiuses=[]
    list_of_rec=[]
    print(len(list_of_centers_and_radiuses))
    for s in range(num_of_shapes):
        num_of_points=random.randint(2,8)
        center_coords=(random.randint(-x_axis+(int(0.2*x_axis)),x_axis+(int(0.2*x_axis))),random.randint(-y_axis+(int(0.2*y_axis)),y_axis+(int(0.2*y_axis))),0)
        length_of_radius=random.randint(min_radius,max_radius)
        magnet,rec=create_magnetic_shape(num_of_points,center_coords,length_of_radius)
        if len(list_of_centers_and_radiuses)<1:
            list_of_centers_and_radiuses.append((center_coords,length_of_radius))
            list_of_magnet_polygons.append(magnet)
            list_of_rec.append(rec)
        else:
            if math_zone.check_if_circles_intersect(list_of_centers_and_radiuses,center_coords,length_of_radius):
                s=s-1
            else:
                list_of_rec.append(rec)
                list_of_centers_and_radiuses.append((center_coords,length_of_radius))
                list_of_magnet_polygons.append(magnet)
    
    c=Collection(list_of_magnet_polygons)
    return c,list_of_rec

#Modules magnetic system
def module_magnetic_polygons(x_axis,y_axis,min_radius,max_radius,steps_on_axis):
    #Creating the magnetic module
    c,recs=create_multiple_randomized_magnetic_shapes(x_axis,y_axis,min_radius,max_radius)
    
    #Building matplotlib UI
    steps=steps_on_axis
    xs=np.linspace(-x_axis,x_axis,steps)
    ys=np.linspace(-y_axis,y_axis,steps)
    
    #Performing the calculations
    POS=np.array([(x,y,0) for y in ys for x in xs])
    Bs = c.getB(POS).reshape(steps ,steps,-1)
    
    return xs,ys,Bs,recs

    

#Grants a graphic expression to magnetic module and saves the picture    
def calculate_randomized_magnetic_field(counter,category,gradienttype,t1,t2,magentic_calculations):
    
    xs,ys,Bs,recs=magentic_calculations[0],magentic_calculations[1],magentic_calculations[2],magentic_calculations[3]
    
    
    ##Create the figure that holds the streamplot
    w=40
    h=25
    dpi=300
    fig=plt.figure(figsize=(w,h),dpi=dpi,frameon=True)
    
    #Creating and painting the subplot
    ax2=fig.add_subplot()
    X,Y=np.meshgrid(xs,ys)
    U,V=Bs[:,:,0], Bs[:,:,1]

    
    #defining the subplot - streamplot
    dens=7
    lw=4
    
    formula=np.log(U**t1+V**t2) #2 * np.log(np.hypot(U, V)) 
    ax2.streamplot(X,Y,U,V,density=dens,linewidth=lw,cmap=gradienttype,arrowsize=0,color=formula)
    for rec in recs:
        for p in rec:
            ax2.add_patch(p)
        
    plt.tight_layout()
    plt.axis('off')   
    path='./images/universe/magnetic_emotion/{counter}_{category}_{gradient_type}_x_{x}_y_{y}'.format(counter=counter,category=category,gradient_type=gradienttype,x=t1,y=t2)
    dirpath='./images/universe/magnetic_emotion'
    path_exists= os.path.exists(dirpath)
    if not path_exists:
        os.makedirs(dirpath)
    
    plt.savefig(path+'.png',transparent=False,bbox_inches='tight')
        
    print('finished - {category}/{gradient_type}/x_{x}_y_{y}.png'.format(category=category,gradient_type=gradienttype,x=t1,y=t2)) 
    plt.clf()
    
    
    #Create blackend pic
    #jsonrunner.imageload_blacklines(path+".png")
    #with open('./json/reddots2.json') as f:
        #list_of_dots=list(json.load(f))
    
    #color the pic given                      
    #jsonrunner.distances_to_Json(np.array(Image.open(path+"_blackend.png")))
    #with open('./json/distances.json') as f:
        #dist=np.array(json.load(f))
        
    #Jacobprocessing.color_tiles(np.array(Image.open(path+'png')),dist,10,10,Jacobprocessing.random_color_pallete(jsonrunner.pull_colours(),10))
    
    