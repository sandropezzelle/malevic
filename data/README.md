# README
This document contains all the information you need to use MALeViC. All **MALeViC data** is contained in the directory `malevic/data/`

The `malevic/data/` directory contains 4 folders, one per each MALeViC task:

- `sup1`
- `pos1`
- `pos`
- `set-pos`

Each folder (e.g.,`sup1`) includes all the needed data for a given task. Data is contained in 3 subfolders:

- `images`
- `dataset`
- `annotation`

## images  

It contains 20K (1478x1478 pixels) **images** in total, split into 3 `.tar.gz` archives:

- `<task>-train.tar.gz` (16K images)
- `<task>-val.tar.gz` (2K images)
- `<task>-test.tar.gz` (2K images)

To extract images from a given archive:
`$ tar -zxvf archive.tar.gz`

Images are in `.png` format and are named with integers ranging from 0 to 15999 in `<task>-train` and with integers from 0 to 1999 in `<task>-val` and `<task>-test`


## dataset

It contains the files with 20K **sentences** and **ground-truth answers** (one per image). The dataset is divided into 3 files, one per split:

- `train` (16K datapoints)
- `val` (2K datapoints)
- `test` (2K datapoints)

For each split, we provide data both in `.json` and `.h5` format. 
NOTE: `.h5` is the required format by the models tested in the paper.

The content of the `.json` files can be previewed in the terminal: `$ python -m json.tool split.json`

