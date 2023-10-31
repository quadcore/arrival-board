from arrivalboard.data.adsb import ADSBSource
from arrivalboard.data.airport import AirportSource
from arrivalboard.models.aircraft import Aircraft
from arrivalboard.models.airport import Airport
from arrivalboard.models.airport import Runway


class ArrivalsService:

    def __init__(self, adsb_source: ADSBSource, airport_source: AirportSource):
        self.adsb_source = adsb_source
        self.airports = airport_source.get_airports()

    def get_aircraft_by_runway(self, airport_icao_code: str) -> dict[str, Aircraft]:
        airport = self.airports[airport_icao_code]
        aircraft = self.adsb_source.get_aircraft(airport)

        runway_aircraft = {}
        for runway in airport.runways.values():
            runway_aircraft[runway.number] = []

        # TODO: Optimize this code
        for aircraft in aircraft:
            for runway in airport.runways.values():
                if self._is_on_final(aircraft, runway):
                    runway_aircraft[runway.number].append(aircraft)
                    continue

        return runway_aircraft

    def _is_on_final(self, aircraft: Aircraft, runway: Runway, ):
        if runway.final_bounds.lat_min <= aircraft.lat <= runway.final_bounds.lat_max and \
                runway.final_bounds.lon_min <= aircraft.lon <= runway.final_bounds.lon_max:
            return True

        return False
