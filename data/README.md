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

It contains 20K (1478 x 1478 pixels) **images** in total, split into 3 `.tar.gz` archives:

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
NOTE: `.h5` format is required by the models tested in the paper.

The content of the `.json` files can be previewed in the terminal: `$ python -m json.tool split.json`

Here below, we provide a snippet showing data structure. As can be seen, datapoints are included in `"questions"`. Each question is annotated with `"answer"` (ground-truth answer), `"image_filename"`, `"question"` (sentence), `"split"`, `"image_filename_original"` (original name of the image), etc.

    "info": {},
    "questions": [
        {
            "answer": "no",
            "image_filename": "0.png",
            "image_filename_original": "23411.png",
            "image_index": 0,
            "program": [],
            "question": "The blue rectangle is the biggest rectangle",
            "question_family_index": 1,
            "question_index": 0,
            "split": "val"
        },



## annotation

It contains full annotation for each image included in a dataset. Annotation is contained in 3 `.json` files, one per split:

- `train_annotation.json`
- `val_annotation.json`
- `test_annotation.json`


Full annotation include annotation at both scene level (number of objects in the scene, max area, min area, etc.) and object level (area, color, shape, etc.)

The file is structured as follows:


Note that the train file contains 16K datapoints, val 2K datapoints, test 2K datapoints.


----
### changelog
* 04-September-2019
