import os

from fastapi import FastAPI
from dotenv import load_dotenv
import psycopg2

app = FastAPI()
load_dotenv()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

db_connection = psycopg2.connect(
    database=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),  # Of het IP-adres van je databasehost
    port=os.getenv("DB_PORT")  # De standaard PostgreSQL-poort
)
