import magpylib as mag3
from magpylib import current
from magpylib._lib.obj_classes.class_Collection import Collection
import matplotlib
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
import json
import os



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
    dens=15
    lw=4
<<<<<<< Updated upstream
    ax2.streamplot(X,Y,U,V,density=dens,linewidth=lw,cmap=gradienttype,color=np.log(U**t1+V**t2))
=======
<<<<<<< Updated upstream
    ax2.streamplot(X,Z,U,V,color=np.log(U**16+V**16),density=dens,arrowsize=0,linewidth=lw)
    matplotlib.rc('axes',edgecolor='green')
    ax2.add_patch(Rec1)
    ax2.add_patch(Rec2)
    plt.axis('off')
    plt.savefig('./images/universe/NewAmpereT_1_c{c}_vert_x{vx}z{vz}_ls{ls}stps{steps}_figsz_w{w}h{h}dpi{dpi}_density_{dens}_linewidth{lwid}.png'.format(c=c,vx=vx,vz=vz,ls=ls,steps=steps,w=w,h=h,dpi=dpi,dens=dens,lwid=lw),transparent=False,edgecolor=fig.get_edgecolor(),bbox_inches='tight')
=======
    ax2.streamplot(X,Y,U,V,density=dens,linewidth=lw,cmap=gradienttype,arrowsize=0,color=np.log(U**t1+V**t2))

    #ax2.add_patch(Rec1)
    #ax2.add_patch(Rec2)
    #plt.axis('off')
    plt.axis('off')
>>>>>>> Stashed changes
    plt.tight_layout()
>>>>>>> Stashed changes
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

