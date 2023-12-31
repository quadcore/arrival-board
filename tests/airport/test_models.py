import pytest

from arrivalboard.airport.models import Runway
from arrivalboard.latlon import Coordinate as Crd


class TestRunway:

    @pytest.mark.parametrize("heading,coord_a,coord_b,expected", [
        ("27", Crd(41.966043, -87.891822), Crd(41.967043, -87.891822), 270.0),   # S to N threshold
        ("09", Crd(41.966043, -87.891822), Crd(41.967043, -87.891822), 90.0),    # S to N
        ("27", Crd(41.966043, -87.891822), Crd(41.965043, -87.891822), 270.0),   # N to S
        ("09", Crd(41.966043, -87.891822), Crd(41.965043, -87.891822), 90.0),    # N to S
        ("18", Crd(41.966043, -87.891822), Crd(41.966043, -87.892822), 180.0),   # E to W
        ("36", Crd(41.966043, -87.891822), Crd(41.966043, -87.892822), 360.0),   # E to W
        ("05", Crd(41.966043, -87.891822), Crd(41.967043, -87.892822), 53.37),   # SE to NW
        ("23", Crd(41.966043, -87.891822), Crd(41.967043, -87.892822), 233.37),  # SE to NW
        ("12", Crd(41.966043, -87.891822), Crd(41.967043, -87.890822), 126.63),  # SW to NE
        ("30", Crd(41.966043, -87.891822), Crd(41.967043, -87.890822), 306.63),  # SW to NE
    ])
    def test_calculate_true_heading(self, heading, coord_a, coord_b, expected):
        runway = Runway(heading, coord_a, coord_b)
        assert runway.true_heading == expected
