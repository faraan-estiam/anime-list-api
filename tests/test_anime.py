from fastapi.testclient import TestClient
from main import api
import pytest
from classes.models import AnimeNoID

client = TestClient(api)

def anime_uids():
  response = client.get("/animes")
  uid_list = [anime['uid'] for anime in response.json()]
  if len(uid_list) > 5 :
    uid_list = uid_list[0:5]
  return uid_list

def test_get_all_anime():
  response = client.get("/animes")
  assert response.status_code == 200
  assert type(response.json()) is list

@pytest.mark.parametrize("route,method,body", [
  ("/animes","POST", AnimeNoID(title='shingeki no pytest', fr_title="l'attaque des pytest", genres=['test','tester','testing'], episodes=1, seasons=1, oavs=0).model_dump()),
  ("/animes/animeUID","PUT", AnimeNoID(title='shingeki no pytest', fr_title="l'attaque des pytest", genres=['test','tester','testing'], episodes=1, seasons=1, oavs=0).model_dump()),
  ("/animes/animeUID","DELETE", None)
])
def test_unauthorized(route, method, body):
  if (method == "GET"):
    response = client.get(route)
  elif (method == "POST"):
    response = client.post(route, json=body)
  elif (method == "PUT"):
    response = client.put(route, json=body)
  elif (method == "PATCH"):
    response = client.patch(route, json=body)
  elif (method == "DELETE"):
    response = client.delete(route)
  
  assert response.status_code == 401

@pytest.mark.parametrize("anime",[
  AnimeNoID(title='shingeki no pytest', fr_title="l'attaque des pytest", genres=['test','tester','testing'], episodes=1, seasons=1, oavs=0)
])
def test_post_valid_anime(anime, auth_user):
  response = client.post("/animes", json= anime.model_dump(), headers={
    "Authorization": f"Bearer {auth_user['access_token']}"
  })
  assert response.status_code == 201

@pytest.mark.parametrize("something",[
  {"example": "this is obviously not working"},
  {"title":"this will miss an fr title", "genres":['not','working','test'], "episodes":1, "seasons":3, "oavs":0},
  {"title":"is oav string ?", "fr_title":"est-ce que l'oav est une chaine de caractères?", "genres":['not','working','test'], "episodes":1, "seasons":3, "oavs":"sdfdsfsdf"}
])
def test_post_invalid_anime(something, auth_user):
  response = client.post("/animes", json= something, headers={
    "Authorization": f"Bearer {auth_user['access_token']}"
  })
  assert response.status_code == 422

@pytest.mark.parametrize("id", anime_uids())
def test_get_anime_by_id(id):
  response = client.get(f'/animes/{id}')
  assert response.status_code == 200
