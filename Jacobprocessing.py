from matplotlib import colors
import numpy as np
import cv2 as cv2
from numpy.core.fromnumeric import ndim, shape
import scipy.ndimage as simg
from scipy import misc
from PIL import Image
import matplotlib.pyplot as plt
import math
import json
import time
from colour import Color
import requests
import random
import jsonrunner



             

#crops the image according to black edge around plot given earlier. DEPRACATED
def image_cropper(img):
    im=Image.open(img)
    blacklist=[]
    pix=np.asarray(im)
    h,w,rgb=pix.shape
    for py in range(h):
        for px in range(w):
            if is_pixel_color(pix[py][px],py,px,[0,0,0]):
                blacklist.append((py,px))
    unzipped_blacklist=list(zip(*blacklist))
    
    min_width=min(unzipped_blacklist[1])
    max_width=max(unzipped_blacklist[1])
    min_height=min(unzipped_blacklist[0])
    max_height=max(unzipped_blacklist[0])
    im2=im.crop(box=(min_width,min_height,max_width,max_height))
    im2.save('croppedimage.png')        
                 
#Checks color of specific pixel in the image.   
def is_pixel_color(pixel,colorRGB):
    if(pixel[0]==colorRGB[0] and pixel[1]==colorRGB[1] and pixel[2]==colorRGB[2]):
        return True
    return False


    
#recieves a starting color and an end color and returns a tuple of rgb values that are the gradient from start to end.        
def color_gradient_section(s_color,e_color,steps):
    
    red=Color(s_color)
    colors=list(red.range_to(Color(e_color),steps))
    for c in range(steps):
        colors[c]=colors[c].rgb
        colors[c]=(int(255*colors[c][0]),int(255*colors[c][1]),int(255*colors[c][2]))
    return colors

#This function colors one pixel from the image
#def color_a_pixel(pixel_rgb,coordinates,white_pallete,black_pallete):
    #if is_pixel_color()
    
    
#DEPRACATED This function calculates from the distance of the pixel from the closest center, the color it needs to be painted. DEPRACATED
def calculate_coloring_section(pix,distances,segment,sub_segment,colors_white,colors_black):
   h,w=distances.shape
   
   for py in range(h):
       for px in range(w):
           dis=distances[py][px]
           floor=int(dis/segment)
           step=round((dis%segment)/sub_segment)
           if is_pixel_color(pix[py][px],(255,255,255)):
               pix[py][px][0],pix[py][px][1],pix[py][px][2]=colors_white[min(3,floor)][min(9,step)][0],colors_white[min(3,floor)][min(9,step)][1],colors_white[min(3,floor)][min(9,step)][2]
           elif is_pixel_color(pix[py][px],(0,0,0)):
               pix[py][px][0],pix[py][px][1],pix[py][px][2]=colors_black[min(3,floor)][min(9,step)][0],colors_black[min(3,floor)][min(9,step)][1],colors_black[min(3,floor)][min(9,step)][2]
               
   img=Image.fromarray(pix)
   try:
    img.save(f'./images/Impression/Impression_1_floorsize_{segment}_stepsize_{sub_segment}.png'.format(segment=floor,sub_segment=step))
   except IOError:
       print("couldnt save in specific location")
       img.save('coloredpic.png')             
    
#this function recieves an n-tuple list of colors (strings) and converts them to the gradientts between them                
def create_color_palletes(colors,steps):
    pallet=[]
    fcolor=colors[0]
    for color in colors[1:]:
        pallet.append(color_gradient_section(fcolor,color,steps))
        fcolor=color
    return pallet    

