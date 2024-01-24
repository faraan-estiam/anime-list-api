from firebase_admin import auth
from classes.models import AnimeNoID
from main import api
from fastapi.testclient import TestClient
import pytest
import os
from database.firebase import db

os.environ['TESTING'] = 'True'
client = TestClient(api)

@pytest.fixture()
def create_user():
  client.post("/auth/signup", json= {
    "email": "test.useralreadyexists@gmail.com",
    "password": "password"
  })

@pytest.fixture()
def auth_user(create_user):
  user_credentials = client.post("auth/login", data={
    "username": "test.useralreadyexists@gmail.com",
    "password": "password"
  })
  return user_credentials.json()

def remove_test_users():
  users = auth.list_users().iterate_all()
  for user in users:
    if user.email.startswith("test."):
      auth.delete_user(user.uid)

@pytest.fixture()
def subscribed_user(auth_user):
  auth_user_uid = client.get("/auth/me", headers={'Authorization':f"Bearer {auth_user['access_token']}"}).json()['uid']
  db.child('users').child(auth_user_uid).child('stripe').set({"subscription":"FAKE"},token=f"Bearer {auth_user['access_token']}")
  return auth_user

@pytest.fixture()
def create_anime(auth_user):
  anime = AnimeNoID(title='shingeki no pytest', fr_title="l'attaque des pytest", genres=['test','tester','testing'], episodes=1, seasons=1, oavs=0)
  response = client.post("/animes", json= anime.model_dump(), headers={
    "Authorization": f"Bearer {auth_user['access_token']}"
  })
  return response.json()

def remove_test_animes():
  client.post("/auth/signup", json= {
    "email": "test.useralreadyexists@gmail.com",
    "password": "password"
  })
  user_credentials = client.post("auth/login", data={
    "username": "test.useralreadyexists@gmail.com",
    "password": "password"
  })
  user_token = f"Bearer {user_credentials.json()['access_token']}"
  query_result = db.child('animes').get().val()
  animes = [] if not query_result else [anime for anime in query_result.values()]
  for anime in animes:
    if 'pytest_' in anime['title'].lower() or 'pytest' in anime['fr_title'].lower():
      client.delete(f"/animes/{anime['uid']}", headers={"Authorization": user_token,})

@pytest.fixture(scope="session", autouse=True)
def cleanup(request):
  request.addfinalizer(remove_test_users)
  request.addfinalizer(remove_test_animes)
