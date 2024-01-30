#import os
#from datetime import datetime, timedelta, timezone
#from fastapi import HTTPException, Depends
#from passlib.context import CryptContext
#from jose import JWTError, jwt
#from starlette import status
#from sqlalchemy.orm import Session
#
#from app.models.player import Player
#from app.schemas.authentication import Token
#from app.schemas.player import UserInDB
#from dotenv import load_dotenv
#load_dotenv()
#
#SECRET_KEY = os.getenv("SECRET_KEY")
#
#ALGORITHM = "HS256"
#ACCESS_TOKEN_EXPIRE_MINUTES = 30
#
#pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#
#
#
## todo add checks to all routes for own entities and login
#
#def login(form_data, db: Session) -> Token:
#    user = authenticate_user(db, form_data.username, form_data.password)
#    if not user:
#        raise HTTPException(
#            status_code=status.HTTP_401_UNAUTHORIZED,
#            detail="Incorrect username or password",
#            headers={"WWW-Authenticate": "Bearer"},
#        )
#    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#    access_token = create_access_token(
#        data={"sub": user.username}, expires_delta=access_token_expires
#    )
#    return Token(access_token=access_token, token_type="bearer")
#
#
#def get_user(db, username: str):
#    player = db.query(Player).filter(Player.username == username).first()
#    if player is not None:
#        return UserInDB(username=player.username, hashed_password=player.password)
#
#def authenticate_user(db, username: str, password: str):
#    user = get_user(db, username)
#    if not user:
#        return False
#    if not verify_password(password, user.hashed_password):
#        return False
#    return user
#
#def create_access_token(data: dict, expires_delta: timedelta | None = None):
#    to_encode = data.copy()
#    if expires_delta:
#        expire = datetime.now(timezone.utc) + expires_delta
#    else:
#        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
#    to_encode.update({"exp": expire})
#    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#    return encoded_jwt
#
#
#def get_password_hash(password):
#    return pwd_context.hash(password)
#
#
#def verify_password(plain_password, hashed_password):
#    return pwd_context.verify(plain_password, hashed_password)
#