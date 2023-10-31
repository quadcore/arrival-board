from abc import ABC
from abc import abstractmethod

from arrivalboard.models.aircraft import Aircraft
from arrivalboard.models.airport import Airport


class ADSBSource(ABC):

    @abstractmethod
    def get_aircraft(self, airport: Airport) -> list[Aircraft]:
        pass
