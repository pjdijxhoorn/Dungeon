from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.profile import Profile

from app.services.player import update_fitness_multiplier
from app.utilities.common_functions import calculate_fitness_multiplier, bmi_calculation, \
    calculate_age, max_heart_frequency_calculation, reserve_heart_frequency_calculation


def get_profiles(db: Session):
    """ Get all profiles from the database. """
    return db.query(Profile).all()


def get_profile(db: Session, profile_id: int):
    """ Get a specific profile from the database by using a profile ID. """
    profile = db.query(Profile).filter(
        Profile.profile_id == profile_id).first()
    if profile is None:
        raise HTTPException(status_code=404, detail="profile not found")
    return profile


def update_profile(profile_id: int, updateprofile, db: Session):
    """ Update a profile with the given profile_id in the database. """
    profile = db.query(Profile).filter(
        Profile.profile_id == profile_id).first()
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    bmi = bmi_calculation(updateprofile.height_in_m,
                          updateprofile.weight_in_kg)
    age = calculate_age(profile.date_of_birth)
    max_heart_frequency = max_heart_frequency_calculation(age)
    reserve_heart_frequency = reserve_heart_frequency_calculation(
        max_heart_frequency, updateprofile.rest_heart_frequency)
    fitness_multiplier = calculate_fitness_multiplier(
        bmi, reserve_heart_frequency)
    update_fitness_multiplier(profile_id, db, fitness_multiplier)

    profile.bmi = bmi
    profile.weight_in_kg = updateprofile.weight_in_kg
    profile.height_in_m = updateprofile.height_in_m
    profile.max_heart_frequency = max_heart_frequency
    profile.rest_heart_frequency = updateprofile.rest_heart_frequency
    profile.reserve_heart_frequency = reserve_heart_frequency

    db.commit()
    db.refresh(profile)
    return profile