#This function recieves the array for the image, the distance json, the max distance from it,and the number of colors to gradient and how many gradient stages requested.
def color_tiles(pix,distances,floors,steps,color_lst):
    
    #calculated manualy from left center to (0,0) to acheive biggest minimal distance possible.
    max_distance=2705
    
    #sectioning the image accordingly
    floorsize=max_distance/(floors) #900
    stepsize=floorsize/steps #300
    
    #creating color palletes
    pallete_for_blacklines=create_color_palletes(random_color_pallete(color_lst,floors),steps)
    pallete_for_whitebg=create_color_palletes(random_color_pallete(color_lst,floors),steps)
    
    #The coloring of the image algorithm
    h,w=distances.shape
    for py in range(h):
           for px in range(w):
            dis=distances[py][px]
            floor=math.ceil(dis/floorsize) #2
            real_floor=floor-1
            step=math.ceil((dis-(floorsize*floor))/stepsize)
            p=pix[py][px]
            if is_pixel_color(pix[py][px],(255,255,255)):
               try:   
                p[0],p[1],p[2]=pallete_for_blacklines[real_floor][step][0],pallete_for_blacklines[real_floor][step][1],pallete_for_blacklines[real_floor][step][2]
               except IndexError:
                   print("error in: coordinates- ({y},{x}), distance- {dis}, floor- {floor}, steps- {step}".format(y=py,x=px,dis=dis,floor=floor,step=step))
                   
            else:
                try: 
                    p[0],p[1],p[2]=pallete_for_whitebg[real_floor][step][0],pallete_for_whitebg[real_floor][step][1],pallete_for_whitebg[real_floor][step][2]
                except IndexError:
                    print("error in: coordinates- ({y},{x}), distance- {dis}, floor- {floor}, steps- {step}".format(y=py,x=px,dis=dis,floor=floor,step=step))
                
               
    img=Image.fromarray(pix)
    try:
        img.save('./images/impression/Impression_floorsize_{segment}_stepsize_{sub_segment}.png'.format(segment=floors,sub_segment=steps))
    except IOError:
       print("couldnt save in specific location")
       img.save('coloredpic.png')  
        
#pulls all color names from github    
def pull_colours():
    url ='https://gist.githubusercontent.com/rortian/7516084/raw/1834f5f6475b74e18c05814f8e8441aa5b2f9adc/svg-named-colors.json'
    resp=requests.get(url)
    dic=json.loads(resp.text)
    print(dic)
    return dic               

#randomizes a color list
def random_color_pallete(overall_color_list,size_of_pallete):
    pallete=[]
    for c in range(size_of_pallete+1):
        try:
            i=random.randint(0,len(overall_color_list)-1)
            pallete.append(overall_color_list[i])
        except ValueError:
            pallete.pop(i)
            c=c-1
    return pallete

              

#Creates the gradient of the lines
def gradient_for_lines(line_colors,overall_color_list):
    floors=1
    steps_between_each_floor=len(line_colors)-floors
    floor_colors=random_color_pallete(overall_color_list,floors)
    color_steps=create_color_palletes(floor_colors,steps_between_each_floor)
       
    print(len(line_colors))
    print(len(color_steps))
    return color_steps
    
   
def color_lines(pix,line_colors,overall_color_list):
    new_line_colors=gradient_for_lines(line_colors,overall_color_list)[0]
    h,w,rgb=pix.shape
    for py in range(h):
        for px in range(w):
            p=pix[py][px]
            k=line_colors.index((p[0],p[1],p[2],p[3]))
            if not is_pixel_color(p,(255,255,255,255)):
                
                try:
                    k=line_colors.index((p[0],p[1],p[2],p[3]))
                    print(k)
                    p[0],p[1],p[2]=new_line_colors[k][0],new_line_colors[k][1],new_line_colors[k][2]
                except ValueError:
                   print("error in, ",p) 
                
    img=Image.fromarray(pix)
    img.save('onlystripes.png')
    print('done')            
            
    
    
               

def placeholder():        
    with open('./json/distances.json') as f:
        dist=np.array(json.load(f))
        
    pix=np.array(Image.open('blackendpic.png'))

    colorlist=pull_colours()    
    colors_white=create_color_palletes(('white','yellow','orange','red','blue'))
    colors_black=create_color_palletes(('white','yellow','red','cornflowerblue','darkblue'))
    calculate_coloring_section(pix,dist,500,50,colors_white,colors_black)
    print(random_color_pallete(pull_colours(),5))

with open('./json/distances.json') as f:
        dist=np.array(json.load(f))
        
pix=np.array(Image.open('./images/universe/NewAmpereT_1_c1_vert_x400z10_ls1000stps2000_figsz_w40h25dpi300_density_15_linewidth4.png'))
h,w,rgb=pix.shape
jsonrunner.line_pallete_toJson(pix)

with open('./json/colors of lines.json') as f:
    line_colors=json.load(f)
            


color_lines(pix,line_colors,pull_colours())