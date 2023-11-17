from abc import ABC
from abc import abstractmethod
import sys
from urllib.parse import urljoin

import requests
from requests import Request
from requests import Session
from requests.auth import HTTPBasicAuth

from arrivalboard.config import APP_CONFIG
from arrivalboard.aircraft.models import Aircraft
from arrivalboard.airport.models import Airport
from arrivalboard.latlon import BoundingBox
from arrivalboard.latlon import Coordinate
from arrivalboard.latlon import get_bounding_square_from_point


class ADSBSource(ABC):

    @abstractmethod
    def get_aircraft(self, airport: Airport) -> list[Aircraft]:
        pass


class AdsbFi(ADSBSource):

    def __init__(self):
        adsbfi_config = APP_CONFIG["datasources"]["adsb"]["adsbfi"]
        self.base_url: str = adsbfi_config["base_url"]

    def get_aircraft(self, airport: Airport) -> list[Aircraft]:
        url = urljoin(self.base_url, f"v2/lat/{airport.lat}/lon/{airport.lon}/dist/30")

        resp = requests.get(url)

        if resp.status_code != 200:
            sys.exit(f"adsb.fi error: {resp.status_code}")

        json_dict = resp.json()

        return self._parse_aircraft(json_dict["aircraft"])

    def _parse_aircraft(self, objects: list[object]) -> list[Aircraft]:
        def get_or_default(object):
            def inner(attr, default="N/A"):
                return object.get(attr, default)
            return inner

        aircraft = []

        for o in objects:
            get = get_or_default(o)

            baro_alt_ft = get("alt_baro", 0)
            if (baro_alt_ft == "ground"):
                # TODO: Set to airport elevation
                baro_alt_ft = 0

            cleaned_data = {
                "callsign": get("flight"),
                "type": get("desc"),
                "baro_alt_ft": baro_alt_ft,
                "vert_rate_ftm": get("baro_rate", 0),
                "ground_speed": get("gs", 0),
                "track": get("track", 0),
                "lat": get("lat", 0),
                "lon": get("lon", 0),
            }
            aircraft.append(
                Aircraft(**cleaned_data)
            )

        return aircraft


class OpenSkyApi(ADSBSource):

    def __init__(self):
        self.session = Session()

        opensky_config = APP_CONFIG["datasources"]["adsb"]["opensky"]
        self.base_url: str = opensky_config["base_url"]
        try:
            self.username: str = opensky_config["credentials"]["username"]
            self.password: str = opensky_config["credentials"]["password"]
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
        box: BoundingBox = get_bounding_square_from_point(Coordinate(airport.lat, airport.lon), 30)

        url = urljoin(self.base_url, "states/all")
        params = {
            "lamin": min(box.coord_a.lat, box.coord_b.lat),
            "lomin": min(box.coord_a.lon, box.coord_b.lon),
            "lamax": max(box.coord_a.lat, box.coord_b.lat),
            "lomax": max(box.coord_a.lon, box.coord_b.lon),
        }

        req = Request("GET", url, params=params)
        if hasattr(self, "username") and hasattr(self, "password"):
            req.auth = HTTPBasicAuth(self.username, self.password)

        resp = self.session.send(req.prepare())

        if resp.status_code != 200:
            sys.exit(f"OpenSky error: {resp.status_code}")

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
            except TypeError:
                pass

        return aircraft
