from dataclasses import dataclass
from typing import List

import requests
from requests.auth import HTTPBasicAuth

from data.adsb import ADSBSource
from config import APP_CONFIG
from models.aircraft import Aircraft


class OpenSkyApi(ADSBSource):

    def __init__(self):
        self.base_url: str = APP_CONFIG["opensky"]["base_url"]
        self.username: str = APP_CONFIG["opensky"]["credentials"]["username"]
        self.password: str = APP_CONFIG["opensky"]["credentials"]["password"]

    def get_aircraft(self,
                     lat_min: float,
                     lon_min: float,
                     lat_max: float,
                     lon_max: float) -> List[Aircraft]:
        full_url = self.base_url + "/states/all"

        resp = requests.get(
            full_url,
            auth=HTTPBasicAuth(self.username, self.password),
            params={
                "lamin": lat_min,
                "lomin": lon_min,
                "lamax": lat_max,
                "lomax": lon_max, 
            })
        
        json_dict = resp.json()

        return self._parse_state_vectors(json_dict["states"])

    def _parse_state_vectors(self, state_vectors: List[object]) -> List[Aircraft]:
        aircraft: List[Aircraft] = []

        for v in state_vectors:
            cleaned_data = {
                "callsign": v[1].strip(),
                "baro_alt_ft": v[7] * 3.28084,
                "ground_speed": v[9] * 1.94384,
                "vert_rate_ftm": v[11] * 3.28084 * 60,
            }
            aircraft.append(
                Aircraft(**cleaned_data)
            )

        return aircraft
