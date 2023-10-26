from abc import ABC
from abc import abstractmethod
from typing import Dict

from models.airport import Airport


class AirportSource(ABC):

    @abstractmethod
    def get_airports(self) -> Dict[str, Airport]:
        pass
