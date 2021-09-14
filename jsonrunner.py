import numpy as np
import json
import math
from PIL import Image

#pulls gradient list from original pic and saves it to Json
def line_pallete_toJson(pix):
    h,w,rgb=pix.shape
    colors=np.unique(pix.reshape(-1, pix.shape[2]), axis=0)
    colors=colors.tolist()
    colors.remove([255,255,255,255])
    print(colors)
    with open('./json/colors of lines.json','w') as f:
        json.dump(colors,f)
        
        
        
#Fills a Json with an array that matches the image but contains distances from closest center              
def distances_to_Json(pix,reddots):
    h,w,rgb=pix.shape
    distances=np.zeros((h,w),dtype=float)
    for py in range(h):
        for px in range(w):
            t=1000000000
            for dot in reddots:
                if(math.dist((py,px),dot)<t):
                    t=math.dist((py,px),dot)
                    distances[py][px]=int(t)
            
            
            
    with open('./json/distances.json','w') as f:
        json.dump(distances.tolist(),f,ensure_ascii=False, indent=4)    


#image loader + turns all colors beside white to black.
def imageload_blacklines(img):
    pic=Image.open(img)
    red=[]
    pix=np.array(pic)
    h,w,bpp =pix.shape
    for py in range(h):
        for px in range(w):
            p=pix[py][px]
            #change to np.where and define specific pixels, Combine findredpixels to this function
            if(p[0]!=255 and p[1]!=255 and p[2]!=255 ):
                   if (pix[py][px][1]!=0 and pix[py][px][2]!=0):
                      p[0],p[1],p[2]=0,0,0
            elif (p[0]==255 and p[1]==0 and p[2]==0):
                red.append((py,px))
    
    #Saves red values in a Json                      
    with open('./json/reddots2.json','w') as f:
        json.dump(red,f,ensure_ascii=False, indent=4)  
                   
        
    pic2=Image.fromarray(pix)
    pic2.save("./images/universe/blackendpic.png")