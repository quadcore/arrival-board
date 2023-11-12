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

    def __repr__(self):
        return f"{self.lat}, {self.lon}"


@dataclass
class BoundingBox:
    coord_a: Coordinate
    coord_b: Coordinate

    def __repr__(self):
        return f"{self.coord_a.lat}, {self.coord_a.lon} {self.coord_b.lat}, {self.coord_b.lon}"


def get_bounding_square_from_point(coord: Coordinate,
                                   radius_miles: float) -> BoundingBox:
    """Return a square BoundingBox with the specified radius.

    Keyword arguments:
    coord -- the square's center point latitude/longitude
    radius_miles -- the radius of the square
    """
    # The NW point from the center of the square.
    coord_a = get_point_from_distance_and_bearing(coord, radius_miles, 315)
    # The SE point from the center of the square.
    coord_b = get_point_from_distance_and_bearing(coord, radius_miles, 135)

    return BoundingBox(coord_a, coord_b)


def get_point_from_distance_and_bearing(coord: Coordinate,
                                        distance_miles: float,
                                        bearing_degrees: float) -> Coordinate:
    """Return a point that is the specified distance and bearing
    from the input point.

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


def get_distance_between_points(coord_a: Coordinate,
                                coord_b: Coordinate) -> float:
    """Return a distance in miles between two points.

    Keyword arguments:
    coord a -- the latitude/longitude for point a
    coord b -- the latitude/longitude for point b
    """
    lat_a = math.radians(coord_a.lat)
    lat_b = math.radians(coord_b.lat)
    delta_lat = math.radians((coord_b.lat - coord_a.lat))
    delta_lon = math.radians((coord_b.lon - coord_a.lon))

    x = math.sin(delta_lat / 2) * math.sin(delta_lat / 2) + math.cos(lat_a) * math.cos(lat_b) * \
        math.sin(delta_lon / 2) * math.sin(delta_lon / 2)
    y = 2 * math.atan2(math.sqrt(x), math.sqrt(1 - x))

    return round(EARTH_RADIUS_MILES * y, 2)


def get_bearing_between_points(coord_a: Coordinate,
                               coord_b: Coordinate) -> float:
    """Return a bearing in degrees between two points.

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

    brng_deg = round((brng * 180 / math.pi + 360) % 360, 2)
    if brng_deg == 0.0:
        brng_deg = 360.0

    return brng_deg


def get_perpendicular_bearing_between_points(coord_a: Coordinate,
                                             coord_b: Coordinate) -> tuple[float, float]:
    """Return a tuple with the two perpendicular degree bearings (+90 degrees and
    -90 degrees) between two points.

    Keyword arguments:
    coord_a -- the latitude/longitude for point a
    coord_b -- the latitude/longitude for point b
    """
    brng = math.radians(get_bearing_between_points(coord_a, coord_b))

    perp_brng_a = brng + math.pi / 2
    perp_brng_b = brng - math.pi / 2

    perp_brng_a_deg = round((perp_brng_a * 180 / math.pi + 360) % 360, 2)
    perp_brng_b_deg = round((perp_brng_b * 180 / math.pi + 360) % 360, 2)

    if perp_brng_a_deg == 0.0:
        perp_brng_a_deg = 360.0
    if perp_brng_b_deg == 0.0:
        perp_brng_b_deg = 360.0

    return perp_brng_a_deg, perp_brng_b_deg
