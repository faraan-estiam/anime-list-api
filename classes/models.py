from pydantic import BaseModel
from uuid import UUID

class Anime(BaseModel):
    uid : UUID
    title : str
    fr_title : str
    genres : list[str]
    episodes : int
    oavs: int
    #user_reviews : str | None = None

#TODO :
#<> add User model
    #<> watchlist ?
    #<> profile ?
    #<> reviews ?
    #<> (do stats and graphs on most liked ???)