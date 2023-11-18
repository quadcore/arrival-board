from typing import Callable

from arrivalboard import Airport
from arrivalboard import FlightService
from arrivalboard import Flight
from arrivalboard.aircraft.data import AdsbFi
from arrivalboard.airport.data import AirportTomlReader
from arrivalboard.config import APP_CONFIG
from arrivalboard.config import init_config
from arrivalboard.latlon import Coordinate
from arrivalboard.latlon import get_distance_between_points

# Everything here is temporary dev code.

def proximity_sorter(coord: Coordinate) -> Callable:
    """Return a function that will sort flights that are passed to it
    based on their distance to the specified coordinate.

    Keyword arguments:
    coord -- the Coordinate to calcuate the flight's distance from
    """
    def sorter(flight: Flight):
        other_coord = Coordinate(flight.aircraft.lat, flight.aircraft.lon)
        return get_distance_between_points(coord, other_coord)

    return sorter


class AirportView:

    def __init__(self, airport: Airport):
        self.airport = airport

    def get_formatted(self, flights: list[Flight], sorter_func: Callable) -> list[Flight]:
        results = flights.copy()

        if sorter_func:
            results.sort(key=sorter_func)

        return results


class RunwayView:

    def __init__(self, airport: Airport):
        self.airport = airport

    def get_formatted(self, flights: list[Flight],
                      sorter_func: Callable = None,
                      runway_designators: list[str] = None,) -> dict[str, Flight]:
        runway_flights: dict[str, list[Flight]] = {}

        runway_keys = [r.designator for r in self.airport.runways.values()]
        if runway_designators:
            runway_keys = runway_designators

        for k in runway_keys:
            runway_flights[k] = []

        for flight in flights:
            if flight.landing_runway.designator not in runway_keys:
                continue
            runway_flights[flight.landing_runway.designator].append(flight)

        if sorter_func:
            for flight in runway_flights.values():
                flight.sort(key=sorter_func)

        return runway_flights


def run():
    init_config(app_config_filepath="config/arrivalboard.toml")

    print(f"Running with application config:\n{APP_CONFIG}\n")

    airport_source = AirportTomlReader()
    airport = airport_source.get_airports()["KORD"]

    flight_service = FlightService(adsb_source=AdsbFi())
    flights = flight_service.get_arriving(airport)

    view = RunwayView(airport)

    sorter = proximity_sorter(coord=Coordinate(airport.lat, airport.lon))
    results = view.get_formatted(flights, sorter)

    print(results)


if __name__ == "__main__":
    run()
