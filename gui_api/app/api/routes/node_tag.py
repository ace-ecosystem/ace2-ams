import json

from fastapi import APIRouter, Query, Request, Response
from typing import Optional
from uuid import UUID

from api import db_api
from api.routes import helpers
from api_models.node_tag import NodeTagCreate, NodeTagRead


router = APIRouter(
    prefix="/node/tag",
    tags=["Node Tag"],
)


#
# CREATE
#


def create_node_tag(create: NodeTagCreate, request: Request, response: Response):
    result = db_api.post(path="/node/tag/", payload=json.loads(create.json()))

    response.headers["Content-Location"] = request.url_for("get_node_tag", uuid=result["uuid"])


helpers.api_route_create(router, create_node_tag)


#
# READ
#


def get_all_node_tags(limit: Optional[int] = Query(50, le=100), offset: Optional[int] = Query(0)):
    return db_api.get(path=f"/node/tag/?limit={limit}&offset={offset}")


def get_node_tag(uuid: UUID):
    return db_api.get(path=f"/node/tag/{uuid}")


helpers.api_route_read_all(router, get_all_node_tags, NodeTagRead)
helpers.api_route_read(router, get_node_tag, NodeTagRead)
