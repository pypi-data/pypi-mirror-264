"""
Parse GPS data to GeoJSON Features
"""
import geojson


class GeoJSONParser(object):
    """
    Create a GeoJSONParser object.
    
    """

    def __init__(self):
        self._collections_dict = {}

    def __iter__(self):
        """Return an iterator for `_collections_dict` items."""
        return iter(self._collections_dict.items())

    def add_feature(self, title, lat, long, properties={}):
        """
        Add a `Feature' to `_collections_dict`.

        Parameters
        ----------
        title : str
            The `FeatureCollection` title.
        lat : float
            The latitude of the Feature.
        long : float
            The longitude of the Feature.
        properties : dict
            The Feature properties.
        """
        point = geojson.Point((long, lat))
        feature = geojson.Feature(
            geometry=point, 
            properties=properties
        )
        if title not in self._collections_dict:
            feature_collection = geojson.FeatureCollection(
                features = [feature], 
                title = title
            )
            self._collections_dict[title] = feature_collection
        else:
            self._collections_dict[title]['features'].append(feature)
