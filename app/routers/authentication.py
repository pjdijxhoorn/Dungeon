from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

import app.services.authentication as services
from app.schemas.authentication import Login, Token
from database import get_db

router = APIRouter()
@router.post("/login", status_code=200, tags=["authentication"])
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db=Depends(get_db))-> Token:
    return services.login(form_data, db)


