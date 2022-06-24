import json

from fastapi import APIRouter, Request, Response, status
from uuid import UUID

from api import db_api
from api.routes import helpers
from api_models.submission_comment import SubmissionCommentCreate, SubmissionCommentRead, SubmissionCommentUpdate


router = APIRouter(
    prefix="/alert/comment",
    tags=["Submission Comment"],
)


#
# CREATE
#


def create_alert_comments(
    alert_comments: list[SubmissionCommentCreate],
    request: Request,
    response: Response,
):
    db_api.post(
        path="/submission/comment/",
        payload=[json.loads(c.json(exclude_unset=True)) for c in alert_comments],
        expected_status=status.HTTP_201_CREATED,
    )

    response.headers["Content-Location"] = request.url_for("get_alert_comment", uuid=alert_comments[-1].uuid)


helpers.api_route_create(router, create_alert_comments)


#
# READ
#


def get_alert_comment(uuid: UUID):
    return db_api.get(path=f"/submission/comment/{uuid}", expected_status=status.HTTP_200_OK)


helpers.api_route_read(router, get_alert_comment, SubmissionCommentRead)


#
# UPDATE
#


def update_comment(
    uuid: UUID,
    alert_comment: SubmissionCommentUpdate,
    request: Request,
    response: Response,
):
    db_api.patch(
        path=f"/submission/comment/{uuid}",
        payload=json.loads(alert_comment.json()),
    )

    response.headers["Content-Location"] = request.url_for("get_alert_comment", uuid=uuid)


helpers.api_route_update(router, update_comment)
