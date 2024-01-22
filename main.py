import os
from fastapi import FastAPI
from dotenv import load_dotenv
from pydantic import BaseModel
import psycopg2

app = FastAPI()
load_dotenv()

class Player(BaseModel):
    player_id: int
    username: str
    name: str
    average_score: int
    training_score: list[int]


@app.get("/player")
async def getPlayers():
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM player")
    data = cursor.fetchall()
    print(data)
    cursor.close()
    return {"data": data}


@app.post("/player")
async def create_Player(player: Player):
    cursor = db_connection.cursor()
    cursor.execute(
        'INSERT INTO player (player_id, username, name, average_score, training_score) VALUES (%s, %s, %s, %s, %s)',
        (player.player_id, player.username, player.name, player.average_score, player.training_score)
    )
    db_connection.commit()
    return {"player": player}

@app.delete("/player")
async def delete_Player(player_id: int):
    cursor = db_connection.cursor()
    cursor.execute("DELETE FROM player WHERE player_id = %s", (player_id,))
    db_connection.commit()
    cursor.close()
    return {"message": "Player deleted successfully"}

try:
    db_connection = psycopg2.connect(
    database=os.environ["DBNAME"],
    user=os.environ["DBUSER"],
    password=os.environ["DBPASSWORD"],
    host=os.environ["DBHOST"],  # Of het IP-adres van je databasehost
    port=os.environ["DBPORT"]  # De standaard PostgreSQL-poort
)

except:
    db_connection = psycopg2.connect(
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),  # Of het IP-adres van je databasehost
        port=os.getenv("DB_PORT")  # De standaard PostgreSQL-poort
    )
