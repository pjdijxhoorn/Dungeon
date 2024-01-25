from fastapi import APIRouter, Depends, HTTPException
import app.services.profile as services
from app.schemas.profile import Profile, UpdateProfile
from database import get_db

router = APIRouter()

#all profiles
@router.get("",status_code=200, tags=["Profile"])
def get_profiles(db=Depends(get_db)) -> list[Profile]:
    profiles = services.get_profiles(db)
    return profiles

@router.get("/{profile_id}", status_code=200,  tags=["Profile"])
#one profile
def get_profile(profile_id: int, db=Depends(get_db)) -> Profile:
    profile = services.get_profile(db, profile_id)
    if profile is None:
        raise HTTPException(status_code=404, detail="profile not found")
    return profile


@router.delete("/{profile_id}", status_code=200, tags=["Profile"])

def delete_profile(profile_id: int, db=Depends(get_db)):
    message = services.delete_profile(profile_id, db)
    return message
#update profile
@router.put("/{profile_id}", status_code=200, tags=["Profile"])

def patch_profile(profile_id: int, profile: UpdateProfile, db=Depends(get_db)):
    return services.patch_profile(profile_id, profile, db)
