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
        self._threshold_degrees = latlon.get_bearing_between_points(
            coord_a=self._threshold_a,
            coord_b=self._threshold_b)

        self.designator = designator.replace("-", "")
        self.heading = int(designator.split("-")[0]) * 10
        self.true_heading = self._calculate_true_heading()
        self.final_bounds = self._calculate_final_bounds()

    def _calculate_true_heading(self) -> float:
        perp_bearing: (float, float) = latlon.get_perpendicular_bearing_between_points(
            coord_a=self._threshold_a,
            coord_b=self._threshold_b)

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

    def __repr__(self):
        return self.designator


@dataclass
class Airport:
    icao_code: str
    name: str
    lat: float
    lon: float
    runways: dict[str, Runway]
