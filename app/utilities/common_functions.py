import math
from datetime import date
from random import randint

from app.models.monster import Monster


def bmi_calculation(height_in_m, weight_in_kg):
    """ calculate the bmi by dividing the weight with the lengt sqaured. """
    bmi = weight_in_kg / (
        height_in_m ** 2)
    return round(bmi, 4)


def calculate_fitness_multiplier(bmi, hart_reserve_frequency):
    """ calculate the fitness multiplier by logging the bmi divided by the hart_reserve_frequency 
    and adding one to it to prevent it from becoming negative. """
    fitness_multiplier = math.log10(bmi / hart_reserve_frequency) + 1
    return round(fitness_multiplier, 2)


def max_heart_frequency_calculation(age):
    """ calculate the max heart frequency by substracting the 220 by the age of a person. """
    max_heart_frequency = 220 - age
    return max_heart_frequency


def reserve_heart_frequency_calculation(max_heart_frequency, rest_heart_frequency):
    """ calculate the reserve heart frequency by substracting 
    the rest heart freqeuncy from the max heart frequency. """
    reserve_heart_frequency = max_heart_frequency - rest_heart_frequency
    return reserve_heart_frequency


def calculate_age(date_of_birth: date):
    """ Calculate age based on the given date of birth. """
    current_date = date.today()
    age = current_date.year - date_of_birth.year - (
        (current_date.month, current_date.day) < (date_of_birth.month, date_of_birth.day))
    return age


def random_number(chance):
    """ Generate a random number. """
    return randint(1, chance)

def calculate_loot(monster):
    """ Function to calculate loot based on the difficulty of the monster. """
    if isinstance(monster, Monster):
        if monster.zone_difficulty == 'easy':
            return randint(1, 10)
        elif monster.zone_difficulty == 'medium':
            return randint(10, 50)
        elif monster.zone_difficulty == 'hard':
            return randint(50, 150)
        elif monster.zone_difficulty == 'boss':
            return randint(150, 300)
    else:
        return 0


def xp_calculator(monster):
    xp = (monster.defence + monster.strength +
          monster.health + monster.speed + monster.accuracy) * 2
    return xp

