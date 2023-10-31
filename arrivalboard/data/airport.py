from abc import ABC
from abc import abstractmethod

from arrivalboard.models.airport import Airport


class AirportSource(ABC):

    @abstractmethod
    def get_airports(self) -> dict[str, Airport]:
        pass
