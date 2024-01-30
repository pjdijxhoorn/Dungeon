# from sqlalchemy.orm import Session
#
# from app.services.authentication import authenticate_user
# from database import get_db
# from main import app
# from fastapi.testclient import TestClient
#
# client = TestClient(app)
#
# def test_login():
#     login_data = {
#         "username": "user4",
#         "password": "wachtwoord4",
#     }
#     db: Session = next(get_db())
#     response = client.post("/authentication/login", data=login_data, params={"db": db})
#     assert response.status_code == 200
#
#
# def test_login_incorrect_login():
#     login_data = {
#         "username": "user4",
#         "password": "wachtwoord",
#     }
#     db: Session = next(get_db())
#     response = client.post("/authentication/login", data=login_data, params={"db": db})
#     assert response.status_code == 401
#     assert  response.json() == {'detail': 'Incorrect username or password'}
#
# def test_authenticate_user():
#     db: Session = next(get_db())
#     user = authenticate_user(db, "he who must not be named", '$2a$12$1b1hXeBeAL5rNsDeDdFsUu8VLdcA/ZE9IBEUug9b6kmn8t28alPFG')
#     assert user == False