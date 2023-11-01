import pytest

from arrivalboard.latlon import BoundingBox
from arrivalboard.latlon import Coordinate
from arrivalboard.latlon import get_bearing_between_points
from arrivalboard.latlon import get_bounding_square_from_point
from arrivalboard.latlon import get_point_from_distance_and_bearing


class TestGetBoundingSquareFromPoint:

    @pytest.mark.parametrize("coord,expected", [
        (Coordinate(41.977000, 87.908167), BoundingBox(lat_min=41.874583, lon_min=87.770733, lat_max=42.079252, lon_max=88.046044)),
        (Coordinate(41.977000, -87.908167), BoundingBox(lat_min=41.874583, lon_min=-88.045601, lat_max=42.079252, lon_max=-87.77029)),
        (Coordinate(-41.977000, 87.908167), BoundingBox(lat_min=-42.079252, lon_min=87.77029, lat_max=-41.874583, lon_max=88.045601)),
        (Coordinate(-41.977000, -87.908167), BoundingBox(lat_min=-42.079252, lon_min=-88.046044, lat_max=-41.874583, lon_max=-87.770733)),
        (Coordinate(0, 87.908167), BoundingBox(lat_min=-0.102334, lon_min=87.805832, lat_max=0.102334, lon_max=88.010502)),
        (Coordinate(41.977000, 0), BoundingBox(lat_min=41.874583, lon_min=-0.137434, lat_max=42.079252, lon_max=0.137877)),
        (Coordinate(0, 0), BoundingBox(lat_min=-0.102334, lon_min=-0.102335, lat_max=0.102334, lon_max=0.102335)),
    ])
    def test_lat_lon_input(self, coord, expected):
        box: BoundingBox = get_bounding_square_from_point(coord=coord, radius_miles=10)
        assert box == expected

    @pytest.mark.parametrize("radius_miles,expected", [
        (10, BoundingBox(lat_min=41.874583, lon_min=-88.045601, lat_max=42.079252, lon_max=-87.77029)),
        (.1, BoundingBox(lat_min=41.975977, lon_min=-87.909544, lat_max=41.978023, lon_max=-87.90679)),
        (0, BoundingBox(lat_min=41.977000, lon_min=-87.908167, lat_max=41.977000, lon_max=-87.908167)),
        (-10, BoundingBox(lat_min=42.079252, lon_min=-87.77029, lat_max=41.874583, lon_max=-88.045601))
    ])
    def test_radius_miles_input(self, radius_miles, expected):
        box: BoundingBox = \
            get_bounding_square_from_point(coord=Coordinate(41.977000, -87.908167),
                                           radius_miles=radius_miles)
        assert box == expected


class TestGetPointFromDistanceAndBearing:

    @pytest.mark.parametrize("coord,expected", [
        (Coordinate(41.977000, 87.908167), Coordinate(41.976836, 88.10284)),
        (Coordinate(41.977000, -87.908167), Coordinate(41.976836, -87.713494)),
        (Coordinate(-41.977000, 87.908167), Coordinate(-41.976836, 88.10284)),
        (Coordinate(-41.977000, -87.908167), Coordinate(-41.976836, -87.713494)),
        (Coordinate(0, 87.908167), Coordinate(0.0, 88.05289)),
        (Coordinate(41.977000, 0), Coordinate(41.976836, 0.194673)),
        (Coordinate(0, 0), Coordinate(0.0, 0.144723)),
    ])
    def test_lat_lon_input(self, coord, expected):
        result = get_point_from_distance_and_bearing(coord=coord, distance_miles=10, bearing_degrees=90)
        assert result == expected

    @pytest.mark.parametrize("dist,expected", [
        (10, Coordinate(41.976836, -87.713494)),
        (.1, Coordinate(41.977000, -87.90622)),
        (0, Coordinate(41.977000, -87.908167)),
        (-10, Coordinate(41.976836, -88.10284)),
    ])
    def test_distance_input(self, dist, expected):
        result = get_point_from_distance_and_bearing(coord=Coordinate(41.977000, -87.908167),
                                                     distance_miles=dist, bearing_degrees=90)
        assert result == expected

    @pytest.mark.parametrize("bearing,expected", [
        (0, Coordinate(42.121723, -87.908167)),
        (8.4, Coordinate(42.120167, -87.879664)),
        (25, Coordinate(42.108134, -87.825725)),
        (90, Coordinate(41.976836, -87.713494)),
        (134.7, Coordinate(41.87512, -87.770014)),
        (271, Coordinate(41.979361, -88.102818)),
        (360, Coordinate(42.121723, -87.908167)),
    ])
    def test_bearing_input(self, bearing, expected):
        result = get_point_from_distance_and_bearing(coord=Coordinate(41.977000, -87.908167),
                                                     distance_miles=10, bearing_degrees=bearing)
        assert result == expected


class TestGetBearingBetweenPoints:

    @pytest.mark.parametrize("coord_a,coord_b,expected", [
        (Coordinate(41.977000, -87.908167), Coordinate(42.121723, -87.908167), 0),
        (Coordinate(41.977000, -87.908167), Coordinate(42.120167, -87.879664), 8.4),
        (Coordinate(41.977000, -87.908167), Coordinate(42.108134, -87.825725), 25),
        (Coordinate(41.977000, -87.908167), Coordinate(41.976836, -87.713494), 90),
        (Coordinate(41.977000, -87.908167), Coordinate(41.87512, -87.770014), 134.7),
        (Coordinate(41.977000, -87.908167), Coordinate(41.979361, -88.102818), 271),
    ])
    def test_lat_lon_input(self, coord_a, coord_b, expected):
        result = get_bearing_between_points(coord_a, coord_b)
        assert result == expected
