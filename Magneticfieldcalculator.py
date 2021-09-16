import magpylib as mag3
from magpylib import current
from magpylib._lib.obj_classes.class_Collection import Collection
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

def random_magnetic_field(amount_of_magnets,currents,locations):
    c=Collection()
    list_of_magnets=[]
    rec_centers=[]
    for m in range(amount_of_magnets):
        magnet=mag3.current.Line(current=currents[m],vertices=[(locations[m][0],locations[m][1],10),(locations[m][0],locations[m][1],-10)])
        list_of_magnets.append(magnet)
        c.add(magnet)
        rec_centers.append(patches.Rectangle((locations[m][0],locations[m][1]),0.01,0.01,color='red'))
        
    #Building the UI
    ##Building the space to present the calculations on
    ls=20
    steps=2000
    xs=np.linspace(-ls,ls,steps)
    ys=np.linspace(-ls,ls,steps)
    
    ##Performing the calculations
    POS=np.array([(x,y,0) for y in ys for x in xs])
    Bs = c.getB(POS).reshape(steps ,steps,-1)
    
    return (xs,ys,Bs,rec_centers)
    
def calculate_randomized_magnetic_field(counter,category,gradienttype,t1,t2,magentic_calculations,magnets):
    
    xs,ys,Bs,rectangles=magentic_calculations[0],magentic_calculations[1],magentic_calculations[2],magentic_calculations[3]
    
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
    dens=8
    lw=4
    #ax2.add_patch(Rec1)
    #ax2.add_patch(Rec2)
    formula=np.log(U**t1+V**t2) #2 * np.log(np.hypot(U, V)) 
    ax2.streamplot(X,Y,U,V,density=dens,linewidth=lw,cmap=gradienttype,arrowsize=0,color=formula)
    for rec in rectangles:
        ax2.add_patch(rec)
    plt.tight_layout()
    plt.axis('off')   
    path='./images/universe/magnetic_emotion/{counter}_{category}_{gradient_type}_x_{x}_y_{y}_numofmagnets_{amountofmagnets}'.format(counter=counter,category=category,gradient_type=gradienttype,x=t1,y=t2,amountofmagnets=magnets)
    dirpath='./images/universe/magnetic_emotion'
    plt.axis('off')
    path_exists= os.path.exists(dirpath)
    if not path_exists:
        os.makedirs(dirpath)
    
    plt.savefig(path+'.png',transparent=False,bbox_inches='tight')
        
    print('finished - {category}/{gradient_type}/x_{x}_y_{y}.png'.format(category=category,gradient_type=gradienttype,x=t1,y=t2)) 
    plt.clf()
    
    
    #Create blackend pic
    jsonrunner.imageload_blacklines(path+".png")
    with open('./json/reddots2.json') as f:
        list_of_dots=list(json.load(f))
    
    #color the pic given                      
    jsonrunner.distances_to_Json(np.array(Image.open(path+"_blackend.png")))
    with open('./json/distances.json') as f:
        dist=np.array(json.load(f))
        
    Jacobprocessing.color_tiles(np.array(Image.open(path+'png')),dist,10,10,Jacobprocessing.random_color_pallete(jsonrunner.pull_colours(),10))
    
    
def calculate_magnetic_field():

    #Creating The Magnets
    c=1
    vx,vz=400,10
    y1=mag3.current.Line(current=1,vertices=[(-400,0,-10),(-400,0,10)])
    y2=mag3.current.Line(current=-1,vertices=[(400,0,-10),(400,0,10)])
    Rec1= patches.Rectangle((-400,0),1,0,color='red')
    Rec2= patches.Rectangle((400,0),1,0,color='red')
    
    
    #Creating the collection
    c2=Collection(y1,y2)
    
    
    #Building the UI
    ##Building the space to present the calculations on
    ls=1000
    steps=2000
    xs=np.linspace(-ls,ls,steps)
    ys=np.linspace(-ls,ls,steps)
    
    ##Performing the calculations
    POS=np.array([(x,y,0) for y in ys for x in xs])
    Bs = c2.getB(POS).reshape(steps ,steps,-1)
    
    return (xs,ys,Bs)
    
def draw_and_color_magnetic_lines(category,gradienttype,t1,t2,magentic_calculations):
    
    xs,ys,Bs=magentic_calculations[0],magentic_calculations[1],magentic_calculations[2]
    
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
    dens=10
    lw=8
    #ax2.add_patch(Rec1)
    #ax2.add_patch(Rec2)
    ax2.streamplot(X,Y,U,V,density=dens,linewidth=lw,cmap=gradienttype,arrowsize=0,color=np.log(U**t1+V**t2))

    plt.tight_layout()
    path='./images/universe/{category}/{gradient_type}/x_{x}_y_{y}.png'.format(category=category,gradient_type=gradienttype,x=t1,y=t2)
    dirpath='./images/universe/{category}/{gradient_type}'.format(category=category,gradient_type=gradienttype)
    plt.axis('off')
    path_exists= os.path.exists(dirpath)
    if not path_exists:
        os.makedirs(dirpath)
    
    plt.savefig(path,transparent=False,bbox_inches='tight')
        
    print('finished - {category}/{gradient_type}/x_{x}_y_{y}.png'.format(category=category,gradient_type=gradienttype,x=t1,y=t2))
    
    plt.close()
    plt.clf()

