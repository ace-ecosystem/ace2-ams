from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.orm import Session
from uuid import UUID

from api.routes import helpers
from api_models.node_comment import NodeCommentCreate, NodeCommentRead, NodeCommentUpdate
from db import crud
from db.database import get_db
from exceptions.db import UuidNotFoundInDatabase, ValueNotFoundInDatabase


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
    db: Session = Depends(get_db),
):
    for node_comment in node_comments:
        try:
            obj = crud.node_comment.create_or_read(model=node_comment, db=db)
        except (UuidNotFoundInDatabase, ValueNotFoundInDatabase) as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

        response.headers["Content-Location"] = request.url_for("get_node_comment", uuid=obj.uuid)

    db.commit()


helpers.api_route_create(router, create_node_comments)


#
# READ
#


def get_node_comment(uuid: UUID, db: Session = Depends(get_db)):
    try:
        return crud.node_comment.read_by_uuid(uuid=uuid, db=db)
    except UuidNotFoundInDatabase as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Comment {uuid} does not exist") from e


helpers.api_route_read(router, get_node_comment, NodeCommentRead)


#
# UPDATE
#


def update_node_comment(
    uuid: UUID,
    node_comment: NodeCommentUpdate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    try:
        if not crud.node_comment.update(uuid=uuid, model=node_comment, db=db):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Unable to comment {uuid}")
    except (UuidNotFoundInDatabase, ValueNotFoundInDatabase) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()

    response.headers["Content-Location"] = request.url_for("get_node_comment", uuid=uuid)


helpers.api_route_update(router, update_node_comment)


#
# DELETE
#


def delete_node_comment(uuid: UUID, history_username: str, db: Session = Depends(get_db)):
    try:
        crud.node_comment.delete(uuid=uuid, history_username=history_username, db=db)
    except (UuidNotFoundInDatabase, ValueNotFoundInDatabase) as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e

    db.commit()


helpers.api_route_delete(router, delete_node_comment)
