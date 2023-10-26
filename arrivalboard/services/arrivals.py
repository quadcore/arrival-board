from typing import List

from data.adsb import ADSBSource
from models.aircraft import Aircraft


class ArrivalsService:

    def __init__(self, adsb_source: ADSBSource):
        self.adsb_source = adsb_source

    def get_aircraft(self) -> List[Aircraft]:
        return self.adsb_source.get_aircraft(lat_min=41.96435457528524,
                                             lon_min=-87.89027314349802,
                                             lat_max=41.9671407283871,
                                             lon_max=-87.69732051942088)
