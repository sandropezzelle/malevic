# README
This directory contains all the MALeViC data.

There are 4 folders, one per each MALeViC task:
- sup1/
- pos1/
- pos/
- set-pos/

Each folder (e.g. sup1/) contains 3 subfolders:
- annotation/
- dataset/
- images/

The content of each subfolder is described below. 

## annotation

This folder includes 3 .json files:
- train_annotation.json
- val_annotation.json
- test_annotation.json

Each .json file contains full annotation for each scene in a given task split (e.g. train).
Full annotation include annotation at both scene level (number of objects in the scene, max area, min area, etc.) and object level (area, color, shape, etc.)

The file is structured as follows:


Note that the train file contains 16K datapoints, val 2K datapoints, test 2K datapoints.
To preview one <annotation file>: $ python -m json.tool <annotation file>.json 

## dataset

This folder contains 4 .json files and 3 .h5 files:
- train.json
- val.json
- test.json
- vocab.json

The first 3 files contain the datapoints used in the paper.  

## images  

This folder contains 3 .tar.gz archives containing the images used in each task.
There are 20K images in total: 16K images for training (train), 2K for validation (val), and 2K for testing (test).
Images are named with integers ranging from 0 to the length of the split - 1; e.g., in val, from 0.png to 1999.png
To extract images from a given <task-split> archive: $ tar -zxvf <task-split>.tar.gz

