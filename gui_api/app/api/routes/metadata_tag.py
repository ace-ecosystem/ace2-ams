import json

from fastapi import APIRouter, Query, Request, Response
from typing import Optional
from uuid import UUID

from api import db_api
from api.routes import helpers
from api_models.metadata_tag import MetadataTagCreate, MetadataTagRead


router = APIRouter(
    prefix="/metadata/tag",
    tags=["Tag"],
)


#
# CREATE
#


def create_tag(create: MetadataTagCreate, request: Request, response: Response):
    result = db_api.post(path="/metadata/tag/", payload=json.loads(create.json()))

    response.headers["Content-Location"] = request.url_for("get_tag", uuid=result["uuid"])


helpers.api_route_create(router, create_tag)


#
# READ
#


def get_all_tags(limit: Optional[int] = Query(50, le=100), offset: Optional[int] = Query(0)):
    return db_api.get(path=f"/metadata/tag/?limit={limit}&offset={offset}")


def get_tag(uuid: UUID):
    return db_api.get(path=f"/metadata/tag/{uuid}")


helpers.api_route_read_all(router, get_all_tags, MetadataTagRead)
helpers.api_route_read(router, get_tag, MetadataTagRead)
