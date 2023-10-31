import os
import tomllib

from arrivalboard.data.airport import AirportSource
from arrivalboard.models.airport import Airport
from arrivalboard.models.airport import Runway


class AirportTomlSource(AirportSource):

    def get_airports(self) -> dict[str, Airport]:
        airports = {}

        for filename in os.listdir("config/airports"):
            with open(os.path.join("config/airports", filename), "rb") as a:
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
