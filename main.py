from fastapi import FastAPI
from app.routers import player
from database import get_db
from fastapi import Depends
from app.models.player import Player

app = FastAPI()

app.include_router(player.router, prefix="/player")


@app.on_event("startup")
async def startup_event():
    print("this is the startup event!")