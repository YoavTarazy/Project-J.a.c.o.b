import numpy as np
import json
import math
from PIL import Image
import requests
import math_zone
from Jacobprocessing import is_pixel_color

#pulls gradient list from original pic and saves it to Json
def line_pallete_toJson(pix):
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

#Finding the polygon lines and the distance of white tiles from them
def find_reddots_and_distances(img):
    pix=np.array(Image.open(img+'.png'))
    h,w,rgba=pix.shape
    reds=[]
    dist=np.zeros((h,w),dtype=float)
    for py in range(h):
        for px in range(w):
            p=pix[py][px]
            if is_pixel_color(pix[py][px],(255,0,0)):
                reds.append((px,py))
                dist[py][px]=0
                
    #Saves red values in a Json                      
    with open('./json/reddots.json','w') as f:
        json.dump(reds,f,ensure_ascii=False, indent=4)  
    
    print("found red centers")
    
    for  py in range(h):
        for px in range(w):
            if not is_pixel_color(pix[py][px],(255,0,0)) and not is_pixel_color(pix[py][px],(0,0,0)):
                point1,point2=math_zone.find_two_closest_points_from_point(reds,(px,py))
                x_intersect,y_intersect=math_zone.find_intersect_point(point1,point2,(px,py))
                dist[py][px]=math.dist((x_intersect,y_intersect),(px,py))
                
    
    #saves distances of white tiles from the closest red tile
    with open('./json/distances.json','w') as f:
        json.dump(dist.tolist(),f,ensure_ascii=False, indent=4) 
    
    print('found distances')

def pull_colours():
    url ='https://gist.githubusercontent.com/rortian/7516084/raw/1834f5f6475b74e18c05814f8e8441aa5b2f9adc/svg-named-colors.json'
    resp=requests.get(url)
    dic=json.loads(resp.text)
    return dic     


