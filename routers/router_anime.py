from uuid import uuid4
from fastapi import APIRouter, HTTPException
from classes.models import Anime, AnimeNoID
from classes.database import animes

router = APIRouter(
    prefix='/library/animes',
    tags=['Anime Library']
)


#get all animes
@router.get('/', response_model=list[Anime])
async def get_animes():
    return animes

#add a new anime
@router.post('/', response_model=Anime, status_code=201)
async def post_anime(body_anime: AnimeNoID):
    uid = str(uuid4())
    newAnime=Anime(uid=uid, **body_anime.model_dump())
    animes.append(newAnime)
    return newAnime

#search an anime
@router.get('/search',response_model=list[Anime])
async def search_animes(title:str | None=None, genres:str | None=None):
    search_by_title = False
    search_by_genre = False
    if title:
        title = title.lower()
        search_by_title = True
    if genres:
        genres = genres.split()
        search_by_genre = True

    search_result = []
    
    for anime in animes:
        if(search_by_title):
            if title in anime.title.lower():
                search_result.append(anime)
                continue
            if title in anime.fr_title.lower():
                search_result.append(anime)
                continue

        if(search_by_genre):
            if any(item in anime.genres for item in genres):
                search_result.append(anime)
    
    return search_result

#get specific anime by uid
@router.get('/{anime_uid}', response_model=Anime)
async def get_anime_by_id(anime_uid:str):
    for anime in animes:
        if anime.uid==anime_uid:
            return anime
    raise HTTPException(status_code=404, detail='anime not found')

#update an anime
@router.patch('/{anime_uid}', response_model=Anime)
async def patch_anime(anime_uid:str, body_anime: AnimeNoID):
    for anime in animes:
        if anime.uid==anime_uid:
            anime.title = body_anime.title
            anime.genres = body_anime.genres
            anime.fr_title = body_anime.fr_title
            anime.episodes = body_anime.episodes
            anime.oavs = body_anime.oavs
            return anime
    raise HTTPException(status_code=404, detail='anime not found')

#remove an anime
@router.delete('/{anime_uid}')
async def delete_anime(anime_uid:str):
    for anime in animes:
        if anime.uid==anime_uid:
            animes.remove(anime)
            return {'message': 'anime deleted'}
    raise HTTPException(status_code=404, detail='anime not found')