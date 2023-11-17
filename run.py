from arrivalboard.aircraft.data import AdsbFi
from arrivalboard.airport.data import AirportTomlReader
from arrivalboard.config import APP_CONFIG
from arrivalboard.config import init_config
from arrivalboard.traffic import proximity_sorter
from arrivalboard.traffic import Traffic


def run():
    init_config(app_config_filepath="config/arrivalboard.toml")

    print(f"Running with application config:\n{APP_CONFIG}\n")

    airport_source = AirportTomlReader()
    airport = airport_source.get_airports()["KORD"]

    traffic = Traffic(adsb_source=AdsbFi())
    sorter = proximity_sorter(airport)

    aircraft = traffic.resolve_by_runway(airport=airport, sorter_func=sorter)

    print(aircraft)


if __name__ == "__main__":
    run()
