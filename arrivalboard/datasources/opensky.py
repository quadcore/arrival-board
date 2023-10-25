from dataclasses import dataclass

import requests
from requests.auth import HTTPBasicAuth

from config import APP_CONFIG


@dataclass
class StateVector:
    callsign: str
    baro_altitude: float


class OpenSkyApi:

    def __init__(self):
        self.base_url = APP_CONFIG["opensky"]["base_url"]
        self.username = APP_CONFIG["opensky"]["credentials"]["username"]
        self.password = APP_CONFIG["opensky"]["credentials"]["password"]

    def get_state_vectors(self):
        full_url = self.base_url + "/states/all"

        resp = requests.get(
            full_url,
            auth=HTTPBasicAuth(self.username, self.password),
            params={
                "lamin": "41.96435457528524",
                "lomin": "-87.89027314349802",
                "lamax": "41.9671407283871",
                "lomax": "-87.69732051942088", 
            })
        
        json_dict = resp.json()

        return self._parse_state_vectors(json_dict["states"])

    def _parse_state_vectors(self, state_vectors):
        vectors = []

        for v in state_vectors:
            vectors.append(
                StateVector(v[1].strip(), v[7])
            )

        return vectors
