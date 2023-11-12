from typing import Callable

from arrivalboard.aircraft.data import ADSBSource
from arrivalboard.aircraft.models import Aircraft
from arrivalboard.airport.models import Airport
from arrivalboard.airport.models import Runway
from arrivalboard.latlon import Coordinate
from arrivalboard.latlon import get_distance_between_points


def proximity_sorter(airport: Airport) -> Callable:
    """Return a function that will sort aircraft that are passed to it
    based on their distance to the specified airport.

    Keyword arguments:
    airport -- the airport to use for calculating the aircraft's distance"""
    def sorter(aircraft: Aircraft):
        coord_a = Coordinate(airport.lat, airport.lon)
        coord_b = Coordinate(aircraft.lat, aircraft.lon)
        return get_distance_between_points(coord_a, coord_b)

    return sorter


class Traffic:

    def __init__(self, adsb_source: ADSBSource):
        self.adsb_source = adsb_source

    def resolve_by_runway(self, airport: Airport, sorter_func: Callable) -> dict[str, Aircraft]:
        """Return aircraft traffic that is assigned to runways they are on approach to.

        Keyword arguments:
        airport -- the airport to get traffic for
        sorter_func -- function to use for sorting the list of aircraft resolved to each runway"""
        aircraft = self.adsb_source.get_aircraft(airport)

        runway_aircraft: dict[str, list[Aircraft]] = {}
        for runway in airport.runways.values():
            runway_aircraft[runway.designator] = []

        # TODO: Optimize this code
        for aircraft in aircraft:
            # TODO: Base this on field elevation
            if aircraft.baro_alt_ft < 670 or aircraft.baro_alt_ft > 5000:
                continue

            for runway in airport.runways.values():
                # TODO: Base this on constant setting that can be modified
                if not aircraft.track - 2 < runway.true_heading < aircraft.track + 2:
                    continue

                if self._is_lined_up(aircraft, runway):
                    runway_aircraft[runway.designator].append(aircraft)
                    continue

        for runway, aircraft in runway_aircraft.items():
            aircraft.sort(key=sorter_func)

        return runway_aircraft

    def _is_lined_up(self, aircraft: Aircraft, runway: Runway):
        coord_a = runway.final_bounds.coord_a
        coord_b = runway.final_bounds.coord_b

        lat_min = min(coord_a.lat, coord_b.lat)
        lat_max = max(coord_a.lat, coord_b.lat)
        lon_min = min(coord_a.lon, coord_b.lon)
        lon_max = max(coord_a.lon, coord_b.lon)

        if lat_min <= aircraft.lat <= lat_max and lon_min <= aircraft.lon <= lon_max:
            return True

        return False
