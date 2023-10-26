from config import APP_CONFIG
from config import init as init_config
from data.airport_toml import AirportTomlSource
from data.opensky import OpenSkyApi
from services.arrivals import ArrivalsService


def run():
    init_config()
    
    print(f"Running with application config:\n{APP_CONFIG}\n")

    airport_source = AirportTomlSource()
    airports = airport_source.get_airports()

    arrivals = ArrivalsService(OpenSkyApi())
    aircraft = arrivals.get_aircraft(airports["KORD"].runways[0])

    for a in aircraft:
        print(a)


if __name__ == "__main__":
    run()
