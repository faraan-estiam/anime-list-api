from pydantic import BaseModel
from uuid import UUID

class Anime(BaseModel):
    uid : UUID
    title : str
    fr_title : str | None = None
    genres : list[str] | None = None
    episodes : int | None = None
    oavs : int | None = None