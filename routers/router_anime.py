from uuid import uuid4
from fastapi import APIRouter, HTTPException
from classes.models import Anime
from classes.database import animes

router = APIRouter(
    prefix='/animes'
)


#get all animes
@router.get('', response_model=list[Anime])
async def get_animes():
    return animes

#add a new anime
@router.post('', response_model=Anime, status_code=201)
async def post_anime(title:str, genres:list[str] | None = None, fr_title:str | None = None, episodes: int | None = None, oavs:int | None = None):
    newAnime=Anime(uid=uuid4(), title=title)
    if genres:
        newAnime.genres=genres
    if fr_title:
        newAnime.fr_title=fr_title
    if episodes:
        newAnime.episodes=episodes
    if oavs:
        newAnime.oavs=oavs
    animes.append(newAnime)
    return newAnime

#get specific anime by uid
@router.get('/{anime_uid}', response_model=Anime)
async def get_anime_by_id(anime_uid:str):
    for anime in animes:
        if str(anime.uid)==anime_uid:
            return anime
    raise HTTPException(status_code=404, detail='anime not found')