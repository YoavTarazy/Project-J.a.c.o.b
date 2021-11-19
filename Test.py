import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import matplotlib.patches as patch


#Creating figure
w=5
h=3
dpi=300
fig=plt.figure(figsize=(w,h),dpi=dpi,frameon=True)

#Creating Plot

ax2=fig.add_subplot()
x=np.linspace(-1000,1000,1)
y=np.linspace(-1000,1000,1)
X,Y=np.meshgrid(x,y)
ax2.plot()
ax2.set_position([0, 0, 1, 1])
print(ax2.transData.transform([1,0]))




plt.show()