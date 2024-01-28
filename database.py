import os
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
load_dotenv()

try:
    db_connection = psycopg2.connect(
    database=os.environ["DBNAME"],
    user=os.environ["DBUSER"],
    password=os.environ["DBPASSWORD"],
    host=os.environ["DBHOST"],  # Of het IP-adres van je databasehost
    port=os.environ["DBPORT"]  # De standaard PostgreSQL-poort
    )

except:
    SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

