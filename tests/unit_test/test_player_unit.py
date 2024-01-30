from fastapi.testclient import TestClient
from app.services.player import calculate_personal_average, calculate_training_score
from main import app

Client = TestClient(app)


def test_training_score_calculation():
    """ Test the calculation of training score. """
    # ARRANGE
    base_score = 100000
    fitness_multiplier = 0.1249
    # ACT
    result = calculate_training_score(base_score, fitness_multiplier)
    # ASSERT
    assert result == 1249


def test_calculate_personal_average():
    """ Test the calculation of personal average. """
    # ARRANGE
    training_score_list = [0, 1, 2, 3, 4, 5]
    # ACT
    result = calculate_personal_average(training_score_list)
    # ASSERT
    assert result == 15
