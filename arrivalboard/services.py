from arrivalboard.aircraft.data import ADSBSource
from arrivalboard.aircraft.models import Flight
from arrivalboard.airport.models import Airport


class FlightService:

    def __init__(self, adsb_source: ADSBSource):
        self.adsb_source = adsb_source

    def get_arriving(self, airport: Airport) -> list[Flight]:
        """Get flights that are arriving to the specified airport.

        Keyword arguments:
        airport -- the airport to get flights for
        """
        flights: list[Flight] = []

        adsb_aircraft = self.adsb_source.get_aircraft(airport)

        for aircraft in adsb_aircraft:
            if aircraft.baro_alt_ft in range(airport.elevation - 50, airport.elevation + 50) \
                    or aircraft.baro_alt_ft > airport.elevation + 5000:
                continue

            for runway in airport.runways.values():
                if runway.is_aircraft_lined_up(aircraft):
                    f = Flight(aircraft=aircraft,
                               landing_runway=runway,
                               origin="N/A",
                               destination="N/A")
                    flights.append(f)
                    continue

        return flights
