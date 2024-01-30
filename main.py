from fastapi import FastAPI
from app.routers import player, profile, training #, authentication
from database import get_db
from fastapi import Depends
app = FastAPI()

app.include_router(player.router, prefix="/player")
app.include_router(profile.router, prefix="/profile")
app.include_router(training.router, prefix="/training")
#app.include_router(authentication.router, prefix="/authentication")


@app.on_event("startup")
async def startup_event():
    print("this is the startup event!")
