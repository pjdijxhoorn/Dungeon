from fastapi import APIRouter, Depends
import app.services.profile as services
from app.schemas.profile import Profile, UpdateProfile
from database import get_db

router = APIRouter()


@router.get("", status_code=200, tags=["Profile"])
def get_profiles(db=Depends(get_db)) -> list[Profile]:
    """ Get a list of all profiles from the database. """
    return services.get_profiles(db)


@router.get("/{profile_id}", status_code=200, tags=["Profile"])
def get_profile(profile_id: int, db=Depends(get_db)) -> Profile:
    """ Get a specific profile by its ID. """
    return services.get_profile(db, profile_id)


@router.put("/{profile_id}", status_code=200, tags=["Profile"])
def update_profile(profile_id: int, profile: UpdateProfile, db=Depends(get_db)):
    """ Update an existing profile with new data. """
    return services.update_profile(profile_id, profile, db)
