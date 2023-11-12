import pytest

from arrivalboard import latlon
from arrivalboard.latlon import BoundingBox as Box
from arrivalboard.latlon import Coordinate as Crd


class TestGetBoundingSquareFromPoint:

    @pytest.mark.parametrize("coord,expected", [
        (Crd(41.977000, 87.908167), Box(Crd(42.079252, 87.77029), Crd(41.874583, 88.045601))),
        (Crd(41.977000, -87.908167), Box(Crd(42.079252, -88.046044), Crd(41.874583, -87.770733))),
        (Crd(-41.977000, 87.908167), Box(Crd(-41.874583, 87.770733), Crd(-42.079252, 88.046044))),
        (Crd(-41.977000, -87.908167), Box(Crd(-41.874583, -88.045601), Crd(-42.079252, -87.77029))),
        (Crd(0, 87.908167), Box(Crd(0.102334, 87.805832), Crd(-0.102334, 88.010502))),
        (Crd(41.977000, 0), Box(Crd(42.079252, -0.137877), Crd(41.874583, 0.137434))),
        (Crd(0, 0), Box(Crd(0.102334, -0.102335), Crd(-0.102334, 0.102335))),
    ])
    def test_lat_lon_input(self, coord, expected):
        box: Box = latlon.get_bounding_square_from_point(coord=coord, radius_miles=10)
        assert box == expected

    @pytest.mark.parametrize("radius_miles,expected", [
        (10, Box(Crd(42.079252, -88.046044), Crd(41.874583, -87.770733))),
        (.1, Box(Crd(41.978023, -87.909544), Crd(41.975977, -87.90679))),
        (0, Box(Crd(41.977000, -87.908167), Crd(41.977000, -87.908167))),
        (-10, Box(Crd(41.874583, -87.770733), Crd(42.079252, -88.046044))),
    ])
    def test_radius_miles_input(self, radius_miles, expected):
        box: Box = \
            latlon.get_bounding_square_from_point(coord=Crd(41.977000, -87.908167),
                                                  radius_miles=radius_miles)
        assert box == expected


class TestGetPointFromDistanceAndBearing:

    @pytest.mark.parametrize("coord,expected", [
        (Crd(41.977000, 87.908167), Crd(41.976836, 88.10284)),
        (Crd(41.977000, -87.908167), Crd(41.976836, -87.713494)),
        (Crd(-41.977000, 87.908167), Crd(-41.976836, 88.10284)),
        (Crd(-41.977000, -87.908167), Crd(-41.976836, -87.713494)),
        (Crd(0, 87.908167), Crd(0.0, 88.05289)),
        (Crd(41.977000, 0), Crd(41.976836, 0.194673)),
        (Crd(0, 0), Crd(0.0, 0.144723)),
    ])
    def test_lat_lon_input(self, coord, expected):
        result = latlon.get_point_from_distance_and_bearing(
            coord=coord, distance_miles=10, bearing_degrees=90)
        assert result == expected

    @pytest.mark.parametrize("dist,expected", [
        (10, Crd(41.976836, -87.713494)),
        (.1, Crd(41.977000, -87.90622)),
        (0, Crd(41.977000, -87.908167)),
        (-10, Crd(41.976836, -88.10284)),
    ])
    def test_distance_input(self, dist, expected):
        result = latlon.get_point_from_distance_and_bearing(
            coord=Crd(41.977000, -87.908167), distance_miles=dist, bearing_degrees=90)
        assert result == expected

    @pytest.mark.parametrize("bearing,expected", [
        (0, Crd(42.121723, -87.908167)),
        (8.4, Crd(42.120167, -87.879664)),
        (25, Crd(42.108134, -87.825725)),
        (90, Crd(41.976836, -87.713494)),
        (134.7, Crd(41.87512, -87.770014)),
        (271, Crd(41.979361, -88.102818)),
        (360, Crd(42.121723, -87.908167)),
    ])
    def test_bearing_input(self, bearing, expected):
        result = latlon.get_point_from_distance_and_bearing(
            coord=Crd(41.977000, -87.908167), distance_miles=10, bearing_degrees=bearing)
        assert result == expected


class TestGetDistanceBetweenPoints:

    @pytest.mark.parametrize("coord_a,coord_b,expected", [
        (Crd(41.977000, -87.908167), Crd(42.113285, -87.90182), 9.42),
        (Crd(41.977000, -87.908167), Crd(41.88268, -87.623317), 16.03),
        (Crd(41.977000, -87.908167), Crd(41.977100, -87.908267), 0.01),
        (Crd(41.977000, -87.908167), Crd(41.977000, -87.908167), 0),
    ])
    def test_lat_lon_input(self, coord_a, coord_b, expected):
        result = latlon.get_distance_between_points(coord_a, coord_b)
        assert result == expected


class TestGetBearingBetweenPoints:

    @pytest.mark.parametrize("coord_a,coord_b,expected", [
        (Crd(41.977000, -87.908167), Crd(42.121723, -87.908167), 360.0),
        (Crd(41.977000, -87.908167), Crd(42.120167, -87.879664), 8.4),
        (Crd(41.977000, -87.908167), Crd(42.108134, -87.825725), 25.0),
        (Crd(41.977000, -87.908167), Crd(41.976836, -87.713494), 90.0),
        (Crd(41.977000, -87.908167), Crd(41.87512, -87.770014), 134.7),
        (Crd(41.977000, -87.908167), Crd(41.979361, -88.102818), 271.0),
    ])
    def test_lat_lon_input(self, coord_a, coord_b, expected):
        result = latlon.get_bearing_between_points(coord_a, coord_b)
        assert result == expected


class TestGetPerpendicularBearingBetweenPoints:

    @pytest.mark.parametrize("coord_a,coord_b,expected", [
        (Crd(41.966043, -87.891822), Crd(41.967043, -87.891822), (90.0, 270.0)),     # S to N
        (Crd(41.966043, -87.891822), Crd(41.965043, -87.891822), (270.0, 90.0)),     # N to S
        (Crd(41.966043, -87.891822), Crd(41.966043, -87.892822), (360.0, 180.0)),    # E to W
        (Crd(41.966043, -87.891822), Crd(41.966043, -87.890822), (180.0, 360.0)),    # W to E
        (Crd(41.966043, -87.891822), Crd(41.967043, -87.892822), (53.37, 233.37)),   # SE to NW
        (Crd(41.966043, -87.891822), Crd(41.965043, -87.890822), (233.37, 53.37)),   # NW to SE
        (Crd(41.966043, -87.891822), Crd(41.967043, -87.890822), (126.63, 306.63)),  # SW to NE
        (Crd(41.966043, -87.891822), Crd(41.965043, -87.892822), (306.63, 126.63)),  # NE to SW
    ])
    def test_lat_lon_input(self, coord_a, coord_b, expected):
        result = latlon.get_perpendicular_bearing_between_points(coord_a, coord_b)
        assert result == expected
