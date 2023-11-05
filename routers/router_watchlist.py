from typing import List, Optional #compatibility fix for render
from fastapi import APIRouter, HTTPException, Depends, Response
from classes.models import WatchedAnime
from database.firebase import db
from routers.router_auth import get_current_user
from routers.router_anime import get_anime_by_id

router = APIRouter(
    prefix='/watchlist',
    tags=['Watchlist']
)

#get current user watchlist
@router.get('', response_model=List[WatchedAnime])
async def get_watchlist(user_data: int = Depends(get_current_user)):
    query_result = db.child('users').child(user_data['uid']).child('watchlist').get().val()
    if not query_result : return []
    return [watchlist for watchlist in query_result.values()]

@router.post('', status_code=201)
async def add_watched_anime(anime: WatchedAnime, user_data: int = Depends(get_current_user)):
    #check if anime already inside watchlist
    if (anime.anime_uid in [item['anime_uid'] for item in await get_watchlist(user_data)]):
        raise HTTPException(status_code=409, detail='anime already found in watchlist')
    
    await get_anime_by_id(anime.anime_uid) #checks if anime exists before adding it to watchlist
    db.child('users').child(user_data['uid']).child('watchlist').child(anime.anime_uid).set(anime.model_dump())
    return {'message':'anime added to watchlist'}

@router.get('/{anime_uid}')
async def get_watched_anime_by_anime_uid(anime_uid: str, user_data: int = Depends(get_current_user)):
    query_result = db.child('users').child(user_data['uid']).child('watchlist').child(anime_uid).get().val()
    if not query_result : raise HTTPException(status_code=404, detail='anime not found in watchlist')
    return query_result

@router.delete('/{anime_uid}')
async def remove_entry(anime_uid: str, user_data: int = Depends(get_current_user)):
    #check if anime exists before attempting to delete
    await get_watched_anime_by_anime_uid(anime_uid, user_data)
    db.child('users').child(user_data['uid']).child('watchlist').child(anime_uid).remove()
    return {'message':'anime removed from watchlist'}
