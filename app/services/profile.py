from sqlalchemy.orm import Session
from app.models.profile import Profile


def get_profiles(db: Session):
    return db.query(Profile).all()
