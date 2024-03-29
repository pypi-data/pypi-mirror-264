"""

Parse GeoJSON from image metadata.

<br>


Quick Start
-----------


Import im2geojson and create an image parser:

```python
>>> from im2geojson import ImageToGeoJSON

# Initialise with `input_directory`:
>>> input_directory='./my_images'
>>> my_image_parser = ImageToGeoJSON(input_directory=input_directory)

# Start image processing:
>>> my_image_parser.start()
```
```s
Running...
Finished in 0.31 seconds
```
<br>


Summary
-------

```python
>>> my_image_parser.summary
```
```s
'1 out of 6 images processed successfully'
```
<br>


Output
------

```json
// my_images.geojson
{
    "type": "FeatureCollection", 
    "title": "my_images", 
    "features": 
    [
        {
            "type": "Feature", 
            "geometry": 
            {
                "type": "Point", 
                "coordinates": [115.095269, -8.631053]
            }, 
            "properties": 
            {
                "datetime": "2023-05-05 06:19:24", 
                "original_absolute_path": "./my_images/EXIF.jpg"
            }
        }
    ]
}
```
<br>


Errors
------

```python
>>> my_image_parser.error_dictionary
```
```s
{'my_images/MISSING_EXIF.jpg': 'AttributeError: image does not have attribute gps_latitude',
 'my_images/MISSING_DATETIME.jpg': 'AttributeError: image does not have attribute datetime_original',
 'my_images/CORRUPTED_DATETIME.jpg': "ValueError: time data 'corrupted' does not match format '%Y:%m:%d %H:%M:%S'",
 'my_images/CORRUPTED_EXIF.jpg': 'ValueError: Invalid GPS Reference X, Expecting N, S, E or W',
 'my_images/NO_EXIF.jpg': "'No metadata.'"}
```
<br>
<br>

   
***

<br>

"""

import logging

logging.getLogger('im2geojson').addHandler(logging.NullHandler())


from im2geojson.im2geojson import ImageToGeoJSON

__all__ = ['ImageToGeoJSON']

