import json
import requests

from fastapi import APIRouter, HTTPException, Query, Request, Response, status
from typing import Optional
from uuid import UUID

from api_models.node_tag import NodeTagCreate, NodeTagRead
from api.routes import helpers
from core.config import get_settings


router = APIRouter(
    prefix="/node/tag",
    tags=["Node Tag"],
)


#
# CREATE
#


def create_node_tag(
    create: NodeTagCreate,
    request: Request,
    response: Response,
):

    try:
        result = requests.post(f"{get_settings().database_api_url}/node/tag/", json=json.loads(create.json()))
    except:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database API is unavailable",
            headers={"WWW-Authenticate": "Bearer"},
        )

    response.headers["Content-Location"] = request.url_for("get_node_tag", uuid=result.json()["uuid"])


helpers.api_route_create(router, create_node_tag)


#
# READ
#


def get_all_node_tags(
    limit: Optional[int] = Query(50, le=100),
    offset: Optional[int] = Query(0),
):
    try:
        result = requests.get(f"{get_settings().database_api_url}/node/tag/?limit={limit}&offset={offset}")
    except:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database API is unavailable",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return result.json()


def get_node_tag(uuid: UUID):
    try:
        result = requests.get(f"{get_settings().database_api_url}/node/tag/{uuid}")
    except:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database API is unavailable",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return result.json()


helpers.api_route_read_all(router, get_all_node_tags, NodeTagRead)
helpers.api_route_read(router, get_node_tag, NodeTagRead)
