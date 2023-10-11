from fastapi import APIRouter
from classes.models import Anime
from classes.database import animes

router = APIRouter(
    prefix='/animes'
)


#get all animes
@router.get('', response_model=list[Anime])
async def get_animes():
    return animes
