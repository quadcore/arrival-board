from dataclasses import dataclass


@dataclass
class BoundingSquare:
    lat_min: float
    lon_min: float
    lat_max: float
    lon_max: float


def get_bounding_square_from_point(lat: float, lon: float, radius: int) -> BoundingSquare:
    lat_deg, lat_mins, lat_secs = to_deg_min_sec(lat)
    lon_deg, lon_mins, lon_secs = to_deg_min_sec(lon)

    lat_dist_secs = _distance_to_secs(radius, 101)
    lon_dist_secs = _distance_to_secs(radius, 80)

    lat_mins_diff = int(lat_dist_secs / 60)
    lat_secs_diff = lat_dist_secs - (lat_mins_diff * 60)

    lon_mins_diff = int(lon_dist_secs / 60)
    lon_secs_diff = lon_dist_secs - (lon_mins_diff * 60)

    return BoundingSquare(
        lat_min=to_decimal(lat_deg, lat_mins - lat_mins_diff, lat_secs - lat_secs_diff),
        lon_min=to_decimal(lon_deg, lon_mins - lon_mins_diff, lon_secs - lon_secs_diff),
        lat_max=to_decimal(lat_deg, lat_mins + lat_mins_diff, lat_secs + lat_secs_diff),
        lon_max=to_decimal(lon_deg, lon_mins + lon_mins_diff, lon_secs + lon_secs_diff),
    )


def _distance_to_secs(radius: int, feet_per_sec: int) -> float:
    radius_ft = radius * 5280
    return round(radius_ft / feet_per_sec, 4)


def to_deg_min_sec(coord: float) -> (int, int, int):
    deg = int(coord)
    min = int((coord - deg) * 60)
    sec = int((round((coord - deg) * 60, 4) - min) * 60)
    return (deg, min, sec)


def to_decimal(deg: int, min: int, sec: int) -> float:
    return (((sec / 60) + min) / 60) + deg
