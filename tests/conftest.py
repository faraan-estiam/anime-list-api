from firebase_admin import auth
from main import api
from fastapi.testclient import TestClient
import pytest
import os

os.environ['TESTING'] = 'True'
client = TestClient(api)

@pytest.fixture(scope="session", autouse=True)
def cleanup(request):
  def remove_test_users():
    users = auth.list_users().iterate_all()
    for user in users:
      if user.email.startswith("test."):
        auth.delete_user(user.uid)

  request.addfinalizer(remove_test_users)

@pytest.fixture()
def create_user():
  client.post("/auth/signup", json= {
    "email": "test.useralreadyexists@gmail.com",
    "password": "password"
  })

@pytest.fixture
def auth_user(create_user):
  user_credentials = client.post("auth/login", data={
    "username": "test.useralreadyexists@gmail.com",
    "password": "password"
  })

  return user_credentials.json()