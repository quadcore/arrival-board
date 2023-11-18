from dataclasses import dataclass


@dataclass
class Aircraft:
    callsign: str
    type: str
    baro_alt_ft: float
    vert_rate_ftm: float
    ground_speed: float
    track: int
    lat: float
    lon: float

    def __repr__(self):
        return f"""Callsign: {self.callsign}
Type: {self.type}
Barometric Altitude (ft): {self.baro_alt_ft}
Vertical Rate (ft/m): {self.vert_rate_ftm}
Ground Speed (kts): {self.ground_speed}
Track: {self.track}
Latitude: {self.lat}
Longitude: {self.lon}\n"""


@dataclass
class Flight:

    from arrivalboard.airport.models import Runway

    aircraft: Aircraft
    landing_runway: Runway
    origin: str
    destination: str
