from typing import List, Optional #compatibility fix for render
from fastapi import APIRouter, HTTPException, Depends, Response
from classes.models import WatchedAnime
from database.firebase import db
from routers.router_auth import get_current_user
from routers.router_anime import get_anime_by_id
import stripe

router = APIRouter(
    prefix='/watchlist',
    tags=['Watchlist']
)

async def check_stripe_subscription(user_data):
    stripe_data=db.child('users').child(user_data['uid']).child('stripe').get().val()
    if not stripe_data: raise HTTPException(status_code=401, detail='no active subscription')
    status = stripe.Subscription.retrieve(stripe_data['subscription_id'])['status']
    if status != 'active': raise HTTPException(status_code=401, detail='no active subscription')

#get current user watchlist
@router.get('', response_model=List[WatchedAnime])
async def get_watchlist(user_data: dict = Depends(get_current_user)):
    await check_stripe_subscription(user_data)
    query_result = db.child('users').child(user_data['uid']).child('watchlist').get(token=user_data['idToken']).val()
    if not query_result : return []
    return [watchlist for watchlist in query_result.values()]

@router.post('', status_code=201)
async def add_watched_anime(anime: WatchedAnime, user_data: dict = Depends(get_current_user)):
    #check if anime already inside watchlist
    if (anime.anime_uid in [item['anime_uid'] for item in await get_watchlist(user_data)]):
        raise HTTPException(status_code=409, detail='anime already found in watchlist')
    
    await get_anime_by_id(anime.anime_uid) #checks if anime exists before adding it to watchlist
    db.child('users').child(user_data['uid']).child('watchlist').child(anime.anime_uid).set(anime.model_dump(),token=user_data['idToken'])
    return {'message':'anime added to watchlist'}

@router.get('/{anime_uid}')
async def get_watched_anime_by_anime_uid(anime_uid: str, user_data: dict = Depends(get_current_user)):
    await check_stripe_subscription(user_data)
    query_result = db.child('users').child(user_data['uid']).child('watchlist').child(anime_uid).get(token=user_data['idToken']).val()
    if not query_result : raise HTTPException(status_code=404, detail='anime not found in watchlist')
    return query_result

@router.patch('/{anime_uid}')
async def update_watchlist(anime_uid:str, user_data: dict = Depends(get_current_user),last_episode: Optional[str]=None, last_season: Optional[str]=None,last_oav: Optional[str]=None,status: Optional[str]=None):
        targeted_anime = await get_watched_anime_by_anime_uid(anime_uid, user_data)
        if last_episode : targeted_anime["last_episode"] = last_episode
        if last_season : targeted_anime["last_season"] = last_season
        if last_oav : targeted_anime["last_oav"] = last_oav
        if status : targeted_anime["status"] = status
        db.child('users').child(user_data['uid']).child('watchlist').child(anime_uid).set(targeted_anime,token=user_data['idToken'])
        return {'message':'anime updated in watchlist'}

@router.delete('/{anime_uid}')
async def remove_entry(anime_uid: str, user_data: dict = Depends(get_current_user)):
    #check if anime exists before attempting to delete
    await get_watched_anime_by_anime_uid(anime_uid, user_data)
    db.child('users').child(user_data['uid']).child('watchlist').child(anime_uid).remove(token=user_data['idToken'])
    return {"message":"anime removed from watchlist"}