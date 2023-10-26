from dataclasses import dataclass
from typing import List

import requests
from requests.auth import HTTPBasicAuth

from config import APP_CONFIG
from data.adsb import ADSBSource
from helpers import latlon
from models.aircraft import Aircraft
from models.airport import Airport


class OpenSkyApi(ADSBSource):

    def __init__(self):
        self.base_url: str = APP_CONFIG["opensky"]["base_url"]
        self.username: str = APP_CONFIG["opensky"]["credentials"]["username"]
        self.password: str = APP_CONFIG["opensky"]["credentials"]["password"]

    def get_aircraft(self, airport: Airport) -> List[Aircraft]:
        area: latlon.BoundingSquare = \
            latlon.get_bounding_square_from_point(airport.lat, airport.lon, 10)

        full_url = self.base_url + "/states/all"

        resp = requests.get(
            full_url,
            auth=HTTPBasicAuth(self.username, self.password),
            params={
                "lamin": area.lat_min,
                "lomin": area.lon_min,
                "lamax": area.lat_max,
                "lomax": area.lon_max,
            })
        
        json_dict = resp.json()

        return self._parse_state_vectors(json_dict["states"])

    def _parse_state_vectors(self, state_vectors: List[object]) -> List[Aircraft]:
        aircraft: List[Aircraft] = []

        for v in state_vectors:
            # TODO: Handle this better
            try:
                cleaned_data = {
                    "callsign": v[1].strip(),
                    "baro_alt_ft": v[7] * 3.28084,
                    "ground_speed": v[9] * 1.94384,
                    "vert_rate_ftm": v[11] * 3.28084 * 60,
                }
                aircraft.append(
                    Aircraft(**cleaned_data)
                )
            except:
                pass

        return aircraft
