from dataclasses import dataclass
from typing import List


@dataclass
class Runway:
    final_lat_min: float
    final_lon_min: float
    final_lat_max: float
    final_lon_max: float


@dataclass
class Airport:
    callsign: str
    runways: List[Runway]
