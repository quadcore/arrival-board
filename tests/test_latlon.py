import pytest

from arrivalboard.latlon import BoundingBox
from arrivalboard.latlon import get_bounding_square_from_point


class TestGetBoundingSquareFromPoint:

    @pytest.mark.parametrize("lat,lon,expected",[
        (41.977000, 87.908167, BoundingBox(lat_min=41.874583, lon_min=87.770733, lat_max=42.079252, lon_max=88.046044)),
        (41.977000, -87.908167, BoundingBox(lat_min=41.874583, lon_min=-88.045601, lat_max=42.079252, lon_max=-87.77029)),
        (-41.977000, 87.908167, BoundingBox(lat_min=-42.079252, lon_min=87.77029, lat_max=-41.874583, lon_max=88.045601)),
        (-41.977000, -87.908167, BoundingBox(lat_min=-42.079252, lon_min=-88.046044, lat_max=-41.874583, lon_max=-87.770733)),
        (0, 87.908167, BoundingBox(lat_min=-0.102334, lon_min=87.805832, lat_max=0.102334, lon_max=88.010502)),
        (41.977000, 0, BoundingBox(lat_min=41.874583, lon_min=-0.137434, lat_max=42.079252, lon_max=0.137877)),
        (0, 0, BoundingBox(lat_min=-0.102334, lon_min=-0.102335, lat_max=0.102334, lon_max=0.102335)),
    ])
    def test_lat_lon_inputs(self, lat, lon, expected):
        box: BoundingBox = get_bounding_square_from_point(lat=lat, lon=lon, radius_miles=10)
        assert box == expected

    @pytest.mark.parametrize("radius_miles,expected", [
        (.1, BoundingBox(lat_min=41.975977, lon_min=-87.909544, lat_max=41.978023, lon_max=-87.90679)),
        (10, BoundingBox(lat_min=41.874583, lon_min=-88.045601, lat_max=42.079252, lon_max=-87.77029)),
        (0, BoundingBox(lat_min=41.977000, lon_min=-87.908167, lat_max=41.977000, lon_max=-87.908167)),
        (-10, BoundingBox(lat_min=42.079252, lon_min=-87.77029, lat_max=41.874583, lon_max=-88.045601))
    ])
    def test_radius_miles_input(self, radius_miles, expected):
        box: BoundingBox = \
            get_bounding_square_from_point(lat=41.977000, lon=-87.908167, radius_miles=radius_miles)
        assert box == expected
