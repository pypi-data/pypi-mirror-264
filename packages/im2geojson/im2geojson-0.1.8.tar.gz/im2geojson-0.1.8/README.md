im2geojson
==========


[![Unittests](https://github.com/MJBishop/im2geojson/actions/workflows/test.yml/badge.svg)](https://github.com/MJBishop/im2geojson/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/MJBishop/im2geojson/graph/badge.svg?token=9C03IBN0Z3)](https://codecov.io/gh/MJBishop/im2geojson)



im2geojson is a python package for parsing GeoJSON from image metadata.

<br>

Installation
------------
The recommended way to install im2geojson is via pip:

    pip install im2geojson

<br>

Usage
-----

Simply set the `input_directory` to the path to your image folders:

    python -m im2geojson <path-to-image-folders>


* Image folders are parsed to GeoJSON FeatureCollections
  
* Images are parsed to GeoJSON Features.
  
* GeoJSON files are saved to `output_directory` in a folder named `geojson`
  
* The default is `./assets/geojson`

<br>


Options
-------

### Save Images

`--save_images`  or  `-s`  will save images stripped of metadata:

    python -m im2geojson <path-to-image-folders> -s

* Images are saved to `output_directory` in a folder named `images`

* The default is `./assets/images/`
  
<br>

### Save Thumbnails

`--save_thumbanails`  or  `-t`  will save image thumbnails:

    python -m im2geojson <path-to-image-folders> -t

* Thumbnails are saved to `output_directory` in a folder named `images`

* The default is `./assets/images/`
  
<br>

### Output Directory

`-o` or `--output_directory` will set the `output_directory`:

    python -m im2geojson <path-to-image-folders> -o <output_directory>

<br>

For example, to set the `output_directory` to `./output`:

    python -m im2geojson <path-to-image-folders> -o ./output

<br>


API Documentation
-----------------
Take a look at the [API Documentation](https://mjbishop.github.io/im2geojson/im2geojson.html) if you would like to use im2geojson in your own code.

<br>

