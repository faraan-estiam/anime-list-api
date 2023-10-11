from fastapi import FastAPI

#importing routes
import routers.router_anime


api = FastAPI(
    title="anime-list-api"
)

api.include_router(routers.router_anime.router)