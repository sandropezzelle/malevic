"""
MALeViC
code for extracting balanced datasets
from generated scenes and annotations

code written by:
Sandro Pezzelle
ILLC - University of Amsterdam
September 2019

usage (example):
$ python extract_dataset.py --input_path ./mydata/ --outputh_path ./mydataset/ --task d --cases_per_class 50
Note that, by default, there are 80 classes (4 shapes * 5 colors * 2 sizes * 2 GTs)

this will generate a folder called 'd_hard_vague_dataset' containing 3 .json files: 
'train.json' (3200 datapoints), 'val.json' (400), and 'test.json' (400)

Note: if --difficulty is set to hard, then only 'val.json' and 'test.json' will be built

TO-DO:
- define automatically cases_per_class based on size on train/val/test set

"""

import os
import sys
import argparse
import glob
import shutil

import random
from random import shuffle

import json
from pprint import pprint


parser = argparse.ArgumentParser()

parser.add_argument('--input_path', default='../data/') # directory containing scenes and .json files
parser.add_argument('--output_path', default='../data/') # directory where to save the dataset
parser.add_argument('--task', default='d') # options: a (sup1), b (pos1), c (pos), d (set-pos); e.g. --task b
parser.add_argument('--difficulty', default='regular') # options: hard (no biggest/smallest in set), very_hard (big in set but not in scene); e.g. --difficulty hard
parser.add_argument('--variant', default='vague') # options: vague (k sampled from reference_k +- sigma), static (k = reference_k); e.g. --variant vague
parser.add_argument('--shapes', default=['triangle','circle','square','rectangle'], nargs='+') # list of strings (only these shapes implemented), e.g. --shapes triangle circle
parser.add_argument('--colors', default=['red','blue','yellow','green','white'], nargs='+') # list of strings (only these colors implemented); e.g. --colors red blue white
parser.add_argument('--cases_per_class', default=250, type=int) # a, b, c, d: 250; hard, very_hard: 50
parser.add_argument('--rads', default=[30,40,50,60,70,80,90,100,110,120], nargs='+') # list of integers (any integer allowed), e.g. --rads 20 40 50 90 130


# Define implemented colors, shapes, sizes, ground-truth answers
avail_colors = ['red', 'blue', 'yellow', 'green', 'white']
avail_shapes = ['triangle', 'circle', 'square', 'rectangle']
avail_sizes = []
avail_gts = ['true','false']

json_list = []
dct,data = {},{}


def main(args):
  alt_shapes, alt_colors = [], []
  v = ''
  if len(args.shapes) < 4:
     for el in args.shapes:
         v= v + '_'+str(el)
         alt_shapes.append(el)
  else:
       v = v
       alt_shapes = avail_shapes
  if len(args.colors) < 5:
     for el in args.colors:
         v= v + '_'+str(el)
         alt_colors.append(el)
  else:
       v = v
       alt_colors = avail_colors
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
  
  # Create output folder where to save balanced datasets
  if args.task == 'a':
     avail_sizes.append('biggest')
     avail_sizes.append('smallest')
     path_to_json = str(args.input_path)+str(uptask)+str(v)+'_all_data/' # input
     print(path_to_json)
     if not os.path.exists(path_to_json):
        print('Data does not exist. Built it first')
        exit(0)
     json_pattern = os.path.join(path_to_json,'*.json')
     file_list = glob.glob(json_pattern)
     for file in file_list:
         json_list.append(file)
     png_pattern = os.path.join(path_to_json,'*.png')
     png = glob.glob(png_pattern)
     n_images = int(len(png))
     print('Building %s dataset by extracting %s cases per class from %s images' % (uptask, args.cases_per_class,n_images))
     path = str(args.output_path)+str(uptask)+str(v)+'_dataset/' # e.g. a_dataset
     if not os.path.exists(path):
        os.mkdir(path)
        print('Create new directory')
     else:
         print('Appending data into existing directory')
  else:
      avail_sizes.append('big')
      avail_sizes.append('small')
      path_to_json = str(args.input_path)+str(uptask)+'_'+str(args.variant)+str(v)+'_all_data/'
      print(path_to_json)
      if not os.path.exists(path_to_json):
         print('Data does not exist. Built it first')
         exit(0)
      json_pattern = os.path.join(path_to_json,'*.json')
      file_list = glob.glob(json_pattern)
      for file in file_list:
          json_list.append(file)
      png_pattern = os.path.join(path_to_json,'*.png')
      png = glob.glob(png_pattern)
      n_images = int(len(png))
      print('Building %s dataset by extracting %s cases per class from %s images' % (uptask, args.cases_per_class,n_images))
      path = str(args.output_path)+str(uptask)+'_'+str(args.variant)+str(v)+'_dataset/' # e.g. d_hard_vague_dataset
      if not os.path.exists(path):
         os.mkdir(path)
         print('Create new directory')
      else:
          print('Appending data into existing directory')

  get_balanced_dataset(png,args.cases_per_class,path_to_json,path,uptask,alt_shapes,alt_colors)


def store_in_list(id, caption, truth_value, dictionary):
    strn = str(caption.split()[1])+'_'+str(caption.split()[5])+'_'+str(caption.split()[2])+'_'+str(truth_value)
    mylist = dictionary[strn]
    mylist.append(id)


