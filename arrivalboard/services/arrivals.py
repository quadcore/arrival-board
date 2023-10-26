from typing import List

from data.adsb import ADSBSource
from models.aircraft import Aircraft
from models.airport import Airport
from models.airport import Runway


class ArrivalsService:

    def __init__(self, adsb_source: ADSBSource):
        self.adsb_source = adsb_source

    def get_aircraft(self, airport: Airport) -> List[Aircraft]:
        return self.adsb_source.get_aircraft(airport)
