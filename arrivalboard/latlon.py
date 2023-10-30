from dataclasses import dataclass
import math

# Formulas courtesy of http://www.movable-type.co.uk/scripts/latlong.html

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
    la1 = math.radians(lat_a)
    lo1 = math.radians(lon_a)
    la2 = math.radians(lat_b)
    lo2 = math.radians(lon_b)
    londelta = lo2 - lo1

    x = math.cos(la2) * math.sin(londelta)
    y = math.cos(la1) * math.sin(la2) - math.sin(la1) * math.cos(la2) * math.cos(londelta)
    brng = math.atan2(x, y)

    return (brng * 180 / math.pi + 360) % 360
