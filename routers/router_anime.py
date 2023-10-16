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
async def post_anime(title:str, genres:list[str], fr_title:str, episodes: int, oavs:int):
    newAnime=Anime(uid=uuid4(), title=title, fr_title=fr_title, genres=genres, episodes=episodes, oavs=oavs)
    animes.append(newAnime)
    return newAnime

#get specific anime by uid
@router.get('/{anime_uid}', response_model=Anime)
async def get_anime_by_id(anime_uid:str):
    for anime in animes:
        if str(anime.uid)==anime_uid:
            return anime
    raise HTTPException(status_code=404, detail='anime not found')

#update an anime
@router.patch('/{anime_uid}', response_model=Anime)
async def patch_anime(anime_uid:str, title:str | None = None, genres:list[str] | None = None, fr_title:str | None = None, episodes: int | None = None, oavs:int | None = None):
    for anime in animes:
        if str(anime.uid)==anime_uid:
            if title:
                anime.title = title
            if genres:
                anime.genres=genres
            if fr_title:
                anime.fr_title=fr_title
            if episodes:
                anime.episodes=episodes
            if oavs:
                anime.oavs=oavs
            return anime
    raise HTTPException(status_code=404, detail='anime not found')

#remove an anime
@router.delete('/{anime_uid}')
async def delete_anime(anime_uid:str):
    for anime in animes:
        if str(anime.uid)==anime_uid:
            animes.remove(anime)
            return
    raise HTTPException(status_code=404, detail='anime not found')

#search an anime
@router.get('/search',response_model=list[Anime])
async def search_animes(title:str | None=None, genres:list[str] | None=None):
    search_by_title = False
    search_by_genre = False
    if title:
        title = title.lower
        search_by_title = True
    if genres:
        search_by_genre = True

    search_result = []
    
    for anime in animes:
        if(search_by_title):
            if title in anime.title.lower():
                search_result.append(anime)
                continue

        if(search_by_genre):
            if any(item in anime.genres for item in genres):
                search_result.append(genres)
    
    return search_result
