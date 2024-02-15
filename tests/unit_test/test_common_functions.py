from datetime import date
from fastapi.testclient import TestClient
from app.utilities.common_functions import bmi_calculation, calculate_fitness_multiplier, \
    max_heart_frequency_calculation, reserve_heart_frequency_calculation, calculate_age
from main import app

Client = TestClient(app)


def test_bmi_calculation():
    """ Test the BMI calculation. """
    # ARRANGE
    height_in_m = 1.93
    weight_in_kg = 72
    # ACT
    result = bmi_calculation(height_in_m, weight_in_kg)
    # ASSERT
    assert result == 19.3294


def test_calculate_fitness_multiplier():
    """ Test the fitness multiplier calculation. """
    # ARRANGE
    bmi = 20
    hart_reserve_frequency = 150
    # ACT
    result = calculate_fitness_multiplier(bmi, hart_reserve_frequency)
    # ASSERT
    assert result == 0.12


def test_max_heart_frequency_calculation():
    """ Test the heart frequency calculation. """
    # ARRANGE
    age = 20
    # ACT
    result = max_heart_frequency_calculation(age)
    # ASSERT
    assert result == 200


def test_reserve_heart_frequency_calculation():
    """ Test the reserve heart frequency calculation. """
    # ARRANGE
    max_heart_frequency = 200
    rest_heart_frequency = 80
    # ACT
    result = reserve_heart_frequency_calculation(
        max_heart_frequency, rest_heart_frequency)
    # ASSERT
    assert result == 120


def test_calculate_age():
    """ Test age calculation function. """
    # ARRANGE
    date_of_birth = date(1990, 1, 1)
    # ACT
    result = calculate_age(date_of_birth)
    # ASSERT
    assert result == 34
