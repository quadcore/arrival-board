import pytest

from arrivalboard.latlon import Coordinate as Coord
from arrivalboard.latlon import get_bearing_between_points
from arrivalboard.latlon import get_distance_between_points
from arrivalboard.latlon import get_perpendicular_bearing_between_points
from arrivalboard.latlon import get_point_from_distance_and_bearing


# class TestGetBoundingSquareFromPoint:

#     @pytest.mark.parametrize("coord,expected", [
#         (Coord(41.977000, 87.908167), Bbox(41.874583, 87.770733, 42.079252, 88.046044)),
#         (Coord(41.977000, -87.908167), Bbox(41.874583, -88.045601, 42.079252, -87.77029)),
#         (Coord(-41.977000, 87.908167), Bbox(-42.079252, 87.77029, -41.874583, 88.045601)),
#         (Coord(-41.977000, -87.908167), Bbox(-42.079252, -88.046044, -41.874583, -87.770733)),
#         (Coord(0, 87.908167), Bbox(-0.102334, 87.805832, 0.102334, 88.010502)),
#         (Coord(41.977000, 0), Bbox(41.874583, -0.137434, 42.079252, 0.137877)),
#         (Coord(0, 0), Bbox(-0.102334, -0.102335, 0.102334, 0.102335)),
#     ])
#     def test_lat_lon_input(self, coord, expected):
#         box: Bbox = get_bounding_square_from_point(coord=coord, radius_miles=10)
#         assert box == expected

#     @pytest.mark.parametrize("radius_miles,expected", [
#         (10, Bbox(41.874583, -88.045601, 42.079252, -87.77029)),
#         (.1, Bbox(41.975977, -87.909544, 41.978023, -87.90679)),
#         (0, Bbox(41.977000, -87.908167, 41.977000, -87.908167)),
#         (-10, Bbox(42.079252, -87.77029, 41.874583, -88.045601))
#     ])
#     def test_radius_miles_input(self, radius_miles, expected):
#         box: Bbox = \
#             get_bounding_square_from_point(coord=Coord(41.977000, -87.908167),
#                                            radius_miles=radius_miles)
#         assert box == expected


class TestGetPointFromDistanceAndBearing:

    @pytest.mark.parametrize("coord,expected", [
        (Coord(41.977000, 87.908167), Coord(41.976836, 88.10284)),
        (Coord(41.977000, -87.908167), Coord(41.976836, -87.713494)),
        (Coord(-41.977000, 87.908167), Coord(-41.976836, 88.10284)),
        (Coord(-41.977000, -87.908167), Coord(-41.976836, -87.713494)),
        (Coord(0, 87.908167), Coord(0.0, 88.05289)),
        (Coord(41.977000, 0), Coord(41.976836, 0.194673)),
        (Coord(0, 0), Coord(0.0, 0.144723)),
    ])
    def test_lat_lon_input(self, coord, expected):
        result = get_point_from_distance_and_bearing(
            coord=coord, distance_miles=10, bearing_degrees=90)
        assert result == expected

    @pytest.mark.parametrize("dist,expected", [
        (10, Coord(41.976836, -87.713494)),
        (.1, Coord(41.977000, -87.90622)),
        (0, Coord(41.977000, -87.908167)),
        (-10, Coord(41.976836, -88.10284)),
    ])
    def test_distance_input(self, dist, expected):
        result = get_point_from_distance_and_bearing(
            coord=Coord(41.977000, -87.908167), distance_miles=dist, bearing_degrees=90)
        assert result == expected

    @pytest.mark.parametrize("bearing,expected", [
        (0, Coord(42.121723, -87.908167)),
        (8.4, Coord(42.120167, -87.879664)),
        (25, Coord(42.108134, -87.825725)),
        (90, Coord(41.976836, -87.713494)),
        (134.7, Coord(41.87512, -87.770014)),
        (271, Coord(41.979361, -88.102818)),
        (360, Coord(42.121723, -87.908167)),
    ])
    def test_bearing_input(self, bearing, expected):
        result = get_point_from_distance_and_bearing(
            coord=Coord(41.977000, -87.908167), distance_miles=10, bearing_degrees=bearing)
        assert result == expected


class TestGetDistanceBetweenPoints:

    @pytest.mark.parametrize("coord_a,coord_b,expected", [
        (Coord(41.977000, -87.908167), Coord(42.113285, -87.90182), 9.42),
        (Coord(41.977000, -87.908167), Coord(41.88268, -87.623317), 16.03),
        (Coord(41.977000, -87.908167), Coord(41.977100, -87.908267), 0.01),
        (Coord(41.977000, -87.908167), Coord(41.977000, -87.908167), 0),
    ])
    def test_lat_lon_input(self, coord_a, coord_b, expected):
        result = get_distance_between_points(coord_a, coord_b)
        assert result == expected


class TestGetBearingBetweenPoints:

    @pytest.mark.parametrize("coord_a,coord_b,expected", [
        (Coord(41.977000, -87.908167), Coord(42.121723, -87.908167), 360.0),
        (Coord(41.977000, -87.908167), Coord(42.120167, -87.879664), 8.4),
        (Coord(41.977000, -87.908167), Coord(42.108134, -87.825725), 25.0),
        (Coord(41.977000, -87.908167), Coord(41.976836, -87.713494), 90.0),
        (Coord(41.977000, -87.908167), Coord(41.87512, -87.770014), 134.7),
        (Coord(41.977000, -87.908167), Coord(41.979361, -88.102818), 271.0),
    ])
    def test_lat_lon_input(self, coord_a, coord_b, expected):
        result = get_bearing_between_points(coord_a, coord_b)
        assert result == expected


class TestGetPerpendicularBearingBetweenPoints:

    @pytest.mark.parametrize("coord_a,coord_b,expected", [
        (Coord(41.966043, -87.891822), Coord(41.967043, -87.891822), (90.0, 270.0)),     # S to N
        (Coord(41.966043, -87.891822), Coord(41.965043, -87.891822), (270.0, 90.0)),     # N to S
        (Coord(41.966043, -87.891822), Coord(41.966043, -87.892822), (360.0, 180.0)),    # E to W
        (Coord(41.966043, -87.891822), Coord(41.966043, -87.890822), (180.0, 360.0)),    # W to E
        (Coord(41.966043, -87.891822), Coord(41.967043, -87.892822), (53.37, 233.37)),   # SE to NW
        (Coord(41.966043, -87.891822), Coord(41.965043, -87.890822), (233.37, 53.37)),   # NW to SE
        (Coord(41.966043, -87.891822), Coord(41.967043, -87.890822), (126.63, 306.63)),  # SW to NE
        (Coord(41.966043, -87.891822), Coord(41.965043, -87.892822), (306.63, 126.63)),  # NE to SW
    ])
    def test_lat_lon_input(self, coord_a, coord_b, expected):
        result = get_perpendicular_bearing_between_points(coord_a, coord_b)
        assert result == expected
