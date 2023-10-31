import pytest

from arrivalboard.latlon import BoundingBox
from arrivalboard.latlon import get_bearing_between_points
from arrivalboard.latlon import get_bounding_square_from_point
from arrivalboard.latlon import get_point_from_distance_and_bearing


class TestGetBoundingSquareFromPoint:

    @pytest.mark.parametrize("lat,lon,expected", [
        (41.977000, 87.908167, BoundingBox(lat_min=41.874583, lon_min=87.770733, lat_max=42.079252, lon_max=88.046044)),
        (41.977000, -87.908167, BoundingBox(lat_min=41.874583, lon_min=-88.045601, lat_max=42.079252, lon_max=-87.77029)),
        (-41.977000, 87.908167, BoundingBox(lat_min=-42.079252, lon_min=87.77029, lat_max=-41.874583, lon_max=88.045601)),
        (-41.977000, -87.908167, BoundingBox(lat_min=-42.079252, lon_min=-88.046044, lat_max=-41.874583, lon_max=-87.770733)),
        (0, 87.908167, BoundingBox(lat_min=-0.102334, lon_min=87.805832, lat_max=0.102334, lon_max=88.010502)),
        (41.977000, 0, BoundingBox(lat_min=41.874583, lon_min=-0.137434, lat_max=42.079252, lon_max=0.137877)),
        (0, 0, BoundingBox(lat_min=-0.102334, lon_min=-0.102335, lat_max=0.102334, lon_max=0.102335)),
    ])
    def test_lat_lon_input(self, lat, lon, expected):
        box: BoundingBox = get_bounding_square_from_point(lat=lat, lon=lon, radius_miles=10)
        assert box == expected

    @pytest.mark.parametrize("radius_miles,expected", [
        (10, BoundingBox(lat_min=41.874583, lon_min=-88.045601, lat_max=42.079252, lon_max=-87.77029)),
        (.1, BoundingBox(lat_min=41.975977, lon_min=-87.909544, lat_max=41.978023, lon_max=-87.90679)),
        (0, BoundingBox(lat_min=41.977000, lon_min=-87.908167, lat_max=41.977000, lon_max=-87.908167)),
        (-10, BoundingBox(lat_min=42.079252, lon_min=-87.77029, lat_max=41.874583, lon_max=-88.045601))
    ])
    def test_radius_miles_input(self, radius_miles, expected):
        box: BoundingBox = \
            get_bounding_square_from_point(lat=41.977000, lon=-87.908167, radius_miles=radius_miles)
        assert box == expected


class TestGetPointFromDistanceAndBearing:

    @pytest.mark.parametrize("lat,lon,expected", [
        (41.977000, 87.908167, (41.976836, 88.10284)),
        (41.977000, -87.908167, (41.976836, -87.713494)),
        (-41.977000, 87.908167, (-41.976836, 88.10284)),
        (-41.977000, -87.908167, (-41.976836, -87.713494)),
        (0, 87.908167, (0.0, 88.05289)),
        (41.977000, 0, (41.976836, 0.194673)),
        (0, 0, (0.0, 0.144723)),
    ])
    def test_lat_lon_input(self, lat, lon, expected):
        result = get_point_from_distance_and_bearing(lat, lon, 10, 90)
        assert result == expected

    @pytest.mark.parametrize("dist,expected", [
        (10, (41.976836, -87.713494)),
        (.1, (41.977000, -87.90622)),
        (0, (41.977000, -87.908167)),
        (-10, (41.976836, -88.10284)),
    ])
    def test_distance_input(self, dist, expected):
        result = get_point_from_distance_and_bearing(41.977000, -87.908167, dist, 90)
        assert result == expected

    def test_poop(self):
        print(get_point_from_distance_and_bearing(41.977000, -87.908167, 10, 360))


class TestGetBearingBetweenPoints:

    @pytest.mark.parametrize("lat_a,lon_a,lat_b,lon_b,expected", [
        (41.977000, -87.908167, 42.121723, -87.908167, 0),
        (41.977000, -87.908167, 42.120167, -87.879664, 8.4),
        (41.977000, -87.908167, 42.108134, -87.825725, 25),
        (41.977000, -87.908167, 41.976836, -87.713494, 90),
        (41.977000, -87.908167, 41.87512, -87.770014, 134.7),
        (41.977000, -87.908167, 41.979361, -88.102818, 271),
    ])
    def test_lat_lon_input(self, lat_a, lon_a, lat_b, lon_b, expected):
        result = get_bearing_between_points(lat_a, lon_a, lat_b, lon_b)
        assert result == expected
