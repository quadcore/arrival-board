from dataclasses import dataclass

import latlon


class Runway:

    def __init__(self,
                 number: str,
                 threshold_lat_a: float,
                 threshold_lon_a: float,
                 threshold_lat_b: float,
                 threshold_lon_b: float):
        self._threshold_lat_a = threshold_lat_a
        self._threshold_lon_a = threshold_lon_a
        self._threshold_lat_b = threshold_lat_b
        self._threshold_lon_b = threshold_lon_b

        self.number = number
        self.final_bounds = self._get_final_bounds()

    def _get_final_bounds(self) -> latlon.BoundingBox:
        threshold_degrees = self._get_threshold_degrees()

        if threshold_degrees > 180:
            offset_a_degrees= (threshold_degrees + 180) - 360
        else:
            offset_a_degrees = threshold_degrees + 180

        offset_lat_a, offset_lon_a = latlon.get_point_from_distance_and_bearing(
            lat=self._threshold_lat_a,
            lon=self._threshold_lon_a,
            distance_miles=0.1,
            bearing_degrees=offset_a_degrees)

        offset_lat_b, offset_lon_b = latlon.get_point_from_distance_and_bearing(
            lat=self._threshold_lat_b,
            lon=self._threshold_lon_b,
            distance_miles=0.1,
            bearing_degrees=threshold_degrees)

        threshold_perpendicular_degrees = self._get_threshold_perpendicular_degrees(threshold_degrees)

        final_lat_b, final_lon_b = latlon.get_point_from_distance_and_bearing(
            lat=offset_lat_b,
            lon=offset_lon_b,
            distance_miles=20,
            bearing_degrees=threshold_perpendicular_degrees)

        lat_min = offset_lat_a if offset_lat_a < final_lat_b else final_lat_b
        lon_min = offset_lon_a if offset_lon_a < final_lon_b else final_lon_b
        lat_max = offset_lat_a if offset_lat_a > final_lat_b else final_lat_b
        lon_max = offset_lon_a if offset_lon_a > final_lon_b else final_lon_b

        return latlon.BoundingBox(lat_min=lat_min,
                                  lon_min=lon_min,
                                  lat_max=lat_max,
                                  lon_max=lon_max)

    def _get_threshold_degrees(self):
        return latlon.get_bearing_between_points(
            lat_a=self._threshold_lat_a,
            lon_a=self._threshold_lon_a,
            lat_b=self._threshold_lat_b,
            lon_b=self._threshold_lon_b)

    def _get_threshold_perpendicular_degrees(self, threshold_degrees: float):
        runway_heading = int(self.number[:2]) * 10

        if runway_heading > 180:
            if threshold_degrees > 180:
                return abs(360 - (threshold_degrees + 90))
            else:
                return threshold_degrees - 90
        else:
            if threshold_degrees > 180:
                return threshold_degrees - 90
            else:
                return threshold_degrees + 90


@dataclass
class Airport:
    icao_code: str
    name: str
    lat: float
    lon: float
    runways: dict[str, Runway]
