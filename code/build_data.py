"""
MALeViC
code for generating synthetic visual scenes
and captions about objects' size

code written by:
Sandro Pezzelle
ILLC - University of Amsterdam
September 2019

usage (example):
$ python build_data.py --outputh_path ./mydata/ --task d --difficulty hard --n_images 10 --steps 5

this will generate a folder called 'd_hard_vague_all_data' containing 10 images and
2 .json files containing full annotation (scene level, object level, captions) for
scenes 0 to 4, and 5 to 9, respectively

"""

import os
import sys
import argparse

import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
from skimage.draw import circle, rectangle, polygon

import numpy as np
import scipy
import json


parser = argparse.ArgumentParser()

parser.add_argument('--output_path', default='../data/')
parser.add_argument('--task', default='d') # options: a (sup1), b (pos1), c (pos), d (set-pos); e.g. --task b
parser.add_argument('--difficulty', default='regular') # options: hard (no biggest/smallest in set), very_hard (big in set but not in scene); e.g. --difficulty hard
parser.add_argument('--shapes', default=['triangle','circle','square','rectangle'], nargs='+') # list of strings (only these shapes implemented), e.g. --shapes triangle circle
parser.add_argument('--variant', default='vague') # options: vague (k sampled from reference_k +- sigma), static (k = reference_k); e.g. --variant vague
parser.add_argument('--steps', default=1000, type=int) # number of datapoints saved in each .json file 
parser.add_argument('--n_images', default=25000, type=int) # number of total images to be generated
parser.add_argument('--start_from', default=0, type=int) # if N not 0, recap image generation from N (where N is number of images already generated)
parser.add_argument('--build_more_images', default=0, type=int) # build N more images on top of already generated ones
parser.add_argument('--reference_k', default=0.29, type=float) # ranging from 0 to 1
parser.add_argument('--reference_sigma', default=0.066, type=float) # 0.066 = +-0.2; 0.033 = +- 0.1
parser.add_argument('--colors', default=['red','blue','yellow','green','white'], nargs='+') # list of strings (only these colors implemented); e.g. --colors red blue white
parser.add_argument('--rads', default=[30,40,50,60,70,80,90,100,110,120], nargs='+') # list of integers (any integer allowed), e.g. --rads 20 40 50 90 130


# Define implemented colors
avail_colors = ['red', 'blue', 'yellow', 'green', 'white']

