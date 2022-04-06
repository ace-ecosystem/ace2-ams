import json

from fastapi import APIRouter, Depends, Request, Response, status
from typing import List
from uuid import UUID

from api import db_api
from api.routes import helpers
from api_models.node_comment import NodeCommentCreate, NodeCommentRead
from core.auth import validate_access_token


router = APIRouter(
    prefix="/node/comment",
    tags=["Node Comment"],
)


#
# CREATE
#


def create_node_comments(
    node_comments: List[NodeCommentCreate],
    request: Request,
    response: Response,
    claims: dict = Depends(validate_access_token),
):
    db_api.post(
        path=f"/node/comment/?history_username={claims['sub']}",
        payload=[json.loads(c.json(exclude_unset=True)) for c in node_comments],
        expected_status=status.HTTP_201_CREATED,
    )

    response.headers["Content-Location"] = request.url_for("get_node_comment", uuid=node_comments[-1].uuid)


helpers.api_route_create(router, create_node_comments)


#
# READ
#


def get_node_comment(uuid: UUID):
    return db_api.get(path=f"/node/comment/{uuid}", expected_status=status.HTTP_200_OK)


helpers.api_route_read(router, get_node_comment, NodeCommentRead)
