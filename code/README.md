# README
This document describes the **code** contained in the directory `malevic/code/`

In this folder, you can find the code for **generating** new images and corresponding annotation, and to obtain new (balanced) datasets **from scratch**:

- `build_data.py`

- `extract_dataset.py`

## Generating data from scratch

You can generate new MALeViC images and annotation by running 

`$ python build_data.py`

with the desired **arguments**. Note: a brief description of each argument can be found in the script.

### Example

To generate new data and annotation for the **SET+POS** task, for example, all you have to do is to run the following:

`$ python build_data.py --task d --n_images 10 --steps 5 --outputh_path /mydata/`

This will generate a folder named `d_vague_all_data` in your output directory containing 10 images (numbered with indexes 0-9)  and 2 `.json` files with full annotation (scene level, object level, captions) for scenes 0-4 and 5-9, respectively. Note that, by setting `steps` to 1, annotation for all generated images will be saved into a single `.json` file; however, we recommend saving annotation in several `.json` files so to avoid losing any annotation already generated. This way, in case anything wrong happens, you will be able to resume the data generation from where it stopped.

**NOTE** that, in the code, tasks are referred to as letters `a`, `b`, `c`, `d`. In particular, task `sup1` is referred to as `a`, `pos1` as `b`, pos as `c`, and `set+pos` as `d`. Consistently, e.g., task `set+pos-hard` is referred to as `d_hard`, and so on.


## Extracting a balanced dataset

Once your images and annotation are generated, you can obtain a balanced dataset (train, val, test) including, per each split, one folder with the extracted images and the corresponding `.json` file with question-answer pairs.

To do so, all you have to do is to run

`$ python extract_dataset.py`

with the desired **arguments**. Note: a brief description of each argument can be found in the script.

### Example

To extract a balanced dataset (train, val, test) for the **SET+POS** task, for example, all you have to do is to run the following:

`$ python extract_dataset.py --input_path ./mydata/ --outputh_path ./mydataset/ --task d --cases_per_class 50`

In this case, the script will generate a folder called `d_vague_dataset` containing 3 .json files:  `train.json` (3200 datapoints), `val.json` (400), and `test.json` (400). The corresponding images for each split will be saved in a separate folder. **Important**: in case there are not enough generated images (and annotation) to allow for a perfectly balanced dataset, it may be necessary to build extra images!

Note that, by default, there are **80 classes** (4 shapes \* 5 colors \* 2 sizes \* 2 ground-truth answers). That is, by default a dataset containing 20K datapoints (16K, 2K, 2K) will be generated.

Also note that, if `--difficulty` is set to **hard**, then only `val.json` and `test.json` will be generated.


## Training the models


In the subfolder `code/train/`, you can find the scripts for **training all models** tested in the paper, with all reported configurations of hyper-parameters (all the **hyper-parameters** are briefly described in the script):

- `train_film.sh`

- `train_film_pixels.sh`

- `train_baselines.sh`


To do so, you first need to preprocess the `train.json`, `val.json`, and `test.json` files (questions) and to extract visual features of images with a pre-trained ResNet-101 ([instructions here](https://github.com/facebookresearch/clevr-iep/blob/master/TRAINING.md#preprocessing-clevr)). Then, you need to clone repositories [clevr-iep] (https://github.com/facebookresearch/clevr-iep) and [film] (https://github.com/ethanjperez/film) and train the models by launching the `.sh` scripts above.

[Note that some minor adjustments to the preprocessing and model code could be needed to make them work with pytorch 1]

## Testing the models

You can test the best trained models described in the paper [available soon]

----
## changelog
* 02-October-2013 
