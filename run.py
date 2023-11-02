from arrivalboard.aircraft.data import OpenSkyApi
from arrivalboard.airport.data import AirportTomlReader
from arrivalboard.config import APP_CONFIG
from arrivalboard.config import init_config
from arrivalboard.traffic import TrafficService


def run():
    init_config(app_config_filepath="config/arrivalboard.toml")

    print(f"Running with application config:\n{APP_CONFIG}\n")

    print("Test")

    traffic = TrafficService(adsb_source=OpenSkyApi(), airport_source=AirportTomlReader())
    aircraft = traffic.get_resolved_by_runway("KORD")

    print(aircraft)


if __name__ == "__main__":
    run()
