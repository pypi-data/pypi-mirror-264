"""
Tests for cli
"""

import unittest
import io
import shutil
import os
from contextlib import redirect_stdout

from im2geojson.cli import create_parser, parse_args_to_dict, main


class TestParserCreate(unittest.TestCase):

    def test_create_parser(self):
        parser = create_parser()
        self.assertIsNotNone(parser)

    def test_create_parser_prog(self):
        parser = create_parser()
        self.assertEqual('im2geojson', parser.prog)
        self.assertEqual('Parse GeoJSON from image metadata', parser.description)

    
class TestParserArguments(unittest.TestCase):

    def setUp(self):
        self.parser = create_parser()

    def test_parser_positional_input_directory(self):
        parsed = self.parser.parse_args(['testing/in'])
        self.assertEqual('testing/in', parsed.input_directory)

    def test_parser_short_out_path(self):
        parsed = self.parser.parse_args(['testing/in', '-o', 'testing/out'])
        self.assertEqual('testing/out', parsed.output_directory)

    def test_parser_out_path(self):
        parsed = self.parser.parse_args(['testing/in', '--output_directory', 'testing/out'])
        self.assertEqual('testing/out', parsed.output_directory)

    def test_parser_short_save_images(self):
        parsed = self.parser.parse_args(['testing/in', '-s'])
        self.assertTrue(parsed.save_images)

    def test_parser_save_images(self):
        parsed = self.parser.parse_args(['testing/in', '--save_images'])
        self.assertTrue(parsed.save_images)

    def test_parser_short_save_thumbnails(self):
        parsed = self.parser.parse_args(['testing/in', '-t'])
        self.assertTrue(parsed.save_thumbnails)

    def test_parser_save_thumbnails(self):
        parsed = self.parser.parse_args(['testing/in', '--save_thumbnails'])
        self.assertTrue(parsed.save_thumbnails)

    def test_parser_defaults(self):
        parsed = self.parser.parse_args(['testing/in'])
        self.assertTrue(parsed.input_directory)
        with self.assertRaises(AttributeError):
            parsed.out_dir_path
        with self.assertRaises(AttributeError):
            parsed.save_images
        with self.assertRaises(AttributeError):
            parsed.save_thumbnails


class TestParseArgs(unittest.TestCase):

    def test_parsed_args_dict(self):
        args = ['testing/in', '-o', 'testing/out', '-s', '-t']
        parsed_args_dict = parse_args_to_dict(args)
        expected = {'input_directory': 'testing/in', 
                    'output_directory': 'testing/out', 
                    'save_images': True, 
                    'save_thumbnails': True}
        self.assertEqual(expected, parsed_args_dict)


class TestMain(unittest.TestCase):

    def setUp(self):
        self.output_directory = 'tests/assets/'

    def tearDown(self):
        if os.path.isdir(self.output_directory):
            shutil.rmtree(self.output_directory)

    def test_main(self):
        f = io.StringIO()
        with redirect_stdout(f):
            
            main(['./', '-o', self.output_directory])
        out = f.getvalue()
        out_lines = out.split('\n')

        expected_first_line = 'Running...'
        expected_last_line = '0 out of 0 images processed successfully'

        self.assertEqual(expected_first_line, out_lines[0])
        self.assertEqual(expected_last_line, out_lines[2])

    def test_main_prints_errors(self):
        f = io.StringIO()
        with redirect_stdout(f):
            
            main(['tests/test_files/test_images/test_no_exif/', '-o', self.output_directory])
        out = f.getvalue()
        out_lines = out.split('\n')

        expected_first_line = 'Running...'
        expected_last_line = '0 out of 1 images processed successfully'

        self.assertEqual(expected_first_line, out_lines[0])
        self.assertEqual(expected_last_line, out_lines[2])
        self.assertIn('No metadata', out_lines[3])


if __name__ == '__main__':  
    unittest.main()             # pragma: no cover