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

#get specific anime by uid
@router.get('/{anime_uid}', response_model=Anime)
async def get_anime_by_id(anime_uid:str):
    for anime in animes:
        if str(anime.uid)==anime_uid:
            return anime
    raise HTTPException(status_code=404, detail='anime not found')