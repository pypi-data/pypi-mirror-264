"""
Tests for dms_conversion
"""

import unittest
from im2geojson.dms_conversion import dms_to_decimal


class TestDMSToDecimal(unittest.TestCase):

    def test_convert_zero_east(self):
        test_result = 0
        self.assertEqual(test_result, dms_to_decimal(0, 0, 0, 'E'))

    def test_convert_five_degrees_east(self):
        test_result = 5
        self.assertEqual(test_result, dms_to_decimal(5, 0, 0, 'E'))

    def test_convert_five_degrees_twelve_minutes_north(self):
        test_result = 5.2
        self.assertEqual(test_result, dms_to_decimal(5, 12, 0, 'N'))

    def test_convert_five_degrees_twelve_minutes_eighteen_seconds_north(self):
        test_result = 5.205
        self.assertEqual(test_result, dms_to_decimal(5, 12, 18, 'N'))

    def test_convert_five_degrees_twelve_minutes_eighteen_seconds_south(self):
        test_result = -5.205
        self.assertEqual(test_result, dms_to_decimal(5, 12, 18, 'S'))

    def test_convert_five_degrees_twelve_minutes_eighteen_seconds_west(self):
        test_result = -5.205
        self.assertEqual(test_result, dms_to_decimal(5, 12, 18, 'W'))

    def test_convert_fiftynine_degrees_five_minutes_three_seconds_north(self):
        test_result = 59.084167
        self.assertEqual(test_result, dms_to_decimal(59, 5, 3, 'N'))

    def test_lat_91N_raises_exception(self):
        with self.assertRaises(ValueError):
            dms_to_decimal(91, 0, 0, 'N')

    def test_lat_91S_raises_exception(self):
        with self.assertRaises(ValueError):
            dms_to_decimal(91, 0, 0, 'S')

    def test_long_181W_raises_exception(self):
        with self.assertRaises(ValueError):
            dms_to_decimal(181, 0, 0, 'W')

    def test_long_181E_raises_exception(self):
        with self.assertRaises(ValueError):
            dms_to_decimal(181, 0, 0, 'E')

    def test_invalid_ref_raises_exception(self):
        with self.assertRaises(ValueError):
            dms_to_decimal(1, 1, 1, 'Z')

    def test_invalid_minutes_60_raises_exception(self):
        with self.assertRaises(ValueError):
            dms_to_decimal(1, 60, 1, 'N')

    def test_invalid_negative_minutes_raises_exception(self):
        with self.assertRaises(ValueError):
            dms_to_decimal(1, -1, 1, 'N')

    def test_invalid_seconds_60_raises_exception(self):
        with self.assertRaises(ValueError):
            dms_to_decimal(1, 1, 60, 'N')

    def test_invalid_negative_seconds_raises_exception(self):
        with self.assertRaises(ValueError):
            dms_to_decimal(1, 1, -1, 'N')

    def test_invalid_negative_degrees_raises_exception(self):
        with self.assertRaises(ValueError):
            dms_to_decimal(-1, 1, 1, 'N')


if __name__ == '__main__':
    unittest.main()             # pragma: no cover