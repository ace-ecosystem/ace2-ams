from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.orm import Session
from uuid import UUID

from api.routes import helpers
from api_models.event_comment import EventCommentCreate, EventCommentRead, EventCommentUpdate
from db import crud
from db.database import get_db
from exceptions.db import UuidNotFoundInDatabase, ValueNotFoundInDatabase


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
    db: Session = Depends(get_db),
):
    for event_comment in event_comments:
        try:
            obj = crud.event_comment.create_or_read(model=event_comment, db=db)
        except (UuidNotFoundInDatabase, ValueNotFoundInDatabase) as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

        response.headers["Content-Location"] = request.url_for("get_event_comment", uuid=obj.uuid)

    db.commit()


helpers.api_route_create(router, create_event_comments)


#
# READ
#


def get_event_comment(uuid: UUID, db: Session = Depends(get_db)):
    try:
        return crud.event_comment.read_by_uuid(uuid=uuid, db=db)
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Comment {uuid} does not exist") from e


helpers.api_route_read(router, get_event_comment, EventCommentRead)


#
# UPDATE
#


def update_event_comment(
    uuid: UUID,
    event_comment: EventCommentUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    try:
        if not crud.event_comment.update(uuid=uuid, model=event_comment, db=db):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to comment {uuid}")
    except (UuidNotFoundInDatabase, ValueNotFoundInDatabase) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()

    response.headers["Content-Location"] = request.url_for("get_event_comment", uuid=uuid)


helpers.api_route_update(router, update_event_comment)


#
# DELETE
#


def delete_event_comment(uuid: UUID, history_username: str, db: Session = Depends(get_db)):
    try:
        crud.event_comment.delete(uuid=uuid, history_username=history_username, db=db)
    except (UuidNotFoundInDatabase, ValueNotFoundInDatabase) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()


helpers.api_route_delete(router, delete_event_comment)
