from fastapi import FastAPI
from app.routers import player, profile, training
from database import get_db
from fastapi import Depends

app = FastAPI()

app.include_router(player.router, prefix="/player")
app.include_router(profile.router, prefix="/profile")
app.include_router(training.router, prefix="/training")


@app.on_event("startup")
async def startup_event():
    print("this is the startup event!")
