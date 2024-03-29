"""
Tests for geojsonphoto
"""

import unittest
import os
import shutil
import io
from contextlib import redirect_stdout

from im2geojson.im2geojson import *


class TestBaseClass(unittest.TestCase):

    def setUp(self):
        self.default_in_path = "./"
        self.input_directory = 'tests/test_files/test_images/test_exif/'
        self.output_directory = 'tests/assets/'
        self.geojson_dir_path = os.path.join(self.output_directory, GEOJSON_DIR)
        self.image_dir_path = os.path.join(self.output_directory, IMAGE_DIR)

    def tearDown(self):
        if os.path.isdir(self.output_directory):
            shutil.rmtree(self.output_directory)

        if os.path.isdir(DEFAULT_OUTPUT_DIRECTORY):
            shutil.rmtree(DEFAULT_OUTPUT_DIRECTORY)

class TestImageToGeoJSONInit(TestBaseClass):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()
    
    def test_in_path(self):
        im2geojson = ImageToGeoJSON(input_directory = self.input_directory)
        self.assertEqual(self.input_directory, im2geojson.input_directory)

    def test_no_in_path_raises_exception(self):
        with self.assertRaises(TypeError):
            im2geojson = ImageToGeoJSON()
    
    def test_out_path(self):
        im2geojson = ImageToGeoJSON(input_directory = self.input_directory, output_directory = self.output_directory)
        self.assertEqual(self.output_directory.rstrip('/'), im2geojson.output_directory)

    def test_output_folder(self):
        im2geojson = ImageToGeoJSON(input_directory = self.input_directory, output_directory = self.output_directory)
        self.assertEqual('assets', im2geojson._output_parent_folder())

    def test_init_creates_geojsonphoto_dir_path(self):
        im2geojson = ImageToGeoJSON(input_directory = self.input_directory, output_directory = self.output_directory)
        self.assertEqual(self.geojson_dir_path, im2geojson._geojson_dir_path)

    def test_init_creates_image_dir_path(self):
        im2geojson = ImageToGeoJSON(input_directory = self.input_directory, output_directory = self.output_directory)
        self.assertEqual(self.image_dir_path, im2geojson._image_dir_path)
    
    def test_init_geojsonphoto_parser(self):
        im2geojson = ImageToGeoJSON(input_directory = self.input_directory, output_directory = self.output_directory)
        self.assertTrue(im2geojson._geojson_parser)
    
    def test_default_init_im2geojson_creates_out_directories(self):
        self.assertFalse(os.path.isdir(self.output_directory))

        im2geojson = ImageToGeoJSON(input_directory = self.input_directory, 
                            output_directory = self.output_directory)

        self.assertTrue(os.path.isdir(self.geojson_dir_path))
        self.assertFalse(os.path.isdir(self.image_dir_path))
    
    def test_thumbnail_init_im2geojson_creates_out_directories(self):
        self.assertFalse(os.path.isdir(self.output_directory))

        im2geojson = ImageToGeoJSON(input_directory = self.input_directory, 
                            output_directory = self.output_directory, 
                            save_images=False, 
                            save_thumbnails=True)

        self.assertTrue(os.path.isdir(self.geojson_dir_path))
        self.assertTrue(os.path.isdir(self.image_dir_path))
    
    def test_image_init_im2geojson_creates_out_directories(self):
        self.assertFalse(os.path.isdir(self.output_directory))

        im2geojson = ImageToGeoJSON(input_directory = self.input_directory, 
                            output_directory = self.output_directory, 
                            save_images=True, 
                            save_thumbnails=False)

        self.assertTrue(os.path.isdir(self.geojson_dir_path))
        self.assertTrue(os.path.isdir(self.image_dir_path))

    def test_init_logs_geojson_directory_created(self):
        self.assertFalse(os.path.isdir(self.output_directory))

        with self.assertLogs() as captured:
            im2geojson = ImageToGeoJSON(input_directory = self.input_directory, 
                                output_directory = self.output_directory)

        self.assertEqual(len(captured.records), 1)
        self.assertEqual(captured.records[0].getMessage(), f"Folder {self.geojson_dir_path} created.")

    def test_init_logs_geojson_directory_exists(self):
        self.assertFalse(os.path.isdir(self.output_directory))
        os.makedirs(self.geojson_dir_path)

        with self.assertLogs() as captured:
            im2geojson = ImageToGeoJSON(input_directory = self.input_directory, 
                                output_directory = self.output_directory)

        self.assertEqual(len(captured.records), 1)
        self.assertEqual(captured.records[0].getMessage(), f"Folder {self.geojson_dir_path} already exists.")

    def test_init_logs_image_directory_created(self):
        self.assertFalse(os.path.isdir(self.output_directory))

        with self.assertLogs() as captured:
            im2geojson = ImageToGeoJSON(input_directory = self.input_directory, 
                            output_directory = self.output_directory, 
                            save_images=True, 
                            save_thumbnails=False)

        self.assertEqual(len(captured.records), 2)
        self.assertEqual(captured.records[1].getMessage(), f"Folder {self.image_dir_path} created.")
        

