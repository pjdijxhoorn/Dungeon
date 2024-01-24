from app.services.training import calculate_base_score, calculate_average_speed
import unittest

class UnitTests(unittest.TestCase):

    def test_average_speed_calculation(self):
        # ARRANGE
        distance_in_meters = 10000
        time_in_seconds = 3600
        # ACT
        result = calculate_average_speed(distance_in_meters, time_in_seconds)
        # ASSERT
        self.assertEqual(result, 39)

    def test_base_score_calculation(self):
        # ARRANGE
        distance_in_meters = 10000
        kilometer_per_hour = 10
        # ACT
        result = calculate_base_score(distance_in_meters, kilometer_per_hour)
        # ASSERT
        self.assertEqual(result, 10000)