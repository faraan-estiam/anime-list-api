from fastapi import FastAPI

# Documentation
from documentation.description import api_description
from documentation.tags import tags_metadata

#importing routes
import routers.router_anime
import routers.router_auth


api = FastAPI(
    title='anime-list-api',
    description=api_description,
    openapi_tags=tags_metadata,
    docs_url='/'
)

api.include_router(routers.router_anime.router)
api.include_router(routers.router_auth.router)