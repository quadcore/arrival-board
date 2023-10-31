from arrivalboard.config import APP_CONFIG
from arrivalboard.config import init_config
from arrivalboard.data.airport_toml import AirportTomlSource
from arrivalboard.data.opensky import OpenSkyApi
from arrivalboard.services.arrivals import ArrivalsService


def run():
    init_config("config", "arrivalboard.toml")
    
    print(f"Running with application config:\n{APP_CONFIG}\n")

    arrivals = ArrivalsService(OpenSkyApi(), AirportTomlSource.from_files("config/airports"))
    aircraft = arrivals.get_aircraft_by_runway("KORD")

    print(aircraft)


if __name__ == "__main__":
    run()
