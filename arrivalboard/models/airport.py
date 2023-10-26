from dataclasses import dataclass
from typing import List


@dataclass
class Runway:
    number: str
    final_lat_min: float
    final_lon_min: float
    final_lat_max: float
    final_lon_max: float


@dataclass
class Airport:
    icao_code: str
    name: str
    boundary_lat_min: float
    boundary_lon_min: float
    boundary_lat_max: float
    boundary_lon_max: float
    runways: List[Runway]
