import os
import psycopg2
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

try:
    SessionLocal = psycopg2.connect(
        database=os.environ["DBNAME"],
        user=os.environ["DBUSER"],
        password=os.environ["DBPASSWORD"],
        host=os.environ["DBHOST"],
        port=os.environ["DBPORT"]
    )

except:
    SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()


def get_db():
    """ This function provides a session-local database connection. """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def reset_database():
    """ This function resets the database. """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sql_file_path = os.path.join(script_dir, "test_script.sql")
    if os.path.exists(sql_file_path):
        with open(sql_file_path, 'r') as sql_file:
            sql_script = sql_file.read()
        db = next(get_db())
        try:
            db.execute(text(sql_script))
            db.commit()

            print("Database reset successful.")
        except Exception as e:
            print(f"Error resetting database: {e}")

            db.rollback()
        finally:
            db.close()
