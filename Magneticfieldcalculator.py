import PIL
import magpylib as mag3
from magpylib import current
from magpylib._lib.obj_classes.class_Collection import Collection
import matplotlib
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import cv2 as cv
import imageio
from numpy.lib.arraypad import pad



def m_field_of_current():
    
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
    
    ##Create the figure that holds the streamplot
    w=40
    h=25
    dpi=300
    fig=plt.figure(figsize=(w,h),dpi=dpi,frameon=True)
    
    #Creating and painting the subplot
    ax2=fig.add_subplot()
    X,Z=np.meshgrid(xs,ys)
    U,V=Bs[:,:,0], Bs[:,:,1]
    dens=15
    lw=4
    ax2.streamplot(X,Z,U,V,color=np.log(U**16+V**16),density=dens,arrowsize=0,linewidth=lw)
    matplotlib.rc('axes',edgecolor='green')
    ax2.add_patch(Rec1)
    ax2.add_patch(Rec2)
    plt.axis('off')
    plt.savefig('./images/universe/NewAmpereT_1_c{c}_vert_x{vx}z{vz}_ls{ls}stps{steps}_figsz_w{w}h{h}dpi{dpi}_density_{dens}_linewidth{lwid}.png'.format(c=c,vx=vx,vz=vz,ls=ls,steps=steps,w=w,h=h,dpi=dpi,dens=dens,lwid=lw),transparent=False,edgecolor=fig.get_edgecolor(),bbox_inches='tight')
    plt.tight_layout()
    print("Done")
    

Image.MAX_IMAGE_PIXELS=500000000
#print(checkifsymmetrical('Try.png'))
m_field_of_current()