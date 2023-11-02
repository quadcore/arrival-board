from dataclasses import dataclass
import math
from typing import Self

# Formulas courtesy of http://www.movable-type.co.uk/scripts/latlong.html
#
# Encapsulating all lat/lon related calculations in this module. If things
# get more complex in the future and we need to rely on an external dependency
# for calculations, we can refactor.

EARTH_RADIUS_MILES = 3959


@dataclass
class Coordinate:
    lat: float
    lon: float

    @classmethod
    def from_list(cls, latlon_list: list[float, float]) -> Self:
        return cls(lat=latlon_list[0], lon=latlon_list[1])


@dataclass
class BoundingBox:
    lat_min: float
    lon_min: float
    lat_max: float
    lon_max: float


def get_bounding_square_from_point(coord: Coordinate,
                                   radius_miles: float) -> BoundingBox:
    """Return a square BoundingBox with the specified radius.

    Keyword arguments:
    coord -- the center point's latitude/longitude
    radius_miles -- the radius of the square
    """
    coord_min = get_point_from_distance_and_bearing(coord, radius_miles, 225)
    coord_max = get_point_from_distance_and_bearing(coord, radius_miles, 45)

    return BoundingBox(lat_min=coord_min.lat,
                       lon_min=coord_min.lon,
                       lat_max=coord_max.lat,
                       lon_max=coord_max.lon)


def get_point_from_distance_and_bearing(coord: Coordinate,
                                        distance_miles: float,
                                        bearing_degrees: float) -> Coordinate:
    """Return a coordinate that is the specified distance and bearing
    from the input coordinate.

    Keyword arguments:
    coord -- the input latitude/longitude
    distance_miles -- the distance in miles for the resulting point
    bearing_degrees -- the bearing in degrees for the resulting point
    """
    dist = distance_miles / EARTH_RADIUS_MILES
    brng = math.radians(bearing_degrees)
    lat = math.radians(coord.lat)
    lon = math.radians(coord.lon)

    new_lat = math.asin(
        math.sin(lat) * math.cos(dist) + math.cos(lat) * math.sin(dist) * math.cos(brng))
    new_lon = lon + math.atan2(
        math.sin(brng) * math.sin(dist) * math.cos(lat),
        math.cos(dist) - math.sin(lat) * math.sin(new_lat))

    return Coordinate(lat=round(math.degrees(new_lat), 6),
                      lon=round(math.degrees(new_lon), 6))


def get_bearing_between_points(coord_a: Coordinate,
                               coord_b: Coordinate) -> float:
    """Return a bearing in degrees between coordinate a and coordinate b.

    Keyword arguments:
    coord_a -- the latitude/longitude for point a
    coord_b -- the latitude/longitude for point b
    """
    lat_a = math.radians(coord_a.lat)
    lon_a = math.radians(coord_a.lon)
    lat_b = math.radians(coord_b.lat)
    lon_b = math.radians(coord_b.lon)
    londelta = lon_b - lon_a

    x = math.cos(lat_b) * math.sin(londelta)
    y = math.cos(lat_a) * math.sin(lat_b) - math.sin(lat_a) * math.cos(lat_b) * math.cos(londelta)
    brng = math.atan2(x, y)

    return round((brng * 180 / math.pi + 360) % 360, 2)
