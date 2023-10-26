from dataclasses import dataclass


@dataclass
class Aircraft:
    callsign: str
    baro_alt_ft: float
    ground_speed: float
    vert_rate_ftm: float

    def __repr__(self):
        return f"""Callsign: {self.callsign}
Barometric Altitude (ft): {self.baro_alt_ft}
Ground Speed (kts): {self.ground_speed}
Vertical Rate (ft/m): {self.vert_rate_ftm}\n"""
