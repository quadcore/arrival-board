from dataclasses import dataclass

from arrivalboard.latlon import BoundingBox
from arrivalboard.latlon import Coordinate
import arrivalboard.latlon as latlon


class Runway:

    def __init__(self,
                 designator: str,
                 threshold_a: Coordinate,
                 threshold_b: Coordinate):
        self._threshold_a = threshold_a
        self._threshold_b = threshold_b

        self.designator = designator.replace("-", "")
        self.number = int(designator.split("-")[0]) * 10
        self.final_bounds = self._get_final_bounds()

    def _get_final_bounds(self) -> latlon.BoundingBox:
        threshold_degrees = self._get_threshold_degrees()

        if threshold_degrees > 180:
            offset_a_degrees= (threshold_degrees + 180) - 360
        else:
            offset_a_degrees = threshold_degrees + 180

        offset_a = latlon.get_point_from_distance_and_bearing(
            coord=self._threshold_a,
            distance_miles=0.1,
            bearing_degrees=offset_a_degrees)

        offset_b = latlon.get_point_from_distance_and_bearing(
            coord=self._threshold_b,
            distance_miles=0.1,
            bearing_degrees=threshold_degrees)

        threshold_perpendicular_degrees = self._get_threshold_perpendicular_degrees(threshold_degrees)

        final_b = latlon.get_point_from_distance_and_bearing(
            coord=offset_b,
            distance_miles=20,
            bearing_degrees=threshold_perpendicular_degrees)

        # TODO: Make this prettier
        lat_min = offset_a.lat if offset_a.lat < final_b.lat else final_b.lat
        lon_min = offset_a.lon if offset_a.lon < final_b.lon else final_b.lon
        lat_max = offset_a.lat if offset_a.lat > final_b.lat else final_b.lat
        lon_max = offset_a.lon if offset_a.lon > final_b.lon else final_b.lon

        return BoundingBox(lat_min=lat_min,
                           lon_min=lon_min,
                           lat_max=lat_max,
                           lon_max=lon_max)

    def _get_threshold_degrees(self):
        return latlon.get_bearing_between_points(
            coord_a=self._threshold_a,
            coord_b=self._threshold_b)

    def _get_threshold_perpendicular_degrees(self, threshold_degrees: float):
        if self.number > 180:
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
