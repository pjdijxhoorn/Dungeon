from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.profile import Profile
from app.schemas.profile import UpdateProfile
from datetime import date


def get_profiles(db: Session):
    return db.query(Profile).all()


def get_profile(db: Session, profile_id: int):
    profile = db.query(Profile).filter(Profile.profile_id == profile_id).first()
    return profile


def delete_profile(profile_id: int, db: Session):
    profile = db.query(Profile).filter(Profile.profile_id == profile_id).first()
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    db.delete(profile)
    db.commit()
    return "profile deleted"


def patch_profile(profile_id: int, update_profile, db: Session):
    profile = db.query(Profile).filter(Profile.profile_id == profile_id).first()
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")

    # Assuming `update_profile` is an instance of UpdateProfile
    bmi = bmi_calculation(update_profile.height_in_m, update_profile.weight_in_kg)
    age = calculate_age(profile.date_of_birth)
    max_heart_frequency = max_heart_frequency_calculation(age)
    reserve_heart_frequency = reserve_heart_frequency_calculation(max_heart_frequency,
                                                                  update_profile.rest_heart_frequency)

    # Update the existing profile instead of creating a new one
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
    """calculate the bmi by dividing the weight with the lengt sqaured"""
    bmi = weight_in_kg / (
                height_in_m ** 2)  # Momenteel alleen voor mannen, gezien BMI berekening voor vrouwen anders is, dit willen we in de toekomst ook zeker nog implemeteren maar voor nu hebben we gekozen om het simpeler te houden
    return round(bmi, 2)


def max_heart_frequency_calculation(age):
    """calculate the max heart frequency by substracting the 220 by the age of a person"""
    max_heart_frequency = 220 - age
    return max_heart_frequency


def reserve_heart_frequency_calculation(max_heart_frequency, rest_heart_frequency):
    """calculate the reserve heart frequency bu substracting the rest heart freqeuncy of the max heart frequency"""
    reserve_heart_frequency = max_heart_frequency - rest_heart_frequency
    return reserve_heart_frequency


def calculate_age(date_of_birth):
    try:
        # Convert the input string to a datetime object
        date_of_birth_split = date_of_birth
        # Get the current date
        current_date = date.today()
        # Calculate the age
        age = current_date.year - date_of_birth_split.year - (
                    (current_date.month, current_date.day) < (date_of_birth_split.month, date_of_birth_split.day))
        return age

    except ValueError:
        # Handle invalid date format
        #raise HTTPException(status_code=404, detail="Profile not found")
        return "Invalid date format."
