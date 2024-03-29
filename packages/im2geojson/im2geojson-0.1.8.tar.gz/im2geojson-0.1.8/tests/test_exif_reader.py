"""
Tests for exif_reader
"""

import unittest
import os

from exif import Image

from im2geojson.exif_reader import read_exif


class TestExif(unittest.TestCase):

    def setUp(self):
        self.in_path = 'tests/test_files/test_images/test_exif/'
        self.file_dir = 'test_folder/EXIF.jpg'
        self.filepath = os.path.join(self.in_path, self.file_dir)

    def test_read_exif_coord_lat_long(self):
        lat = -8.631053
        long = 115.095269
        test_coord = (lat, long)
        coord, props, image_b, thumb_b = read_exif(self.filepath, get_image=False, get_thumbnail=False)
        self.assertEqual(test_coord, coord)

    def test_read_exif_datetime(self):
        datetime = "2023-05-05 06:19:24"
        coord, props, image_b, thumb_b = read_exif(self.filepath, get_image=False, get_thumbnail=False)
        self.assertEqual(props['datetime'], datetime)

    def test_read_exif_thumbnail_file(self):
        coord, props, image_b, thumb_b = read_exif(self.filepath, get_image=False, get_thumbnail=True)
        self.assertIsNotNone(thumb_b)
        self.assertIsNone(image_b)

    def test_read_exif_image_file(self):
        coord, props, image_b, thumb_b = read_exif(self.filepath, get_image=True, get_thumbnail=False)
        self.assertIsNotNone(image_b)
        self.assertIsNone(thumb_b)
    
    def test_read_exif_image_file_strips_exif_gps_data(self):
        coord, props, image_b, thumb_b = read_exif(self.filepath, get_image=True, get_thumbnail=False)
        image = Image(image_b)
        with self.assertRaises(AttributeError):
            image.gps_latitude

    def test_read_exif_logs_exception_for_unknown_file(self):
        file_dir = 'test_folder/NO_EXIST.jpg'
        filepath = os.path.join(self.in_path, file_dir)
        with self.assertLogs() as captured:
            read_exif(filepath, get_image=False, get_thumbnail=False)
        self.assertEqual(len(captured.records), 1)
        self.assertIn('No such file or directory', captured.records[0].getMessage())


class TestExifFromImageTypes(unittest.TestCase):

    def setUp(self):
        self.in_path = 'tests/test_files/test_images/test_multiple_image_types/'

    def test_jpeg(self):
        file_dir = 'test_folder/EXIF_jpeg.jpeg'
        filepath = os.path.join(self.in_path, file_dir)
        coord, props, image_b, thumb_b = read_exif(filepath, get_image=True, get_thumbnail=False)
        self.assertIsNotNone(image_b)

    @unittest.expectedFailure
    def test_tiff(self):
        file_dir = 'test_folder/EXIF_tiff.tiff'
        filepath = os.path.join(self.in_path, file_dir)
        coord, props, image_b, thumb_b = read_exif(filepath, get_image=True, get_thumbnail=False)
        self.assertIsNotNone(image_b)


class TestNoExif(unittest.TestCase):
    
    def setUp(self):
        self.in_path = 'tests/test_files/test_images/test_no_exif/'
        self.file_dir = 'test_folder/NO_EXIF.jpg'
        self.filepath = os.path.join(self.in_path, self.file_dir)

    def test_read_no_exif(self):
        with self.assertRaises(KeyError) as e:
            coord, props, image_b, thumb_b = read_exif(self.filepath, get_image=False, get_thumbnail=False)
        self.assertEqual("'KeyError: No metadata.'", str(e.exception))


class TestMissingExif(unittest.TestCase):
    
    def setUp(self):
        self.in_path = 'tests/test_files/test_images/test_missing_exif/'
        self.file_dir = 'test_folder/MISSING_EXIF.jpg'
        self.filepath = os.path.join(self.in_path, self.file_dir)

    def test_read_missing_exif(self):
        with self.assertRaises(AttributeError) as e:
            coord, props, image_b, thumb_b = read_exif(self.filepath, get_image=False, get_thumbnail=False)
        self.assertEqual('AttributeError: image does not have attribute gps_latitude', str(e.exception))


class TestMissingDatetime(unittest.TestCase):
    
    def setUp(self):
        self.in_path = 'tests/test_files/test_images/test_missing_datetime/'
        self.file_dir = 'test_folder/MISSING_DATETIME.jpg'
        self.filepath = os.path.join(self.in_path, self.file_dir)

    def test_read_missing_datetime(self):
        with self.assertRaises(AttributeError) as e:
            coord, props, image_b, thumb_b = read_exif(self.filepath, get_image=False, get_thumbnail=False)
        self.assertEqual('AttributeError: image does not have attribute datetime_original', str(e.exception))


class TestCorruptedGPSExif(unittest.TestCase):
    
    def setUp(self):
        self.in_path = 'tests/test_files/test_images/test_corrupted_exif/'
        self.file_dir = 'test_folder/CORRUPTED_EXIF.jpg'
        self.filepath = os.path.join(self.in_path, self.file_dir)

    def test_read_corrupted_gps(self):
        with self.assertRaises(ValueError) as e:
            coord, props, image_b, thumb_b = read_exif(self.filepath)
        self.assertEqual('ValueError: Invalid GPS Reference X, Expecting N, S, E or W', str(e.exception))


class TestCorruptedDatetime(unittest.TestCase):
    
    def setUp(self):
        self.in_path = 'tests/test_files/test_images/test_corrupted_datetime/'
        self.file_dir = 'test_folder/CORRUPTED_DATETIME.jpg'
        self.filepath = os.path.join(self.in_path, self.file_dir)

    def test_read_corrupted_datetime(self):
        with self.assertRaises(ValueError) as e:
            coord, props, image_b, thumb_b = read_exif(self.filepath, get_image=False, get_thumbnail=False)
        self.assertEqual("ValueError: time data 'corrupted' does not match format '%Y:%m:%d %H:%M:%S'", str(e.exception))



if __name__ == '__main__':
    unittest.main()             # pragma: no cover