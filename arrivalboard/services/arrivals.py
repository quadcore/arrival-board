from typing import List

from data.adsb import ADSBSource
from models.aircraft import Aircraft
from models.airport import Runway


class ArrivalsService:

    def __init__(self, adsb_source: ADSBSource):
        self.adsb_source = adsb_source

    def get_aircraft(self, runway: Runway) -> List[Aircraft]:
        return self.adsb_source.get_aircraft(lat_min=runway.final_lat_min,
                                             lon_min=runway.final_lon_min,
                                             lat_max=runway.final_lat_max,
                                             lon_max=runway.final_lon_max)