class TestImageToGeoJSONStart(TestBaseClass):

    def setUp(self):
        super().setUp()
        self.test_geojson_file_name = 'test_folder.geojson'

    def tearDown(self):
        super().tearDown()

    def test_im2geojson_start_creates_geojsonphoto_file(self):
        im2geojson = ImageToGeoJSON(input_directory = self.input_directory, 
                            output_directory = self.output_directory, 
                            save_images=False)
        im2geojson.start()

        self.assertTrue(os.path.isdir(self.geojson_dir_path))

        geojson_path = os.path.join(self.geojson_dir_path, self.test_geojson_file_name)
        with open(geojson_path, 'r') as f:
            jsn = json.load(f)
            self.assertIsNotNone(jsn['features'][0]['properties']['datetime'])

            with self.assertRaises(KeyError):
                jsn['features'][0]['properties']['image_path']
            with self.assertRaises(KeyError):
                jsn['features'][0]['properties']['thumbnail_path']

    def test_im2geojson_start_creates_image_file(self):
        test_image_file = 'EXIF.jpg'
        im2geojson = ImageToGeoJSON(input_directory = self.input_directory, 
                            output_directory = self.output_directory, 
                            save_images=True)
        im2geojson.start()

        self.assertTrue(os.path.isdir(self.image_dir_path))

        image_path = os.path.join(self.image_dir_path, test_image_file)
        with open(image_path, 'r') as f:
            pass
        
        geojson_path = os.path.join(self.geojson_dir_path, self.test_geojson_file_name)
        with open(geojson_path, 'r') as f:
            jsn = json.load(f)
            self.assertIsNotNone(jsn['features'][0]['properties']['datetime'])
            self.assertIsNotNone(jsn['features'][0]['properties']['rel_image_path'])

            with self.assertRaises(KeyError):
                jsn['features'][0]['properties']['rel_thumbnail_path']

    def test_im2geojson_start_creates_thumbnail_file(self):
        test_thumbnail_file = 'EXIF_thumb.jpg'
        im2geojson = ImageToGeoJSON(input_directory = self.input_directory, 
                            output_directory = self.output_directory, 
                            save_images=False, 
                            save_thumbnails=True)
        im2geojson.start()

        self.assertTrue(os.path.isdir(self.image_dir_path))

        thumb_path = os.path.join(self.image_dir_path, test_thumbnail_file)
        with open(thumb_path, 'r') as f:
            pass
        
        geojson_path = os.path.join(self.geojson_dir_path, self.test_geojson_file_name)
        with open(geojson_path, 'r') as f:
            jsn = json.load(f)
            self.assertIsNotNone(jsn['features'][0]['properties']['datetime'])
            self.assertIsNotNone(jsn['features'][0]['properties']['rel_thumbnail_path'])

            with self.assertRaises(KeyError):
                jsn['features'][0]['properties']['rel_image_path']

    def test_im2geojson_start_original_image_absolute_path(self):
        test_thumbnail_file = 'EXIF_thumb.jpg'
        im2geojson = ImageToGeoJSON(input_directory = self.input_directory, 
                            output_directory = self.output_directory, 
                            save_images=False, 
                            save_thumbnails=False)
        im2geojson.start()

        geojson_path = os.path.join(self.geojson_dir_path, self.test_geojson_file_name)
        with open(geojson_path, 'r') as f:
            jsn = json.load(f)
            self.assertIsNotNone(jsn['features'][0]['properties']['original_image_absolute_path'])


