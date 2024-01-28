from sqlalchemy.orm import Session

from database import get_db
from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_login():
    login_data = {
        "username": "user4",
        "password": "wachtwoord4",
    }
    db: Session = next(get_db())
    response = client.post("/authentication/login", data=login_data, params={"db": db})
    assert response.status_code == 200
