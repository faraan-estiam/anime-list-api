from fastapi.testclient import TestClient
import pytest
from main import api

client = TestClient(api)

def test_valid_user():
  response = client.post("/auth/signup", json= {
    "email": "test.user1@gmail.com",
    "password": "password"
  })
  assert response.status_code == 201

def test_email_already_exists(create_user):
  response = client.post("/auth/signup", json= {
    "email": "test.useralreadyexists@gmail.com",
    "password": "password"
  })
  assert response.status_code == 409

def test_invalid_user():
  with pytest.raises(ValueError) as e:
    client.post("/auth/signup", json={
      "email": "thisisnotanemailàgmail.com",
      "password": "password"
    })
  assert "Malformed email address string" in str(e.value)
  response = client.post("/auth/signup", json={
    "notAnEmail": "thisisanemail@gmail.com",
    "password": "password"
  })
  assert response.status_code == 422

def test_login(create_user):
  response = client.post("auth/login", data={
    "username": "test.useralreadyexists@gmail.com",
    "password": "password"
  })
  assert response.status_code == 200

def test_invalid_login(create_user):
  response = client.post("auth/login", data={
    "email": "test.useralreadyexists@gmail.com",
    "password": "password"
  })
  assert response.status_code == 422

def test_invalid_credentials_login(create_user):
  response = client.post("auth/login", data={
    "username": "test.useralreadyexists@gmail.com",
    "password": "iforgotmypassword"
  })
  assert response.status_code == 401

def test_auth_me(auth_user):
  response = client.get('/auth/me', headers={"Authorization": f"Bearer {auth_user['access_token']}"})
  assert response.status_code == 200

def test_auth_me_unauthenticated():
  response = client.get('/auth/me', headers={"Authorization": f"i dont have a token :("})
  assert response.status_code == 401