class TestImageToGeoJSONStatus(TestBaseClass):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_in_progress_status(self):
        im2geojson = ImageToGeoJSON(input_directory = self.input_directory, 
                                 output_directory = self.output_directory, 
                                 save_images=False, 
                                 save_thumbnails=True)
        f = io.StringIO()
        with redirect_stdout(f):
            im2geojson.start()
        out = f.getvalue()
        self.assertIn('Running...\nFinished in ', out)

    def test_repeat_calls_to_start_raises_exception(self):
        im2geojson = ImageToGeoJSON(input_directory = self.input_directory, 
                                 output_directory = self.output_directory, 
                                 save_images=False, 
                                 save_thumbnails=True)
        im2geojson.start()
        with self.assertRaises(RuntimeError):
            im2geojson.start()


class TestImageToGeoJSONErrors(TestBaseClass):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()
    
    def test_no_errors(self):
        im2geojson = ImageToGeoJSON(input_directory = self.input_directory, 
                            output_directory = self.output_directory, 
                            save_images=False, 
                            save_thumbnails=True)
        im2geojson.start()
        self.assertEqual({}, im2geojson.error_dictionary)
    
    def test_errors(self):
        in_path = 'tests/test_files/test_images/test_no_exif/'
        im2geojson = ImageToGeoJSON(input_directory = in_path, 
                            output_directory = self.output_directory,
                            save_images=False, 
                            save_thumbnails=True)
        im2geojson.start()
        test_folder_file = 'test_folder/NO_EXIF.jpg'
        test_error_dictionary = {
            test_folder_file:"'KeyError: No metadata.'"
        }
        self.assertEqual(test_error_dictionary, im2geojson.error_dictionary)


class TestImageToGeoJSONSummary(TestBaseClass):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_summary(self):
        im2geojson = ImageToGeoJSON(input_directory = self.input_directory, 
                            output_directory = self.output_directory, 
                            save_images=False, 
                            save_thumbnails=True)
        im2geojson.start()
        self.assertEqual('1 out of 1 images processed successfully', im2geojson.summary)
        
        
class TestFolderFilesFromPath(unittest.TestCase):

    def setUp(self):
        self.test_filename = 'image_file.jpg'
        self.test_folder_filename = 'image_file_thumb.jpg'
        self.test_folder_name = 'folder'
        self.test_in_path = os.path.join('tests/test_files/', self.test_folder_name, self.test_filename)

    def test_filename_from_path(self):
        filename = ImageToGeoJSON._folder_and_filename_from_filepath(self.test_in_path)[1]
        self.assertEqual(self.test_filename, filename )

    def test_folder_from_path(self):
        folder = ImageToGeoJSON._folder_and_filename_from_filepath(self.test_in_path)[0]
        self.assertEqual(self.test_folder_name, folder)

    def test_thumbnail_filename_from_image_filename(self):
        thumbnail_filename = ImageToGeoJSON._thumbnail_filename(self.test_filename)
        self.assertEqual(self.test_folder_filename, thumbnail_filename)



if __name__ == '__main__':
    unittest.main()             # pragma: no cover