def get_balanced_dataset(mypng,n_cases_per_class,source_path,out_path,uptask,ashapes,acolors):
  for f in json_list:
      anns = open(f, 'r')
      data.update(json.load(anns))

  if not ashapes:
     pass
  else:
      avail_shapes = ashapes
  if not acolors:
     pass
  else:
      avail_colors = acolors
  classes = 0
  for i in avail_colors:
      a = str(i)+'_'
      for j in avail_sizes:
          b = a+str(j)+'_'
          for q in avail_shapes:
              c = b+str(q)+'_'
              for y in avail_gts:
                  d = c+str(y)
                  dct[d] = []
                  classes += 1
  print('number of classes %s' % classes)
  print('number of total datapoints in the dataset %s' % (classes*n_cases_per_class))

  for ell in mypng:
      name = ell.split('/')[-1]
      myi = str(name.split('.')[0])
      if len(data[myi]) > 2:
         n_capt = len(data[myi]) - 2
         for j in range(n_capt):
             store_in_list(data[myi][0]['image_id'],data[myi][j+2]['captions'][0]['caption_true'],avail_gts[0],dct)
             store_in_list(data[myi][0]['image_id'],data[myi][j+2]['captions'][1]['caption_false'],avail_gts[1],dct)
      else:
          continue


  min_list = min([len(ls) for ls in dct.values()])
  print('Number images in least-represented case:',min_list)

  helper = [(key, len(dct[key])) for key in dct.keys()]
  helper.sort(key=lambda x: x[1])
  print(helper)

  #here below we select only one caption (either true or false) per image
  used = []
  for el in helper:
      for k,v in dct.items():
          if  k == el[0]:
              count = 0
              shuffle(v)
              for i in v:
                  if count < n_cases_per_class:
                      if i not in used:
                          used.append(i)
                          count += 1
                      else:
                          #print(i, 'removed')
                          dct[k] = [x for x in dct[k] if x != i]
                  else:
                      dct[k] = [x for x in dct[k] if x != i]



  #now we balance the number of images per each of the 80 cases
  ref_thresh = min([len(ls) for ls in dct.values()])
  print('Number of images in least-represented case:',ref_thresh)

  lstlst = ['train', 'val', 'test']
  qT, qV, qTt = [],[],[]
  train, val, test = {}, {}, {}
  countT,countV,countTt = 0,0,0

  for k, v in dct.items():
      try:
         dct[k] = random.sample(v,n_cases_per_class)
      except:
            print('Not enough cases to build a balanced dataset. Build more cases and try again!')
            exit(0)
      color = k.split('_')[0]
      size = k.split('_')[1]
      shape = k.split('_')[2]
      gt = k.split('_')[3]
      if args.task == 'a':
         if size == 'biggest':
            idx = 1
         else:
             idx = 0 
      else:
          if size == 'big':
             idx = 1
          else:
              idx = 0
      if gt == 'true':
         ans = 'yes'
      else:
          ans = 'no'

      count = 1
      for el in v:
          if uptask == 'a' or uptask == 'b' or uptask == 'c' or uptask == 'd':
             if count <= (n_cases_per_class*0.8):
                reflist = qT
                splt = str(lstlst[0])
                countT +=1
                prog = countT
             if count > (n_cases_per_class*0.8) and count <= (n_cases_per_class*0.9):
                reflist = qV
                splt = str(lstlst[1])
                countV +=1
                prog = countV
             elif count > (n_cases_per_class*0.9):
                  reflist = qTt
                  splt = str(lstlst[2])        
                  countTt +=1
                  prog = countTt
          else:
             if count <= (n_cases_per_class*0.5):
                reflist = qV
                splt = str(lstlst[1])
                countV +=1
                prog = countV
             elif count > (n_cases_per_class*0.5):
                  reflist = qTt
                  splt = str(lstlst[2]) 
                  countTt +=1
                  prog = countTt

           
          img = str(el)+'.png'
          if args.task == 'c' or args.task == 'c_hard':
             q = str("The "+str(color)+" "+str(shape)+" is a "+str(size)+" object")
          elif args.task == 'a':
               q = str("The "+str(color)+" "+str(shape)+" is the "+str(size)+" "+str(shape))
          else:
               q = str("The "+str(color)+" "+str(shape)+" is a "+str(size)+" "+str(shape))

          d = {}
          eldict = data[el]
          d = {
              "image_index": int(prog-1), 
              "program": [],
              "question_index": int(prog-1),
              "image_filename": str(str(prog-1)+'.png'),
              "image_filename_original": str(img),
              "question_family_index": int(idx),
              "split": splt,
              "answer": str(ans),
              "question": str(q)
          }
          reflist.append(d)

          if reflist == qT:
             if not os.path.exists(str(out_path)+'train/'):
                os.mkdir(str(out_path)+'train/')
             nameout = str(str(out_path)+'train/'+str(prog-1)+'.png')
          elif reflist == qV:
              if not os.path.exists(str(out_path)+'val/'):
                 os.mkdir(str(out_path)+'val/')
              nameout = str(str(out_path)+'val/'+str(prog-1)+'.png')
          else:
              if not os.path.exists(str(out_path)+'test/'):
                 os.mkdir(str(out_path)+'test/')
              nameout = str(str(out_path)+'test/'+str(prog-1)+'.png')

          name = str(str(source_path)+str(img))
          shutil.copy2(name, nameout)
          count += 1


  train = {"info": {},
           "questions": qT
  }

  val = {"info": {},
         "questions": qV
  }  

  test = {"info": {},
         "questions": qTt
  }

  print('train:',len(train['questions']))
  print('validation:',len(val['questions']))
  print('test:',len(test['questions']))
  
  if len(train['questions']) != 0:
     out1 = open(str(out_path)+'train.json', 'w')
     json.dump(train, out1)
     out1.close()

  out2 = open(str(out_path)+'val.json', 'w')
  json.dump(val, out2)
  out2.close()

  out3 = open(str(out_path)+'test.json', 'w')
  json.dump(test, out3)
  out3.close()
  

if __name__ == '__main__':
  args = parser.parse_args()
  main(args)