Here below, we provide a snippet showing data structure:

    "info": {},
    "questions": [
        {
            "answer": "no",
            "image_filename": "0.png",
            "image_filename_original": "8892.png",
            "image_index": 0,
            "program": [],
            "question": "The yellow square is a big object",
            "question_family_index": 1,
            "question_index": 0,
            "split": "val"
        },

As can be seen, datapoints are included in `"questions"` (which is a list of dictionaries). Each datapoint is annotated with:

- `"answer"`: automatically generated ground-truth answer to the question
- `"image_filename"`: image name in the split
- `"image_filename_original"`: original image name, i.e. name of the image among all generated images for the task (see **annotation** below)
- `"image_index"`: integer standing for image index
- `"program"`: this entry is just to preserve CLEVR data structure; here, it is always an empty list
- `"question"`: question to be answered
- `"question_family_index"`: this entry is just to preserve CLEVR data structure; here, we annotate with 1 questions containing *big*, 0 *small*
- `"question_index"`: same integer as image index
- `"split"`: dataset split

In addition to these files, we provide:

- `vocab.json`

a file containing the entire vocabulary of tokens used in the dataset.


## annotation

It contains full annotation for each image included in the dataset. Annotation is contained in 3 `.json` files, one per split:

- `train_annotation.json` (16K datapoints)
- `val_annotation.json` (2K datapoints)
- `test_annotation.json` (2K datapoints)


Full annotation includes, per each image, information about **scene**, **objects**, and **captions**.

**NOTE**: each *key* in this dictionary (e.g., `0` in the example below) corresponds to`"image_index"` (and `"image_filename"`) in **dataset**. Thus, to obtain annotation for a dataset image, extract the *value* in this dictionary using `"image_index"` *key*.


Here below, we provide a snippet showing data structure:


     "0": [
        {
            "avg_area_px": "16800.0",
            "image_id": "8892",
            "image_url": "8892.png",
            "max_area": "57600",
            "max_radius": "120",
            "min_area": "3600",
            "min_radius": "30",
            "n_colors": "3",
            "n_objects": "5",
            "total_area_px": "84000"
        },
        {
            "objects": [
                {
                    "area": "6400",
                    "cc": "70",
                    "color": "green",
                    "k": "0.2499",
                    "object_id": "0",
                    "prob": "1.0",
                    "radius": "40",
                    "rr": "212",
                    "shape": "square",
                    "size": "small",
                    "thresh_dist": "0.6982",
                    "vagueness": "same"
                },
                {
                    "area": "6400",
                    "cc": "996",
                    "color": "green",
                    "k": "0.2499",
                    "object_id": "1",
                    "prob": "1.0",
                    "radius": "40",
                    "rr": "366",
                    "shape": "triangle",
                    "size": "small",
                    "thresh_dist": "0.6982",
                    "vagueness": "same"
                },
                {
                    "area": "3600",
                    "cc": "441",
                    "color": "red",
                    "k": "0.2499",
                    "object_id": "2",
                    "prob": "1.0",
                    "radius": "30",
                    "rr": "626",
                    "shape": "triangle",
                    "size": "small",
                    "thresh_dist": "0.7501",
                    "vagueness": "same"
                },
                {
                    "area": "57600",
                    "cc": "783",
                    "color": "red",
                    "k": "0.2499",
                    "object_id": "3",
                    "prob": "0.9965",
                    "radius": "120",
                    "rr": "183.0",
                    "shape": "rectangle",
                    "size": "big",
                    "thresh_dist": "0.2499",
                    "vagueness": "same"
                },
                {
                    "area": "10000",
                    "cc": "326",
                    "color": "yellow",
                    "k": "0.2499",
                    "object_id": "4",
                    "prob": "1.0",
                    "radius": "50",
                    "rr": "902",
                    "shape": "square",
                    "size": "small",
                    "thresh_dist": "0.6315",
                    "vagueness": "same"
                }
            ]
        },
        {
            "captions": [
                {
                    "caption_true": "The green square is a small object",
                    "dist_from_thresh:": "0.6982",
                    "k": "0.2499",
                    "prob_RH_R_true": "1.0",
                    "vagueness": "same"
                },
                {
                    "caption_false": "The green square is a big object",
                    "dist_from_thresh": "0.6982",
                    "k": "0.2499",
                    "prob_RH_R_false": "0.0",
                    "vagueness": "same"
                }
            ]
        },
        {
            "captions": [
                {
                    "caption_true": "The yellow square is a small object",
                    "dist_from_thresh:": "0.6315",
                    "k": "0.2499",
                    "prob_RH_R_true": "1.0",
                    "vagueness": "same"
                },
                {
                    "caption_false": "The yellow square is a big object",
                    "dist_from_thresh": "0.6315",
                    "k": "0.2499",
                    "prob_RH_R_false": "0.0",
                    "vagueness": "same"
                }
            ]
        },
        {
            "captions": [
                {
                    "caption_true": "The green triangle is a small object",
                    "dist_from_thresh:": "0.6982",
                    "k": "0.2499",
                    "prob_RH_R_true": "1.0",
                    "vagueness": "same"
                },
                {
                    "caption_false": "The green triangle is a big object",
                    "dist_from_thresh": "0.6982",
                    "k": "0.2499",
                    "prob_RH_R_false": "0.0",
                    "vagueness": "same"
                }
            ]
        }
    ],


As can be seen, **scene** annotation contains information on:

- `"avg_area_px"`: average area in pixels computed over all objects in the scene
- `"image_id"`: *original* image number; `"image_url"`: *original* image name (same as `"image_filename_original"` in **dataset** above)
- `"max_area"`, `"min_area"`: number of pixels of biggest and smallest, respectively, object in the scene
- `"max_radius"`, `"min_radius"`: size class (ranging from 30 to 120) of the biggest and smallest, respectively, object in the scene
- `"n_colors"`: number of unique colors in the scene
- `"n_objects"`: number of objects in the scene
- `"total_area_px"`: total number of pixels occupied by objects in the scene

For each object in the scene, **objects** annotation contains information on:

- `"area"`: number of pixels occupied by the object
- `"cc"`, `"rr"`: spatial coordinates of the object
- `"color"`: object color
- `"k"`: sampled *k* ranging from 0.09 to 0.49 determining threshold T
- `"object_id"`: id of the object (from 0 to 8)
- `"prob"`: probability for the object to have the size in the ground truth annotation (not used in the reported experiments)
- `"radius"`: size class (ranging from 30 to 120) of the object
- `"shape"`: shape type
- `"size"`: automatically generated ground truth size
- `"thresh_dist"`: normalized distance from the threshold (the lower, the closer); it ranges from 0 to 1
- `"vagueness"`: if *same*, then the ground truth answer would not have changed if *k* was = 0.29; if *different*, then the ground truth answer would have been different (opposite)

For each generated sentence suitable for the scene, **captions** annotation contains information on:

- `"caption_true"`, `"caption_false"`: automatically generated *true* and *false* sentence, respectively
- `"dist_from_thresh"`: normalized distance from the threshold of the queried object (the lower, the closer)
- `"k"`: sampled *k*
- `"prob_RH_R_true"`, `"prob_RH_R_false"`: probability for a *true* or *false* sentence, respectively, to be *true* or *false* (not used in the experiments reported in the paper)
- `"vagueness"`: if *same*, then the ground truth answer would not have changed if *k* was = 0.29; if *different*, then the ground truth answer would have been different (opposite)

----
### changelog
* 09-September-2019