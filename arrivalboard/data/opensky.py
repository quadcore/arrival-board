from dataclasses import dataclass

from requests import Request
from requests import Session
from requests.auth import HTTPBasicAuth

from config import APP_CONFIG
from data.adsb import ADSBSource
import latlon
from models.aircraft import Aircraft
from models.airport import Airport


class OpenSkyApi(ADSBSource):

    def __init__(self):
        self.session = Session()
        self.base_url: str = APP_CONFIG["opensky"]["base_url"]

        try:
            self.username: str = APP_CONFIG["opensky"]["credentials"]["username"]
            self.password: str = APP_CONFIG["opensky"]["credentials"]["password"]
        except KeyError:
            # Default to non-authenticated requests.
            pass

    def get_aircraft(self, airport: Airport) -> list[Aircraft]:
        """Get aircraft within range of the specified airport.

        Keyword arguments:
        airport -- the airport to get aircraft for
        """
        # OpenSky works based on a bounding box so we create a square of a
        # specified size with its center being the airport's WGS84 coordinates.
        area: latlon.BoundingBox = \
            latlon.get_bounding_square_from_point(airport.lat, airport.lon, 15)

        url = self.base_url + "/states/all"
        params = {
            "lamin": area.lat_min,
            "lomin": area.lon_min,
            "lamax": area.lat_max,
            "lomax": area.lon_max,
        }

        req = Request("GET", url, params=params)
        if hasattr(self, "username") and hasattr(self, "password"):
            req.auth = HTTPBasicAuth(self.username, self.password)

        resp = self.session.send(req.prepare())
        json_dict = resp.json()

        return self._parse_state_vectors(json_dict["states"])

    def _parse_state_vectors(self, state_vectors: list[object]) -> list[Aircraft]:
        aircraft: list[Aircraft] = []

        for v in state_vectors:
            # TODO: Handle this better
            try:
                cleaned_data = {
                    "callsign": v[1].strip(),
                    "baro_alt_ft": v[7] * 3.28084,
                    "vert_rate_ftm": v[11] * 3.28084 * 60,
                    "ground_speed": v[9] * 1.94384,
                    "track": int(v[10]),
                    "lat": round(v[6], 6),
                    "lon": round(v[5], 6),
                }
                aircraft.append(
                    Aircraft(**cleaned_data)
                )
            except:
                pass

        return aircraft
