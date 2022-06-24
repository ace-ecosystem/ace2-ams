from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.orm import Session
from uuid import UUID

from api.routes import helpers
from api_models.submission_comment import SubmissionCommentCreate, SubmissionCommentRead, SubmissionCommentUpdate
from db import crud
from db.database import get_db
from exceptions.db import UuidNotFoundInDatabase, ValueNotFoundInDatabase


router = APIRouter(
    prefix="/submission/comment",
    tags=["Submission Comment"],
)


#
# CREATE
#


def create_submission_comments(
    submission_comments: list[SubmissionCommentCreate],
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    for submission_comment in submission_comments:
        try:
            obj = crud.submission_comment.create_or_read(model=submission_comment, db=db)
        except (UuidNotFoundInDatabase, ValueNotFoundInDatabase) as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

        response.headers["Content-Location"] = request.url_for("get_submission_comment", uuid=obj.uuid)

    db.commit()


helpers.api_route_create(router, create_submission_comments)


#
# READ
#


def get_submission_comment(uuid: UUID, db: Session = Depends(get_db)):
    try:
        return crud.submission_comment.read_by_uuid(uuid=uuid, db=db)
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Comment {uuid} does not exist") from e


helpers.api_route_read(router, get_submission_comment, SubmissionCommentRead)


#
# UPDATE
#


def update_submission_comment(
    uuid: UUID,
    submission_comment: SubmissionCommentUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    try:
        if not crud.submission_comment.update(uuid=uuid, model=submission_comment, db=db):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to comment {uuid}")
    except (UuidNotFoundInDatabase, ValueNotFoundInDatabase) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()

    response.headers["Content-Location"] = request.url_for("get_submission_comment", uuid=uuid)


helpers.api_route_update(router, update_submission_comment)


#
# DELETE
#


def delete_submission_comment(uuid: UUID, history_username: str, db: Session = Depends(get_db)):
    try:
        crud.submission_comment.delete(uuid=uuid, history_username=history_username, db=db)
    except (UuidNotFoundInDatabase, ValueNotFoundInDatabase) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()


helpers.api_route_delete(router, delete_submission_comment)
