from typing import List #compatibility for Render
from pydantic import BaseModel

class Anime(BaseModel):
    uid : str
    title : str
    fr_title : str
    genres : List[str]
    episodes : int
    seasons : int
    oavs: int
    #user_reviews : str | None = None

#an Anime Object without id to use as data_type in routers
class AnimeNoID(BaseModel):
    title : str
    fr_title : str
    genres : List[str]
    episodes : int
    seasons : int
    oavs: int

class WatchedAnime(BaseModel):
    anime_uid: str
    last_season: int
    last_episode: int
    last_oav: int
    status: str

class User(BaseModel):
    email: str
    password: str
#TODO :
#<> add User model
    #<> watchlist ?
    #<> profile ?
    #<> reviews ?
    #<> (do stats and graphs on most liked ???)