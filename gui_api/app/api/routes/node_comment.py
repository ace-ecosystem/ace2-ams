import json

from fastapi import APIRouter, Request, Response, status
from uuid import UUID

from api import db_api
from api.routes import helpers
from api_models.node_comment import NodeCommentCreate, NodeCommentRead, NodeCommentUpdate


router = APIRouter(
    prefix="/node/comment",
    tags=["Node Comment"],
)


#
# CREATE
#


def create_node_comments(
    node_comments: list[NodeCommentCreate],
    request: Request,
    response: Response,
):
    db_api.post(
        path="/node/comment/",
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


#
# UPDATE
#


def update_comment(
    uuid: UUID,
    node_comment: NodeCommentUpdate,
    request: Request,
    response: Response,
):
    db_api.patch(
        path=f"/node/comment/{uuid}",
        payload=json.loads(node_comment.json()),
    )

    response.headers["Content-Location"] = request.url_for("get_node_comment", uuid=uuid)


helpers.api_route_update(router, update_comment)
