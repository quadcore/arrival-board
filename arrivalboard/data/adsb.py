from abc import ABC
from abc import abstractmethod
from typing import List

from models.aircraft import Aircraft


class ADSBSource(ABC):

    @abstractmethod
    def get_aircraft(self,
                     lat_min: float,
                     lon_min: float,
                     lat_max: float,
                     lon_max: float) -> List[Aircraft]:
        pass
