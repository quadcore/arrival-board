from dataclasses import dataclass

from arrivalboard.aircraft.models import Aircraft
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
        self._threshold_degrees = \
            latlon.get_bearing_between_points(self._threshold_a, self._threshold_b)

        self.designator = designator.replace("-", "")
        self.heading = int(designator.split("-")[0]) * 10
        self.true_heading = self._calculate_true_heading()
        self.final_bounds = self._calculate_final_bounds()

    def _calculate_true_heading(self) -> float:
        perp_bearing: tuple[float, float] = \
            latlon.get_perpendicular_bearing_between_points(self._threshold_a, self._threshold_b)

        # The threshold's perpendicular bearing that is closest to the runway's heading
        # is the runway's true heading.
        if abs(self.heading - perp_bearing[0]) < abs(self.heading - perp_bearing[1]):
            return perp_bearing[0]
        else:
            return perp_bearing[1]

    def _calculate_final_bounds(self) -> BoundingBox:
        if self._threshold_degrees > 180:
            offset_a_degrees = (self._threshold_degrees + 180) - 360
        else:
            offset_a_degrees = self._threshold_degrees + 180

        offset_a = latlon.get_point_from_distance_and_bearing(
            coord=self._threshold_a,
            distance_miles=0.1,
            bearing_degrees=offset_a_degrees)

        offset_b = latlon.get_point_from_distance_and_bearing(
            coord=self._threshold_b,
            distance_miles=0.1,
            bearing_degrees=self._threshold_degrees)

        inverted_true_heading = self.true_heading + 180
        if inverted_true_heading > 360:
            inverted_true_heading -= 360

        final_b = latlon.get_point_from_distance_and_bearing(
            coord=offset_b,
            distance_miles=15,
            bearing_degrees=inverted_true_heading)

        return BoundingBox(offset_a, final_b)

    def is_aircraft_lined_up(self, aircraft: Aircraft) -> bool:
        if not aircraft.track - 2 < self.true_heading < aircraft.track + 2:
            return False

        coord_a = self.final_bounds.coord_a
        coord_b = self.final_bounds.coord_b

        lat_min = min(coord_a.lat, coord_b.lat)
        lat_max = max(coord_a.lat, coord_b.lat)
        lon_min = min(coord_a.lon, coord_b.lon)
        lon_max = max(coord_a.lon, coord_b.lon)

        if lat_min <= aircraft.lat <= lat_max and lon_min <= aircraft.lon <= lon_max:
            return True

        return False

    def __repr__(self):
        return self.designator


@dataclass
class Airport:
    icao_code: str
    name: str
    lat: float
    lon: float
    runways: dict[str, Runway]
