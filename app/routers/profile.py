from fastapi import APIRouter, Depends
from app.services.profile import get_profiles
from database import get_db

router = APIRouter()

@router.get("",tags=["profiles"])
def get_profiles(db=Depends(get_db)):
    profiles = get_profiles(db)
    return profiles