# Define implemented color rgb codes
red = (255, 0, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
green = (0, 128, 0)
white = (255, 255, 255)

# Define implemented shapes
avail_shapes = ['triangle', 'circle', 'square', 'rectangle']

cnt = []

def draw_shape(i,color_list,size_array,shapes_list,img):
    obj_info = []

    targ_color = np.random.randint(0, len(color_list))
    targ_color_code = eval(color_list[targ_color])
    targ_rad = np.random.randint(0, len(size_array))

    targ_shape = np.random.randint(0,len(shapes_list))
    shape_string = shapes_list[targ_shape]

    if shape_string == 'circle':
        radius = int(size_array[targ_rad]) # radius
        rr_rand = np.random.randint(0 + (radius), 1024 - (radius)) # y coord center
        cc_rand = np.random.randint(0 + (radius), 1024 - (radius)) # x coord center
        rr, cc = circle(rr_rand, cc_rand, radius)

    elif shape_string == 'square':
        radius = int(size_array[targ_rad]) # half_base
        base = radius * 2
        a = np.random.randint(0, 1024 - (base))
        b = np.random.randint(0, 1024 - (base))
        start = (a, b)
        end = (a + base-1, b + base-1)
        rr_rand = a + radius # y coord center
        cc_rand = b + radius # x coord center
        rr, cc = rectangle(start, end)

    elif shape_string == 'rectangle':
        opt = ['vert','horiz']
        radius = int(size_array[targ_rad]) # one_fourth_longer_side
        base = radius * 4
        o = np.random.randint(0,2)
        myopt = opt[o]
        if myopt == 'vert':
            a = np.random.randint(0, 1024 - (base))
            b = np.random.randint(0, 1024 - (radius))
            start = (a, b)
            end = (a + base-1, b + radius-1)
            rr_rand = a + (radius*2) # y coord center
            cc_rand = b + (radius/2) # x coord center
            rr, cc = rectangle(start, end)
        elif myopt == 'horiz':
            b = np.random.randint(0, 1024 - (base))
            a = np.random.randint(0, 1024 - (radius))
            start = (a, b)
            end = (a + radius-1, b + base-1)
            rr_rand = a + (radius/2) # y coord center
            cc_rand = b + (radius*2) # x coord center
            rr, cc = rectangle(start, end)

    elif shape_string == 'triangle':
        opt = ['vert','horiz']
        radius = int(size_array[targ_rad]) # one_fourth_longer_side
        base = radius * 4
        alt = radius * 2
        o = np.random.randint(0,2)
        myopt = opt[o]
        if myopt == 'vert':
            a = np.random.randint(0, 1024 - (alt)) # y
            b = np.random.randint(0, 1024 - (base)) # x
            rr_rand = (a+alt) # y coord center
            cc_rand = (b+alt) # x coord center
            rr, cc = polygon([a, a, a+alt-1], [b, b+base, b+alt])
        elif myopt == 'horiz':
            a = np.random.randint(0, 1024 - (base)) # y
            b = np.random.randint(0, 1024 - (alt)) # x
            rr_rand = (a+alt) # x coord center
            cc_rand = (b+alt) # y coord center
            rr, cc = polygon([a, a+alt, a+base], [b, b+alt, b])



    img[rr, cc, :] = targ_color_code  # red = (255, 0, 0)
    mask = np.zeros((1024, 1024))
    mask[rr, cc] = 1
    real_area = int(np.count_nonzero(mask.flatten()))

    obj_info.append(str(i))
    obj_info.append(str(rr_rand))
    obj_info.append(str(cc_rand))
    obj_info.append(color_list[targ_color])
    obj_info.append(str(shape_string))
    obj_info.append(str(radius))
    obj_info.append(str(real_area))

    return mask, radius, real_area, obj_info


def main(args):
  v = ''
  if len(args.shapes) < 4:
     for el in args.shapes:
         v= v + '_'+str(el)
  else:
       v = v
  if len(args.colors) < 5:
     for el in args.colors:
         v= v + '_'+str(el)
  else:
       v = v
  if args.rads != [30,40,50,60,70,80,90,100,110,120]:
     for el in args.rads:
         v= v + '_'+str(el)
  else:
       v = v

  if args.task == 'a' or args.task == 'b':
     if args.difficulty != 'regular':
        uptask = str(str(args.task)+'_'+str(args.difficulty)) # e.g. 'b_hard' 
     else: 
         uptask = str(args.task) # e.g. 'b' 

  else:
     if args.difficulty != 'regular':
        uptask = str(str(args.task)+'_'+str(args.difficulty)) # e.g. 'd_hard' 
     else:
         uptask = str(args.task) # e.g. 'b'
  
  # Define number of annotation files
  for i in range(args.n_images):
      if i%int(args.steps) == 0:
         cnt.append(int(i))
  
  print('Generating %s images for %s task in %s setting...' % (args.n_images, uptask, args.variant))
  
  # Create output folder where to save images and annotations
  if args.task == 'a':
     path = str(args.output_path)+str(uptask)+str(v)+'_all_data/' # a_all_data
     if not os.path.exists(path):
        os.mkdir(path)
        print('Create new directory')
     else:
         print('Appending data into existing directory')
  else:
      path = str(args.output_path)+str(uptask)+'_'+str(args.variant)+str(v)+'_all_data/' # d_hard_vague_all_data
      if not os.path.exists(path):
         os.mkdir(path)
         print('Create new directory')
      else:
          print('Appending data into existing directory')

  for c in args.colors:
      if c not in avail_colors:
         print('Color not implemented. Available colors: red, blue, yellow, green, white')
         exit(0)
  
  for c in args.shapes:      
      if c not in avail_shapes:
         print('Shape not implemented. Available shapes: triangle, circle, square, rectangle')
         exit(0)

  # Make arguments local
  var = args.variant

  build_dataset(args.steps,uptask,var,path,args.rads,args.reference_k,args.reference_sigma)

def build_dataset(steps,task,variant,folder,radss,ref_k,ref_sd):
  # Create .json file with annotations
  if task == 'a' or task == 'b' or task == 'b_hard':
     ccnt = []
     if args.start_from == 0 and args.build_more_images == 0:
        sub = int(int(args.n_images)/int(len(args.shapes)))
        if int(args.n_images)%int(len(args.shapes)) == 0:
           pass
        else:
            print('You can only build N of images that can be divided by number of --shapes, i.e., %s' % len(args.shapes))
            exit(0)
        subcount, cidx = 0, 0
        print('Start generation from scratch')
     elif args.start_from == 0 and args.build_more_images != 0: # e.g. 0, 2000
          print('Specify the starting point using --start_from')
          exit(0)
     elif args.start_from != 0 and args.build_more_images != 0: # e.g. 25000, 2000
          print('Build %s extra images' % (args.build_more_images))
          n_images = args.build_more_images # e.g. 2000
          sub = int(int(n_images)/int(len(args.shapes)))
          if int(n_images)%int(len(args.shapes)) == 0:
             pass
          else:
              print('You can only build N of images that can be divided by number of --shapes, i.e., %s' % len(args.shapes))
              exit(0)
          subcount, cidx = 0, 0
          for i in range(int(n_images)):
              if i%int(args.steps) == 0:
                 ii = i+int(args.start_from) # 25000,26000
                 ccnt.append(int(ii))
     else:
         if int(args.start_from) < int(args.n_images) and int(args.start_from)%int(args.steps) == 0:
            print('Resume generation from %s out of %s images' % (args.start_from,args.n_images))
            pass
         else:
             print('You can only resume from numbers that can be divided by number of --steps, i.e. %s ' % len(args.steps))
             exit(0)

         tbb_images = int(args.n_images) - int(args.start_from) # 18000 = 25000 - 7000 
         sub = int(int(args.n_images)/int(len(args.shapes))) # 6250       
         if int(args.start_from) < sub:
            subcount, cidx = int(args.start_from), 0
            for i in range(args.n_images):
                if i%int(args.steps) == 0:
                   ccnt.append(int(i))
            ii = ccnt.index(int(args.start_from))
            ccnt = ccnt[ii:]
         elif int(args.start_from) >= sub and int(args.start_from) < sub*2:
              subcount, cidx = int(args.start_from), 1
              for i in range(args.n_images):
                  if i%int(args.steps) == 0:
                     ccnt.append(int(i))
              ii = ccnt.index(int(args.start_from))
              ccnt = ccnt[ii:]
         elif int(args.start_from) >= sub*2 and int(args.start_from) < sub*3:
              subcount, cidx = int(args.start_from), 2
              for i in range(args.n_images):
                  if i%int(args.steps) == 0:
                     ccnt.append(int(i))
              ii = ccnt.index(int(args.start_from))
              ccnt = ccnt[ii:]
         elif int(args.start_from) >= sub*3 and int(args.start_from) < sub*4:
              subcount, cidx = int(args.start_from), 3
              for i in range(args.n_images):
                  if i%int(args.steps) == 0:
                     ccnt.append(int(i))
              ii = ccnt.index(int(args.start_from))
              ccnt = ccnt[ii:]
  else: # c, c_hard, d, d_hard, d_very_hard
       ccnt = []
       if args.start_from == 0 and args.build_more_images == 0:
          print('Start generation from scratch')
       elif args.start_from == 0 and args.build_more_images != 0: # e.g. 0, 2000
            print('Specify the starting point using --start_from')
            exit(0)
       elif args.start_from != 0 and args.build_more_images != 0: # e.g. 25000, 2000
            print('Build %s extra images' % (args.build_more_images))
            n_images = args.build_more_images # e.g. 2000
            if int(n_images) < int(args.steps):
               print('Set --build_extra_images to be higher or equal to --steps')
               exit(0)
            for i in range(int(n_images)):
                if i%int(args.steps) == 0:
                   ii = i+int(args.start_from) # 25000,26000
                   ccnt.append(int(ii))
       else:
           if int(args.start_from) < int(args.n_images) and int(args.start_from)%int(args.steps) == 0:
              print('Resume generation from %s out of %s images' % (args.start_from,args.n_images))
              pass
           else:
               print('You can only resume from numbers that can be divided by number of --steps, i.e. %s ' % (args.steps))
               exit(0) 
           for i in range(args.n_images):
               if i%int(args.steps) == 0:
                  ccnt.append(int(i))
           ii = ccnt.index(int(args.start_from))
           ccnt = ccnt[ii:]
   
  if not ccnt:
     pass
  else:
      del cnt[:]
      for j in ccnt:
          cnt.append(j)

  for init in cnt:
      data = {}
      count = int(init)
      strcount = str(count)
      pt = str(folder+'annotations_'+strcount+'.json')
      outfile = open(pt, 'w')


      # Iterate for N times
      for iter in range(1000000):
          condition = []
          print(iter, count)
          
          # Define number of objects in scene
          n_targ_objects = np.random.randint(5,10)
          fig, ax1 = plt.subplots(ncols=1, nrows=1)
          
          # Define image size
          img = np.zeros((1024, 1024, 3), dtype=np.double)
          if task == 'a' or task == 'b' or task == 'b_hard' or task == 'c' or task == 'c_hard':
             areas, info = [], []
          elif task == 'a_hard' or task == 'd' or task == 'd_hard' or task == 'd_very_hard':
               areas, info, areas_circle, areas_triangle, areas_square, areas_rectangle = [], [], [], [], [], []

          info_d = []
          orig = np.zeros((1024,1024)).flatten()
          radiuss = []

          if task == 'a' or task == 'b' or task == 'b_hard':
             tcc = []
             tcc.append(str(args.shapes[cidx]))

          else:
               tcc = args.shapes
          
          # Draw objects
          for i in range(n_targ_objects):
              obj_info_d = {}
              mask, radius, real_area, obj_info = draw_shape(i,args.colors,args.rads,tcc,img)
              info.append(obj_info)
              radiuss.append(radius)
              masked = mask.flatten()
              rp = orig[masked>= 1]

              # Check if objects overlap with each other 
              if np.count_nonzero(rp) == 0:
                 pass
              else:
                  condition.append('overlap')

              # Make lists with object areas
              if task == 'a' or task == 'b' or task == 'b_hard' or task == 'c' or task == 'c_hard':
                 areas.append(real_area)
              elif task == 'a_hard' or task == 'd' or task == 'd_hard' or task == 'd_very_hard':
                   targetlist = eval(str('areas_'+str(obj_info[4])))
                   targetlist.append(real_area)
                   areas.append(real_area)

              orig[masked >= 1] = 1
          
          # Leave the loop if there are overlapping objects
          if len(condition) > 0:
             continue
        
          # Compute average size objects in scene/set
          if task == 'a' or task == 'b' or task == 'b_hard' or task == 'c' or task == 'c_hard':
             avg_area = np.sum(areas)/len(areas)
          else:
               avg_area = np.sum(areas)/len(areas)
               if len(areas_circle) != 0:
                  avg_area_circle = np.sum(areas_circle)/len(areas_circle)
               if len(areas_square) != 0:
                  avg_area_square = np.sum(areas_square)/len(areas_square)
               if len(areas_rectangle) != 0:
                  avg_area_rectangle = np.sum(areas_rectangle)/len(areas_rectangle)
               if len(areas_triangle) != 0:
                  avg_area_triangle = np.sum(areas_triangle)/len(areas_triangle)
          maxrad = int(np.max(radiuss))
          minrad = int(np.min(radiuss))

          if np.max(areas) == np.min(areas):
              print('Aborted because all objects have same size')
              continue

          # Define object size by means of a static or vague (random sample from normal distribution centered on mu) threshold 
          if task == 'a' or task == 'a_hard':
             pass
          elif task == 'b' or task == 'b_hard' or task == 'c' or task == 'c_hard':
               ref_thresh = np.max(areas) - ref_k * (np.max(areas) - np.min(areas))
               if variant == 'static':
                  thresh = np.max(areas) - ref_k * (np.max(areas) - np.min(areas))
               elif variant == 'vague':
                    mu, sigma = ref_k, ref_sd                  
                    s = np.random.normal(mu, sigma, 1)
                    thresh = np.max(areas) - s * (np.max(areas) - np.min(areas))
               else:
                    print('Variant not implemented. Options: vague, static')
                    exit(0)
          else:
               if variant == 'static':
                  ref_thresh = np.max(areas) - ref_k * (np.max(areas) - np.min(areas))
                  if len(areas_circle) != 0:
                     thresh_c = np.max(areas_circle) - ref_k * (np.max(areas_circle) - np.min(areas_circle))
                  if len(areas_square) != 0:
                     thresh_s = np.max(areas_square) - ref_k * (np.max(areas_square) - np.min(areas_square))
                  if len(areas_rectangle) != 0:
                     thresh_r = np.max(areas_rectangle) - ref_k * (np.max(areas_rectangle) - np.min(areas_rectangle))
                  if len(areas_triangle) != 0:
                     thresh_t = np.max(areas_triangle) - ref_k * (np.max(areas_triangle) - np.min(areas_triangle))
               elif variant == 'vague':
                    mu, sigma = ref_k, ref_sd
                    s = np.random.normal(mu, sigma, 1)
                    if len(areas_circle) != 0:
                       thresh_c = np.max(areas_circle) - s * (np.max(areas_circle) - np.min(areas_circle))
                       thresh_c_ref = np.max(areas_circle) - mu * (np.max(areas_circle) - np.min(areas_circle))
                    if len(areas_square) != 0:
                       thresh_s = np.max(areas_square) - s * (np.max(areas_square) - np.min(areas_square))
                       thresh_s_ref = np.max(areas_square) - mu * (np.max(areas_square) - np.min(areas_square))
                    if len(areas_rectangle) != 0:
                       thresh_r = np.max(areas_rectangle) - s * (np.max(areas_rectangle) - np.min(areas_rectangle))
                       thresh_r_ref = np.max(areas_rectangle) - mu * (np.max(areas_rectangle) - np.min(areas_rectangle))
                    if len(areas_triangle) != 0:
                       thresh_t = np.max(areas_triangle) - s * (np.max(areas_triangle) - np.min(areas_triangle))                 
                       thresh_t_ref = np.max(areas_triangle) - mu * (np.max(areas_triangle) - np.min(areas_triangle))
                    ref_thresh = np.max(areas) - s * (np.max(areas) - np.min(areas)) # this is for d_very_hard
               else:
                    print('Variant not implemented. Options: vague, static')
                    exit(0)

          # Get object aread and make list with colors in scene
          new_info_d = []
          n_colors = []
          cb, cs = 0, 0
          sqb,trb,reb,cib = 0,0,0,0 
          sqs,trs,res,cis = 0,0,0,0 
          for obj in info: # obj is a list
              new_obj_dct = {}
              obj_area = int(obj[6])
              if str(obj[3]) not in n_colors:
                  n_colors.append(obj[3])

              # Define object size label, probability, and distance from threshold
              if task == 'a':
                 if int(obj[5]) == maxrad:
                    cb += 1
                    size = 'biggest'
                    obj.append(size)
                 elif int(obj[5]) == minrad:
                      cs += 1
                      size = 'smallest'
                      obj.append(size)
                 else:
                      size = 'NA'
                      obj.append(size)

              elif task == 'a_hard':
                   acode = eval('areas_'+str(obj[4]))
                   if obj_area == int(np.max(acode)):
                      if str(obj[4]) == 'circle':
                         cib +=1
                      elif str(obj[4]) == 'square':
                         sqb +=1
                      elif str(obj[4]) == 'rectangle':
                         reb += 1
                      elif str(obj[4]) == 'triangle':
                         trb += 1

                      if len(acode) >2:
                         size = 'biggest'
                         obj.append(size)
                      else:
                          size = 'NA'
                          obj.append(size)
                      if obj_area == int(np.max(areas)):
                         obj.append('same')
                      else:
                           obj.append('different')
                   elif obj_area == int(np.min(acode)):
                      if str(obj[4]) == 'circle':
                         cis +=1
                      elif str(obj[4]) == 'square':
                         sqs +=1
                      elif str(obj[4]) == 'rectangle':
                         res += 1
                      elif str(obj[4]) == 'triangle':
                         trs += 1
                      if len(acode) >2:
                         size = 'smallest'
                         obj.append(size)
                      else:
                          size = 'NA'
                          obj.append(size)
                      if obj_area == int(np.min(areas)):
                         obj.append('same')
                      else:
                          obj.append('different')
                   else:
                       size = 'NA'
                       obj.append(size)
                       obj.append('nan')

              elif task == 'b' or task == 'b_hard' or task == 'c' or task == 'c_hard':
                 if obj_area > int(thresh):
                    obj_area_n = (obj_area - np.min(areas)) / (np.max(areas) - np.min(areas))
                    thresh_n = (thresh - np.min(areas)) / (np.max(areas) - np.min(areas))
                    prob = (1 + scipy.special.erf(((obj_area - thresh)*0.00001) / (0.05 * np.sqrt(2)))) / 2
                    thresh_dist = obj_area_n - thresh_n
                    size = 'big' 
                    obj.append(size)
                    probab = np.round(prob,decimals=4)
                    obj.append(probab[0])
                    dstth = np.round(thresh_dist,decimals=4)
                    obj.append(dstth[0])
                    ss = np.round(s,decimals=4)
                    obj.append(ss[0])
                    if obj_area > ref_thresh:
                       obj.append('same')
                    else:
                         obj.append('different') 
                 else:
                      obj_area_n = (obj_area - np.min(areas)) / (np.max(areas) - np.min(areas))
                      thresh_n = (thresh - np.min(areas)) / (np.max(areas) - np.min(areas))
                      prob = 1 - ((1 + scipy.special.erf(((obj_area - thresh)*0.00001) / (0.05 * np.sqrt(2)))) / 2)
                      thresh_dist = thresh_n - obj_area_n
                      size = 'small'
                      obj.append(size)
                      probab = np.round(prob,decimals=4)
                      obj.append(probab[0])
                      dstth = np.round(thresh_dist,decimals=4)
                      obj.append(dstth[0])
                      ss = np.round(s,decimals=4)
                      obj.append(ss[0])
                      if obj_area <= ref_thresh:
                         obj.append('same')
                      else:
                           obj.append('different')        
              else:
                   tcode = eval('thresh_'+str(obj[4])[0])
                   acode = eval('areas_'+str(obj[4]))
                   if obj_area > int(tcode):
                      obj_area_n = (obj_area - np.min(acode)) / (np.max(acode) - np.min(acode))
                      thresh_n = (tcode - np.min(acode)) / (np.max(acode) - np.min(acode))
                      prob = (1 + scipy.special.erf(((obj_area - tcode)*0.00001) / (0.05 * np.sqrt(2)))) / 2
                      thresh_dist = obj_area_n - thresh_n
                      size = 'big'
                      obj.append(size)
                      probab = np.round(prob,decimals=4)
                      obj.append(probab[0])
                      dstth = np.round(thresh_dist,decimals=4)
                      obj.append(dstth[0])
                      ss = np.round(s,decimals=4)
                      obj.append(ss[0])
                      if obj_area > int(eval('thresh_'+str(obj[4])[0]+'_ref')):
                         obj.append('same')
                      else:
                           obj.append('different')
                   else:
                      obj_area_n = (obj_area - np.min(acode)) / (np.max(acode) - np.min(acode))
                      thresh_n = (tcode - np.min(acode)) / (np.max(acode) - np.min(acode))
                      prob = 1 - ((1 + scipy.special.erf(((obj_area - tcode)*0.00001) / (0.05 * np.sqrt(2)))) / 2)
                      thresh_dist = thresh_n - obj_area_n
                      size = 'small'
                      obj.append(size)
                      probab = np.round(prob,decimals=4)
                      obj.append(probab[0])
                      dstth = np.round(thresh_dist,decimals=4)
                      obj.append(dstth[0])
                      ss = np.round(s,decimals=4)
                      obj.append(ss[0])
                      if obj_area <= int(eval('thresh_'+str(obj[4])[0]+'_ref')):
                         obj.append('same')
                      else:
                           obj.append('different')

              # Make dictionary with information about each object
              if task == 'a':
                 new_obj_d = {
                     'object_id': str(obj[0]),
                     'rr': str(obj[1]),
                     'cc': str(obj[2]),
                     'color': str(obj[3]),
                     'shape': str(obj[4]),
                     'radius': str(obj[5]),
                     'area': str(obj[6]),
                     'size': str(obj[7]),
                 }

                 new_info_d.append(new_obj_d)

              elif task == 'a_hard':
                   new_obj_d = {
                       'object_id': str(obj[0]),
                       'rr': str(obj[1]),
                       'cc': str(obj[2]),
                       'color': str(obj[3]),
                       'shape': str(obj[4]),
                       'radius': str(obj[5]),
                       'area': str(obj[6]),
                       'size': str(obj[7]),
                       'size_scene': str(obj[8])
                   }

                   new_info_d.append(new_obj_d)

              else:            
                   new_obj_d = {
                     'object_id': str(obj[0]),
                     'rr': str(obj[1]),
                     'cc': str(obj[2]),
                     'color': str(obj[3]),
                     'shape': str(obj[4]),
                     'radius': str(obj[5]),
                     'area': str(obj[6]),
                     'size': str(obj[7]),
                     'prob': str(obj[8]),
                     'thresh_dist': str(obj[9]),
                     'k': str(obj[10]),
                     'vagueness': str(obj[11])
                   }

                   new_info_d.append(new_obj_d)

          # Ensure that there is only one biggest and one smallest object
          if task == 'a':
             if cb == 1 and cs == 1:
                pass
             else:
                 continue

          elif task == 'a_hard':
             if cib == 1 and cis == 1 and len(areas_circle) >2:
                pass
             elif trb == 1 and trs ==1 and len(areas_triangle) >2:
                pass
             elif reb == 1 and res == 1 and len(areas_rectangle) >2:
                pass
             elif sqb == 1 and sqs == 1 and len(areas_square) >2:
                pass
             else:
                 continue

          # Append information regarding scene
          nm = str(count)
          pathim = str(str(nm)+'.png')
          data[count] = []
          data[count].append({
              'image_id': str(nm),
              'image_url': str(pathim),
              'n_objects': str(len(areas)),
              'n_colors': str(len(n_colors)),
              'total_area_px': str(np.sum(areas)),
              'avg_area_px': str(np.round(avg_area, decimals=4)),
              'min_area': str(np.min(areas)),
              'max_area': str(np.max(areas)),
              'min_radius': str(minrad),
              'max_radius': str(maxrad)
          })

          # Append information regarding all objects 
          data[count].append({
              'objects': new_info_d
          })
  
          # Check unique-color objects in scene/set
          candidates = []
          for obj in info:
              a = str(obj[3])
              b = str(obj[4])
              if task == 'a' or task == 'b' or task == 'b_hard':
                 candidates.append(a)
              else:
                   candidates.append(str(a+'_'+b))
          fd = {i:candidates.count(i) for i in set(candidates)}

          # Check presence of at least one callable object
          shortlist = []
          for k, v in fd.items():
              if v == 1:
                 shortlist.append(k)
          if len(shortlist) < 1:
              continue
          
          for el in shortlist: # el = 'red' or 'red_circle'
              cpt, elsh = [], []
              if task == 'a' or task == 'b' or task == 'b_hard':
                 elcol = el
                 elsh.append(b)
              else:
                   elcol = str(el.split('_')[0])
                   elsh.append(str(el.split('_')[1]))

              for obj in info:
                  if task == 'a' or task == 'b' or task == 'b_hard' or task == 'c' or task == 'c_hard':
                     tt = areas
                     maxx = np.max(tt)
                     minn = np.min(tt)
                  elif task == 'd' or task == 'a_hard':
                       myvar = str(obj[4])
                       tt = eval('areas_'+str(myvar))
                       maxx = np.max(areas)
                       minn = np.min(areas)
                  else:
                       myvar = str(obj[4])
                       tt = eval('areas_'+str(myvar))
                       maxx = np.max(tt)
                       minn = np.min(tt)
                  
                  # Generate captions
                  if task == 'a':
                     if obj[3] == elcol and obj[4] in elsh and int(obj[5]) != radss[0] and int(obj[5]) != radss[-1]:
                        caption_true, caption_false = {}, {}
                        st_true, st_false, captions = [], [], []
                        if str(obj[7]) is 'smallest':
                           false = 'biggest'
                           cpt.append('1')
                        elif str(obj[7]) is 'biggest':
                            false = 'smallest'
                            cpt.append('1')
                        else:
                            continue
                        st = str('The '+obj[3]+' '+obj[4]+' is the '+obj[7]+' '+obj[4])
                        st_false = str('The '+obj[3]+' '+obj[4]+' is the '+false+' '+obj[4])
                        caption_true = {
                            'caption_true': str(st)
                        }
                        captions.append(caption_true)
                        caption_false = {
                            'caption_false': str(st_false)
                        }
                        captions.append(caption_false)
                        data[count].append({
                           'captions': captions
                        })

                  elif task == 'a_hard':
                       if obj[3] == elcol and obj[4] in elsh and int(obj[5]) != radss[0] and int(obj[5]) != radss[-1] and int(obj[6]) != maxx and int(obj[6]) != minn and len(tt) > 2 and eval(str(obj[4][:2])+'b') ==1 and eval(str(obj[4][:2])+'s') ==1: # at least 2 objects in the set
                          caption_true, caption_false = {}, {}
                          st_true, st_false, captions = [], [], []
                          if str(obj[7]) is 'smallest':
                             false = 'biggest'
                             cpt.append('1')
                          elif str(obj[7]) is 'biggest':
                              false = 'smallest'
                              cpt.append('1')
                          else:
                              continue
                          st = str('The '+obj[3]+' '+obj[4]+' is the '+obj[7]+' '+obj[4])
                          st_false = str('The '+obj[3]+' '+obj[4]+' is the '+false+' '+obj[4])
                          caption_true = {
                              'caption_true': str(st),
                              'size_scene': str(obj[8])
                          }
                          captions.append(caption_true)
                          caption_false = {
                              'caption_false': str(st_false),
                              'size_scene': str(obj[8])
                          }
                          captions.append(caption_false)
                          data[count].append({
                             'captions': captions
                          })


                  elif task == 'b' or task == 'c':
                       if obj[3] == elcol and obj[4] in elsh and int(obj[5]) != radss[0] and int(obj[5]) != radss[-1] and str(obj[9]) != 'nan':
                          caption_true, caption_false = {}, {}
                          st_true, st_false, captions = [], [], []
                          cpt.append('1')

                          if str(obj[7]) is 'small':
                             false = 'big'
                          else:
                              false = 'small'
                          prob_false = np.round((1 - obj[8]),decimals=4)

                          if task == 'b':
                             st = str('The '+obj[3]+' '+obj[4]+' is a '+obj[7]+' '+obj[4])
                             st_false = str('The '+obj[3]+' '+obj[4]+' is a '+false+' '+obj[4])
                          elif task == 'c':
                               st = str('The '+obj[3]+' '+obj[4]+' is a '+obj[7]+' object')
                               st_false = str('The '+obj[3]+' '+obj[4]+' is a '+false+' object')

                          caption_true = {
                               'caption_true': str(st),
                               'prob_RH_R_true': str(obj[8]),
                               'dist_from_thresh:': str(obj[9]),
                               'k': str(obj[10]),
                               'vagueness': str(obj[11])
                          }
                          captions.append(caption_true)
                          caption_false = {
                               'caption_false': str(st_false),
                               'prob_RH_R_false': str(prob_false),
                               'dist_from_thresh': str(obj[9]),
                               'k': str(obj[10]),
                               'vagueness': str(obj[11])
                          }

                          captions.append(caption_false)
                          data[count].append({
                               'captions': captions
                          })

                  elif task == 'b_hard' or task == 'c_hard' or task == 'd' or task == 'd_hard':
                       if obj[3] == elcol and obj[4] in elsh and int(obj[5]) != radss[0] and int(obj[5]) != radss[-1] and str(obj[9]) != 'nan' and int(obj[6]) != maxx and int(obj[6]) != minn and len(tt) > 2: # at least 2 objects in the set
                          caption_true, caption_false = {}, {}
                          st_true, st_false, captions = [], [], []
                          cpt.append('1')

                          if str(obj[7]) is 'small':
                             false = 'big'
                          else:
                               false = 'small'
                          prob_false = np.round((1 - obj[8]),decimals=4) #todo: doublecheck!

                          if task == 'd' or task == 'b_hard' or task == 'd_hard':
                             st = str('The '+obj[3]+' '+obj[4]+' is a '+obj[7]+' '+obj[4])
                             st_false = str('The '+obj[3]+' '+obj[4]+' is a '+false+' '+obj[4])
                          else:
                              st = str('The '+obj[3]+' '+obj[4]+' is a '+obj[7]+' object')
                              st_false = str('The '+obj[3]+' '+obj[4]+' is a '+false+' object')
                          caption_true = {
                              'caption_true': str(st),
                              'prob_RH_R_true': str(obj[8]),
                              'dist_from_thresh:': str(obj[9]),
                              'k': str(obj[10]),
                              'vagueness': str(obj[11])
                          }
                          captions.append(caption_true)
                          caption_false = {
                              'caption_false': str(st_false),
                              'prob_RH_R_false': str(prob_false),
                              'dist_from_thresh': str(obj[9]),
                              'k': str(obj[10]),
                              'vagueness': str(obj[11])
                          }
                          captions.append(caption_false)
                          data[count].append({
                              'captions': captions
                          })

                  elif task == 'd_very_hard':
                       if obj[3] == elcol and obj[4] in elsh and int(obj[5]) != radss[0] and int(obj[5]) != radss[-1] and str(obj[9]) != 'nan' and int(obj[6]) != maxx and int(obj[6]) != minn and len(tt) > 2 and obj[7] == 'small' and int(obj[6]) > ref_thresh:
                          caption_true, caption_false = {}, {}
                          st_true, st_false, captions = [], [], []
                          cpt.append('1')
                          false = 'big'
                          prob_false = np.round((1 - obj[8]),decimals=4)
                          st = str('The '+obj[3]+' '+obj[4]+' is a '+obj[7]+' '+obj[4])
                          st_false = str('The '+obj[3]+' '+obj[4]+' is a '+false+' '+obj[4])
                          caption_true = {
                              'caption_true': str(st),
                              'prob_RH_R_true': str(obj[8]),
                              'dist_from_thresh:': str(obj[9]),
                              'k': str(obj[10]),
                              'vagueness': str(obj[11])
                          }
                          captions.append(caption_true)
                          caption_false = {
                              'caption_false': str(st_false),
                              'prob_RH_R_false': str(prob_false),
                              'dist_from_thresh': str(obj[9]),
                              'k': str(obj[10]),
                              'vagueness': str(obj[11])
                          }
                          captions.append(caption_false)
                          data[count].append({
                              'captions': captions
                          })

                       elif obj[3] == elcol and obj[4] in elsh and int(obj[5]) != args.rads[0] and int(obj[5]) != args.rads[-1] and str(obj[9]) != 'nan' and int(obj[6]) != maxx and int(obj[6]) != minn and len(tt) > 2 and obj[7] == 'big' and int(obj[6]) < ref_thresh:
                            caption_true, caption_false = {}, {}
                            st_true, st_false, captions = [], [], []
                            cpt.append('1')
                            false = 'small'
                             
                            prob_false = np.round((1 - obj[8]),decimals=4)
                            st = str('The '+obj[3]+' '+obj[4]+' is a '+obj[7]+' '+obj[4])
                            st_false = str('The '+obj[3]+' '+obj[4]+' is a '+false+' '+obj[4])
                            caption_true = {
                                'caption_true': str(st),
                                'prob_RH_R_true': str(obj[8]),
                                'dist_from_thresh:': str(obj[9]),
                                'k': str(obj[10]),
                                'vagueness': str(obj[11])
                            }
                            captions.append(caption_true)
                            caption_false = {
                                'caption_false': str(st_false),
                                'prob_RH_R_false': str(prob_false),
                                'dist_from_thresh': str(obj[9]),
                                'k': str(obj[10]),
                                'vagueness': str(obj[11])
                            }
                            captions.append(caption_false)
                            data[count].append({
                                'captions': captions
                            })

          if len(cpt) > 0:

              # Save image .png
              ax1.imshow(img)
              plt.axis('off')
              ax1.axes.get_xaxis().set_visible(False)
              ax1.axes.get_yaxis().set_visible(False)
 
              path = str(folder+pathim)
              plt.savefig(path, bbox_inches='tight', pad_inches = 0, dpi=400)
              plt.close('all')

              if task == 'a' or task == 'b' or task == 'b_hard':
                 subcount += 1
                 if subcount%int(sub) == 0:
                    cidx += 1

              count += 1
              if count != init and count%int(steps) == 0:
                  break
      
      json.dump(data, outfile)
      outfile.close()

if __name__ == '__main__':
  args = parser.parse_args()
  main(args)

