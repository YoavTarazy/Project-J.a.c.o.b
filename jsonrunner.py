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


#Creates a json file containing categorized cmaps in matplotlib
def cmaps_to_json():
    cmap_list=[('Perceptually Uniform Sequential', [
            'viridis', 'plasma', 'inferno', 'magma']),
         ('Sequential', [
            'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
            'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
            'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']),
         ('Sequential (2)', [
            'binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink',
            'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia',
            'hot', 'afmhot', 'gist_heat', 'copper']),
         ('Diverging', [
            'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu',
            'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic']),
         ('Qualitative', [
            'Pastel1', 'Pastel2', 'Paired', 'Accent',
            'Dark2', 'Set1', 'Set2', 'Set3',
            'tab10', 'tab20', 'tab20b', 'tab20c']),
         ('Miscellaneous', [
            'flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern',
            'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg', 'hsv',
            'gist_rainbow', 'rainbow', 'jet', 'nipy_spectral', 'gist_ncar'])]
    
    with open('./json/cmaps.json','w') as f:
        json.dump(cmap_list,f,ensure_ascii=False, indent=4)
        
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

#image loader + turns all colors besides white to black.
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
    
cmaps_to_json()    
