from typing import List, Optional #compatibility fix for render
from uuid import uuid4
from fastapi import APIRouter, HTTPException
from classes.models import Anime, AnimeNoID
from classes.database import animes
from database.firebase import db

router = APIRouter(
    prefix='/library/animes',
    tags=['Anime Library']
)


#get all animes
@router.get('/', response_model=List[Anime])
async def get_animes():
    query_result = db.child('library').child('animes').get().val()
    if not query_result : return []
    return [anime for anime in query_result.values()]

#add a new anime
@router.post('/', response_model=Anime, status_code=201)
async def post_anime(body_anime: AnimeNoID):
    uid = str(uuid4())
    newAnime=Anime(uid=uid, **body_anime.model_dump())
    db.child('library').child('animes').child(uid).set(data=newAnime.model_dump())
    return newAnime

#search an anime
@router.get('/search',response_model=List[Anime])
async def search_animes(title: Optional[str]=None, genres: Optional[str]=None):
    search_by_title = False
    search_by_genre = False
    if title:
        title = title.lower()
        search_by_title = True
    if genres:
        genres = genres.split()
        search_by_genre = True

    search_result = []
    query_result = db.child('library').child('animes').get().val()
    animes = [anime for anime in query_result.values()]

    for anime in animes:
        if(search_by_title):
            if title in anime['title'].lower():
                search_result.append(anime)
                continue
            if title in anime['fr_title'].lower():
                search_result.append(anime)
                continue

        if(search_by_genre):
            if any(item in anime['genres'] for item in genres):
                search_result.append(anime)
    return search_result

#get specific anime by uid
@router.get('/{anime_uid}', response_model=Anime)
async def get_anime_by_id(anime_uid:str):
    query_result = db.child('library').child('animes').child(anime_uid).get().val()
    if not query_result : raise HTTPException(status_code=404, detail='anime not found')
    return query_result

#update an anime
@router.patch('/{anime_uid}', response_model=Anime)
async def patch_anime(anime_uid:str, body_anime: AnimeNoID):
    query_result = db.child('library').child('animes').child(anime_uid).get().val()
    if not query_result : raise HTTPException(status_code=404, detail='anime not found')
    updated_anime = Anime(uid=anime_uid, **body_anime.model_dump())
    return db.child('library').child('animes').child(anime_uid).update(updated_anime.model_dump())

#remove an anime
@router.delete('/{anime_uid}')
async def delete_anime(anime_uid:str):
    query_result = db.child('library').child('animes').child(anime_uid).get().val()
    if not query_result : raise HTTPException(status_code=404, detail='anime not found')
    db.child('library').child('animes').child(anime_uid).remove()
    return {'message':'anime delted'}