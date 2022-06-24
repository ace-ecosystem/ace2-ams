import json

from fastapi import APIRouter, Request, Response, status
from uuid import UUID

from api import db_api
from api.routes import helpers
from api_models.event_comment import EventCommentCreate, EventCommentRead, EventCommentUpdate


router = APIRouter(
    prefix="/event/comment",
    tags=["Event Comment"],
)


#
# CREATE
#


def create_event_comments(
    event_comments: list[EventCommentCreate],
    request: Request,
    response: Response,
):
    db_api.post(
        path="/event/comment/",
        payload=[json.loads(c.json(exclude_unset=True)) for c in event_comments],
        expected_status=status.HTTP_201_CREATED,
    )

    response.headers["Content-Location"] = request.url_for("get_event_comment", uuid=event_comments[-1].uuid)


helpers.api_route_create(router, create_event_comments)


#
# READ
#


def get_event_comment(uuid: UUID):
    return db_api.get(path=f"/event/comment/{uuid}", expected_status=status.HTTP_200_OK)


helpers.api_route_read(router, get_event_comment, EventCommentRead)


#
# UPDATE
#


def update_comment(
    uuid: UUID,
    event_comment: EventCommentUpdate,
    request: Request,
    response: Response,
):
    db_api.patch(
        path=f"/event/comment/{uuid}",
        payload=json.loads(event_comment.json()),
    )

    response.headers["Content-Location"] = request.url_for("get_event_comment", uuid=uuid)


helpers.api_route_update(router, update_comment)
