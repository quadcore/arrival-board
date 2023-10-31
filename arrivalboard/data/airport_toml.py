import os
import tomllib
from typing import Self

from arrivalboard.data.airport import AirportSource
from arrivalboard.exceptions import ConfigError
from arrivalboard.models.airport import Airport
from arrivalboard.models.airport import Runway


class AirportTomlSource(AirportSource):

    @classmethod
    def from_files(cls, folder_path: str) -> Self:
        filenames = [os.path.join(folder_path, f) for f in os.listdir(folder_path)]
        if not filenames:
            raise ConfigError("No airport configuration files found.")

        inst = cls()
        inst.filenames = filenames
        return inst

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
        runway_dict = {}

        for r in airport_dict["runways"].items():
            runway_dict["number"] = r[0]
            runway_dict.update(r[1])
            runways[r[0]] = Runway(**runway_dict)

        airport_dict["runways"] = runways

        return Airport(**airport_dict)
