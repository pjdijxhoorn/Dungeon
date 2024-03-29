from fastapi.testclient import TestClient
from app.services.training import calculate_average_speed, calculate_base_score
from main import app

Client = TestClient(app)


def test_average_speed_calculation():
    """ Test the calculation of average speed. """
    # ARRANGE
    distance_in_meters = 10000
    time_in_seconds = 3600
    # ACT
    result = calculate_average_speed(distance_in_meters, time_in_seconds)
    # ASSERT
    assert result == 39


def test_base_score_calculation():
    """ Test the calculation of base score. """
    # ARRANGE
    distance_in_meters = 10000
    kilometer_per_hour = 10
    # ACT
    result = calculate_base_score(distance_in_meters, kilometer_per_hour)
    # ASSERT
    assert result == 10000
