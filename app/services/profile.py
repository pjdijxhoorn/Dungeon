import math

from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.profile import Profile
from datetime import date

from app.services.player import update_fitness_multiplier


def get_profiles(db: Session):
    return db.query(Profile).all()


def get_profile(db: Session, profile_id: int):
    profile = db.query(Profile).filter(Profile.profile_id == profile_id).first()
    return profile


def update_profile(profile_id: int, update_profile, db: Session):
    profile = db.query(Profile).filter(Profile.profile_id == profile_id).first()
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")

    bmi = bmi_calculation(update_profile.height_in_m, update_profile.weight_in_kg)
    age = calculate_age(profile.date_of_birth)
    max_heart_frequency = max_heart_frequency_calculation(age)
    reserve_heart_frequency = reserve_heart_frequency_calculation(max_heart_frequency,
                                                                  update_profile.rest_heart_frequency)
    fitness_multiplier = calculate_fitness_multiplier(bmi, reserve_heart_frequency)
    update_fitness_multiplier(profile_id, db, fitness_multiplier)

    profile.bmi = bmi
    profile.weight_in_kg = update_profile.weight_in_kg
    profile.height_in_m = update_profile.height_in_m
    profile.max_heart_frequency = max_heart_frequency
    profile.rest_heart_frequency = update_profile.rest_heart_frequency
    profile.reserve_heart_frequency = reserve_heart_frequency

    db.commit()
    db.refresh(profile)


    return profile


def bmi_calculation(height_in_m, weight_in_kg):
    bmi = weight_in_kg / (
                height_in_m ** 2)  
    return round(bmi, 2)


def max_heart_frequency_calculation(age):
    max_heart_frequency = 220 - age
    return max_heart_frequency


def reserve_heart_frequency_calculation(max_heart_frequency, rest_heart_frequency):
    reserve_heart_frequency = max_heart_frequency - rest_heart_frequency
    return reserve_heart_frequency


def calculate_age(date_of_birth):
    try:
        date_of_birth_split = date_of_birth
        current_date = date.today()
        age = current_date.year - date_of_birth_split.year - (
                    (current_date.month, current_date.day) < (date_of_birth_split.month, date_of_birth_split.day))
        return age

    except ValueError:
        return "Invalid date format."

def calculate_fitness_multiplier(bmi, hart_reserve_frequency):
    fitness_multiplier = math.log10(bmi / hart_reserve_frequency) + 1
    return round(fitness_multiplier, 2)


