from fastapi.testclient import TestClient
from main import api
import pytest
from classes.models import WatchedAnime
client = TestClient(api)

@pytest.mark.parametrize("route,method,body", [
  ("/watchlist", 'GET', None),
  ("/watchlist", 'POST', WatchedAnime(anime_uid="any", last_season=0, last_episode=0, last_oav=0, status='NONE').model_dump()),
  ("/watchlist/AnimeUID", 'GET', None),
  ("/watchlist/AnimeUID", 'PATCH', WatchedAnime(anime_uid="any", last_season=0, last_episode=0, last_oav=0, status='NONE').model_dump()),
  ("/watchlist/AnimeUID", 'DELETE', None)
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

@pytest.mark.parametrize("route,method,body", [
  ("/watchlist", 'GET', None),
  ("/watchlist", 'POST', WatchedAnime(anime_uid="any", last_season=0, last_episode=0, last_oav=0, status='NONE').model_dump()),
  ("/watchlist/AnimeUID", 'GET', None),
  ("/watchlist/AnimeUID", 'PATCH', WatchedAnime(anime_uid="any", last_season=0, last_episode=0, last_oav=0, status='NONE').model_dump()),
  ("/watchlist/AnimeUID", 'DELETE', None)
])
def test_no_active_subscription(route, method, body, auth_user):
  if (method == "GET"):
    response = client.get(route, headers={"Authorization": f"Bearer {auth_user['access_token']}"})
  elif (method == "POST"):
    response = client.post(route, json=body, headers={"Authorization": f"Bearer {auth_user['access_token']}"})
  elif (method == "PUT"):
    response = client.put(route, json=body, headers={"Authorization": f"Bearer {auth_user['access_token']}"})
  elif (method == "PATCH"):
    response = client.patch(route, json=body, headers={"Authorization": f"Bearer {auth_user['access_token']}"})
  elif (method == "DELETE"):
    response = client.delete(route, headers={"Authorization": f"Bearer {auth_user['access_token']}"})
  
  assert response.status_code == 401
  assert response.json()['detail'] == "no active subscription"

# @pytest.mark.parametrize("id", ["not an id", "still not", "i think it's enough testing now"])
# def test_anime_not_found(id, subscribed_user):
#   anime = WatchedAnime(anime_uid="any", last_season=0, last_episode=0, last_oav=0, status='NONE').model_dump()
#   response = client.get(f'/watchlist/{id}')
#   assert response.status_code == 404
#   response = client.patch(f"/watchlist/{id}", headers={"Authorization": f"Bearer {subscribed_user['access_token']}"}, json=anime)
#   assert response.status_code == 404
#   response = client.delete(f"/watchlist/{id}", headers={"Authorization": f"Bearer {subscribed_user['access_token']}"})
#   assert response.status_code == 404

def test_get_watchlist(subscribed_user):
  response = client.get("/watchlist", headers={"Authorization": f"Bearer {subscribed_user['access_token']}"})
  assert response.status_code == 200