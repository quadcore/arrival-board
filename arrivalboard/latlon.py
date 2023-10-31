from dataclasses import dataclass
import math

# Formulas courtesy of http://www.movable-type.co.uk/scripts/latlong.html
#
# Encapsulating all lat/lon related calculations in this module. If things
# get more complex in the future and we need to rely on an external dependency
# for calculations, we can refactor.

EARTH_RADIUS_MILES = 3959


@dataclass
class BoundingBox:
    lat_min: float
    lon_min: float
    lat_max: float
    lon_max: float


def get_bounding_square_from_point(lat: float,
                                   lon: float,
                                   radius_miles: float) -> BoundingBox:
    """Return a square BoundingBox with the specified radius.

    Keyword arguments:
    lat -- the center point's latitude
    lon -- the center point's longitude
    radius_miles -- the radius of the square
    """
    lat_min, lon_min = get_point_from_distance_and_bearing(lat, lon, radius_miles, 225)
    lat_max, lon_max = get_point_from_distance_and_bearing(lat, lon, radius_miles, 45)

    return BoundingBox(
        lat_min=lat_min,
        lon_min=lon_min,
        lat_max=lat_max,
        lon_max=lon_max)


def get_point_from_distance_and_bearing(lat: float,
                                        lon: float,
                                        distance_miles: float,
                                        bearing_degrees: float) -> (float, float):
    """Return a lat/lon coordinate that is the specified distance and bearing
    from the input lat/lon point.

    Keyword arguments:
    lat -- the input latitude
    lon -- the input longitude
    distance_miles -- the distance in miles for the resulting point
    bearing_degrees -- the bearing in degrees for the resulting point
    """
    dist = distance_miles / EARTH_RADIUS_MILES
    brng = math.radians(bearing_degrees)
    la = math.radians(lat)
    lo = math.radians(lon)

    new_la = math.asin(math.sin(la) * math.cos(dist) + math.cos(la) * math.sin(dist) * math.cos(brng))
    new_lo = lo + math.atan2(math.sin(brng) * math.sin(dist) * math.cos(la), math.cos(dist) - math.sin(la) * math.sin(new_la))

    return round(math.degrees(new_la), 6), round(math.degrees(new_lo), 6)


def get_bearing_between_points(lat_a: float,
                               lon_a: float,
                               lat_b: float,
                               lon_b: float) -> float:
    """Return a bearing in degrees between lat/lon point a and lat/lon point b.

    Keyword arguments:
    lat_a -- the latitude for point a
    lon_a -- the longitude for point a
    lat_b -- the latitude for point b
    lon_b -- the longitude for point b
    """
    la1 = math.radians(lat_a)
    lo1 = math.radians(lon_a)
    la2 = math.radians(lat_b)
    lo2 = math.radians(lon_b)
    londelta = lo2 - lo1

    x = math.cos(la2) * math.sin(londelta)
    y = math.cos(la1) * math.sin(la2) - math.sin(la1) * math.cos(la2) * math.cos(londelta)
    brng = math.atan2(x, y)

    return round((brng * 180 / math.pi + 360) % 360, 2)
