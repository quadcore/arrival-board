from abc import ABC
from abc import abstractmethod
import os
import tomllib

from arrivalboard.airport.models import Airport
from arrivalboard.airport.models import Runway
from arrivalboard.config import APP_CONFIG
from arrivalboard.latlon import Coordinate


class AirportSource(ABC):

    @abstractmethod
    def get_airports(self) -> dict[str, Airport]:
        pass


class AirportTomlReader(AirportSource):

    def __init__(self):
        folder_path = APP_CONFIG["datasources"]["airports"]["toml"]["folder"]
        self.filenames = [os.path.join(folder_path, f) for f in os.listdir(folder_path)]

    def get_airports(self) -> dict[str, Airport]:
        airports = {}

        for filename in self.filenames:
            with open(filename, "rb") as a:
                data = tomllib.load(a)
                airport = self._parse_airport(data)
                airports[airport.icao_code] = airport

        return airports
    
    def _parse_airport(self, airport_dict) -> Airport:
        runways = {}

        for r in airport_dict["runways"].items():
            number = r[0]
            threshold_a = Coordinate.from_list(r[1]["threshold_a"])
            threshold_b = Coordinate.from_list(r[1]["threshold_b"])
            runway = Runway(number, threshold_a, threshold_b)
            runways[runway.designator] = runway

        airport_dict["runways"] = runways

        return Airport(**airport_dict)
