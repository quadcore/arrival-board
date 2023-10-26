from abc import ABC
from abc import abstractmethod
from typing import List

from models.aircraft import Aircraft
from models.airport import Airport


class ADSBSource(ABC):

    @abstractmethod
    def get_aircraft(self, airport: Airport) -> List[Aircraft]:
        pass
