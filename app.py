from arrivalboard.config import APP_CONFIG
from arrivalboard.config import init_config
from arrivalboard.data.airport_toml import AirportTomlSource
from arrivalboard.data.opensky import OpenSkyApi
from arrivalboard.services.arrivals import ArrivalsService


def run():
    init_config("config", "arrivalboard.toml")
    
    print(f"Running with application config:\n{APP_CONFIG}\n")

    airport_source = AirportTomlSource()
    airports = airport_source.get_airports()

    arrivals = ArrivalsService(OpenSkyApi())
    aircraft = arrivals.get_aircraft_by_runway(airports["KORD"])

    print(aircraft)


if __name__ == "__main__":
    run()
