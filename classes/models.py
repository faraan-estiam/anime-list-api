from pydantic import BaseModel

class Anime(BaseModel):
    uid : str
    title : str
    fr_title : str
    genres : list[str]
    episodes : int
    oavs: int
    #user_reviews : str | None = None

#an Anime Object without id to use as data_type in routers
class AnimeNoID(BaseModel):
    title : str
    fr_title : str
    genres : list[str]
    episodes : int
    oavs: int

#TODO :
#<> add User model
    #<> watchlist ?
    #<> profile ?
    #<> reviews ?
    #<> (do stats and graphs on most liked ???)