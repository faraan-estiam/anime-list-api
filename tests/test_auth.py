from fastapi.testclient import TestClient
from main import api

client = TestClient(api)

def test_valid_user():
  response = client.post("/auth/signup", json= {
    "email": "test.user1@gmail.com",
    "password": "password"
  })
  assert response.status_code == 201

def test_invalid_user(create_user):
  response = client.post("/auth/signup", json= {
    "email": "test.useralreadyexists@gmail.com",
    "password": "password"
  })
  assert response.status_code == 409