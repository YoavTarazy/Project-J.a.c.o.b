import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import matplotlib.patches as patch
import magpylib as mag3

#Creating magpylib

current1=mag3.current.Line(1.0,vertices=[[0,0,1],[0,0,-1]])
x_axis,y_axis=50,50
steps=1000
xs=np.linspace(-x_axis,x_axis,steps)
ys=np.linspace(-y_axis,y_axis,steps)
    
#Performing the calculations
POS=np.array([(x,y,0) for y in ys for x in xs])
Bs=current1.getB(POS).reshape(steps ,steps,-1)


##Building the figure and streamplot
w=40
h=25
dpi=200
fig=plt.figure(figsize=(w,h),dpi=dpi)
ax2=fig.add_subplot()

#Taking all x,y and their respective fields in the relevant axis.
X,Y=np.meshgrid(xs,ys)
U,V=Bs[:,:,0],Bs[:,:,1]

#plotting
ax2.streamplot(X,Y,U,V,density=1,arrowsize=0,color='black')
ax2.set_position([0, 0, 1, 1])
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['bottom'].set_visible(False)
ax2.spines['left'].set_visible(False)
#Adding a test pixel
rectangle=patch.Rectangle([0,0],0.01,0,color='red')
ax2.add_patch(rectangle)


plt.savefig('Trial.png')
#plt.show()

#finding said pixel
pix=np.asarray(Image.open('Trial.png'))
h,w,ph=pix.shape
new_h,new_w=h/2,w/2
print(type(new_h))

pix[int(new_h)][int(new_w)]=[0,0,255,255]
pic=Image.fromarray(pix)
pic.save('altered_Trial.png')

    