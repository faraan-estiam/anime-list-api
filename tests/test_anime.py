from fastapi.testclient import TestClient
from main import api
import pytest
from classes.models import AnimeNoID

# #get all animes
# @router.get('', response_model=List[Anime])
# async def get_animes():
#     query_result = db.child('animes').get().val()
#     if not query_result : return []
#     return [anime for anime in query_result.values()]
client = TestClient(api)

def test_get_all_anime():
  response = client.get("/animes")
  assert response.status_code == 200
  assert type(response.json()) is list

@pytest.mark.parametrize("anime",[
  AnimeNoID(title='shingeki no pytest', fr_title="l'attaque des pytest", genres=['test','tester','testing'], episodes=1, seasons=1, oavs=0)
])
def test_post_valid_anime(anime, auth_user):
  response = client.post("/animes", json= anime.model_dump(), headers={
    "Authorization": f"Bearer {auth_user['access_token']}",
  })
  assert response.status_code == 201

@pytest.mark.parametrize("something",[
  {"example": "this is obviously not working"},
  {"title":"this will miss an fr title", "genres":['not','working','test'], "episodes":1, "seasons":3, "oavs":0},
  {"title":"is oav string ?", "fr_title":"est-ce que l'oav est une chaine de caractères?", "genres":['not','working','test'], "episodes":1, "seasons":3, "oavs":"sdfdsfsdf"}
])
def test_post_invalid_anime(something, auth_user):
  response = client.post("/animes", json= something, headers={
    "Authorization": f"Bearer {auth_user['access_token']}",
  })
  assert response.status_code == 422