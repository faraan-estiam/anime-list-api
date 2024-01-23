from fastapi.testclient import TestClient
from main import api
import pytest
from classes.models import AnimeNoID, Anime

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
def test_put_post_anime(anime, auth_user, create_anime):
  response = client.post("/animes", json= anime.model_dump(), headers={"Authorization": f"Bearer {auth_user['access_token']}"})
  assert response.status_code == 201
  assert type(response.json()) == dict
  response = client.put(f"/animes/{create_anime['uid']}", json=anime.model_dump(), headers={"Authorization": f"Bearer {auth_user['access_token']}"})
  assert response.status_code == 202
  assert type(response.json()) == dict

def test_get_update_delete_anime(create_anime, auth_user):
  anime = AnimeNoID(title='edited no pytest', fr_title="le pytest modifié", genres=['test','tester','testing'], episodes=1, seasons=1, oavs=0).model_dump()
  response = client.get(f"/animes/{create_anime['uid']}")
  assert response.status_code == 200
  response = client.put(f"/animes/{create_anime['uid']}", headers={"Authorization": f"Bearer {auth_user['access_token']}"}, json=anime)
  assert response.status_code == 202
  response = client.delete(f"/animes/{create_anime['uid']}", headers={"Authorization": f"Bearer {auth_user['access_token']}"})
  assert response.status_code == 202

@pytest.mark.parametrize("id", ["not an id", "still not", "i think it's enough testing now"])
def test_anime_not_found(id, auth_user):
  anime = AnimeNoID(title='shingeki no pytest', fr_title="l'attaque des pytest", genres=['test','tester','testing'], episodes=1, seasons=1, oavs=0).model_dump()
  response = client.get(f'/animes/{id}')
  assert response.status_code == 404
  response = client.put(f"/animes/{id}", headers={"Authorization": f"Bearer {auth_user['access_token']}"}, json=anime)
  assert response.status_code == 404
  response = client.delete(f"/animes/{id}", headers={"Authorization": f"Bearer {auth_user['access_token']}"})
  assert response.status_code == 404

@pytest.mark.parametrize("something",[
  {"example": "this is obviously not working"},
  {"title":"this will miss an fr title", "genres":['not','working','test'], "episodes":1, "seasons":3, "oavs":0},
  {"title":"is oav string ?", "fr_title":"est-ce que l'oav est une chaine de caractères?", "genres":['not','working','test'], "episodes":1, "seasons":3, "oavs":"sdfdsfsdf"}
])
def invalid_anime(something, auth_user, create_anime):
  response = client.post("/animes", json= something, headers={
    "Authorization": f"Bearer {auth_user['access_token']}"
  })
  assert response.status_code == 422
  response = client.put(f"/animes/{create_anime['uid']}", json= something, headers={
    "Authorization": f"Bearer {auth_user['access_token']}"
  })
  assert response.status_code == 422

def test_search_anime():
  response = client.get("/animes/search", params={"title":""})
  assert response.status_code == 200
  assert type(response.json()) is list