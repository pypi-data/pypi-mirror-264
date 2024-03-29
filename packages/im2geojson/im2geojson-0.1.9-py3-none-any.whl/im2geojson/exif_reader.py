"""
Read Exchangeable Image File Format (EXIF) metadata from an image.
"""
from exif import Image
from datetime import datetime
import warnings 
import threading
import logging

from .dms_conversion import dms_to_decimal

log = logging.getLogger('im2geojson')


def read_exif(filepath, get_image=False, get_thumbnail=False):
    """
    Read exif metadata from image file at `filepath`.
    
    Parameters
    ----------
    filepath : str
        The path to the image file.

    Returns
    -------
    (lat, long) : tuple of float
        The decimal latitude, longitude coordinate as a float.
    props : dictionary
        Dictionary containing the date the image was captured.
    image_b : bytes
        The image stripped of exif metadata.
    thumb_b : bytes
        The thumbnail.
    
    Raises
    ------
    KeyError
        If `image_file` has no metadata.
    AttributeError
        If `image_file` has missing metadata.
    ValueError
        If `image_file` has invalid metadata.
    FileNotFoundError
        If no file found at `filepath.
    """
    try:
        with open(filepath, 'rb') as image_file:
            image = Image(image_file)
            if not image.has_exif:
                raise KeyError('KeyError: No metadata.')

            # coord
            try:
                dms_lat = (*image.gps_latitude, image.gps_latitude_ref)
                dms_long = (*image.gps_longitude, image.gps_longitude_ref)
            except AttributeError as e:
                raise AttributeError(f'AttributeError: {e}') from e
            else:
                try:
                    lat = dms_to_decimal(*dms_lat)
                    long = dms_to_decimal(*dms_long)
                except ValueError as e:
                    raise e
            
            # datetime
            try:
                datetime_str = image.datetime_original
            except AttributeError as e:
                raise AttributeError(f'AttributeError: {e}') from e
            else:
                try:
                    datetime_object = datetime.strptime(datetime_str, '%Y:%m:%d %H:%M:%S')
                except ValueError as e:
                    raise ValueError(f'ValueError: {e}') from e

            # props 
            props = { 
                "datetime": str(datetime_object),
                }

            # delete exif data
            if get_image:
                with threading.RLock():
                    # Catch warning that not all data has been deleted:
                    with warnings.catch_warnings():
                        warnings.simplefilter('ignore')
                        image.delete_all()
                
            # files
            image_b = image.get_file() if get_image else None

            # TODO - try
            thumb_b = image.get_thumbnail() if get_thumbnail else None

            return (lat, long), props, image_b, thumb_b
        

    except FileNotFoundError as e:
        log.exception(f'FileNotFoundError: No such file or directory: {filepath}')