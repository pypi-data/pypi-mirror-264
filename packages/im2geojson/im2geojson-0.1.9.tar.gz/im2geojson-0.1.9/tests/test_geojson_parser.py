"""
Tests for geojson_parser
"""

import unittest
from im2geojson.geojson_parser import GeoJSONParser
import geojson


class TestGeoJSONParser(unittest.TestCase):

    def test_init_geojson_parser_collections_dictionary(self):
        geojson_parser = GeoJSONParser()
        self.assertEqual({}, geojson_parser._collections_dict)

    def test_add_first_feature(self):
        geojson_parser = GeoJSONParser()
        test_title = 'Test_Title'
        geojson_parser.add_feature(
            title = test_title, lat=0, long=0, properties={}
        )
        self.assertTrue(test_title in geojson_parser._collections_dict)
        self.assertEqual(1, len(geojson_parser._collections_dict[test_title]['features']))

    def test_point_feature_coord_long_lat(self):
        geojson_parser = GeoJSONParser()
        test_title = 'Test_Title'
        test_lat = -8
        test_long = 115
        geojson_parser.add_feature(
            title = test_title, lat=test_lat, long=test_long, properties={}
        )
        feature = geojson_parser._collections_dict[test_title]['features'][0]
        geometry = feature['geometry']
        coords = geometry['coordinates']
        self.assertEqual([test_long, test_lat], coords)

    def test_add_second_feature(self):
        geojson_parser = GeoJSONParser()
        test_title = 'Test_Title'
        geojson_parser.add_feature(
            title = test_title, lat=0, long=0, properties={}
        )
        geojson_parser.add_feature(
            title = test_title, lat=0, long=0, properties={}
        )
        self.assertEqual(2, len(geojson_parser._collections_dict[test_title]['features']))

    def test_add_second_collection(self):
        geojson_parser = GeoJSONParser()
        test_title1 = 'Test_Title1'
        test_title2 = 'Test_Title2'
        geojson_parser.add_feature(
            title = test_title1, lat=0, long=0, properties={}
        )
        geojson_parser.add_feature(
            title = test_title2, lat=0, long=0, properties={}
        )
        self.assertEqual(1, len(geojson_parser._collections_dict[test_title1]['features']))
        self.assertEqual(1, len(geojson_parser._collections_dict[test_title2]['features']))
        
    def test_geojson_parser_iterator(self):
        geojson_parser = GeoJSONParser()

        # test data
        test_lat = 0
        test_long = 0
        test_title1 = 'Test_Title1'
        test_title2 = 'Test_Title2'

        # add_feature
        geojson_parser.add_feature(
            title = test_title1, lat=test_lat, long=test_long, properties={}
        )
        
        # test geojson
        test_point = geojson.Point((test_lat, test_long))
        test_feature = geojson.Feature(geometry=test_point, properties={})
        test_feature_collection = geojson.FeatureCollection(
            features=[test_feature],
            title=test_title1
            )
        
        # iterator
        it = iter(geojson_parser)
        title, feature_collection = next(it)
        self.assertEqual(test_title1, title)
        self.assertEqual(test_feature_collection, feature_collection)
        with self.assertRaises(StopIteration):
            next(it)


if __name__ == '__main__':
    unittest.main()             # pragma: no cover