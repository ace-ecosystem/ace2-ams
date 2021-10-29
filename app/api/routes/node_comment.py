from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session
from uuid import UUID, uuid4

from api.models.node_comment import NodeCommentCreate, NodeCommentRead, NodeCommentUpdate
from api.routes import helpers
from db import crud
from db.database import get_db
from db.schemas.node import Node
from db.schemas.node_comment import NodeComment


router = APIRouter(
    prefix="/node/comment",
    tags=["Node Comment"],
)


#
# CREATE
#


def create_node_comment(
    node_comment: NodeCommentCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    # Create the new node comment
    new_comment = NodeComment(**node_comment.dict())

    # Make sure the node actually exists
    db_node = crud.read(uuid=node_comment.node_uuid, db_table=Node, db=db)

    # This counts a modifying the node, so it should receive a new version.
    db_node.version = uuid4()

    # Set the user on the comment
    new_comment.user = crud.read_user_by_username(username=node_comment.user, db=db)

    # Save the new comment to the database
    db.add(new_comment)
    crud.commit(db)

    response.headers["Content-Location"] = request.url_for("get_node_comment", uuid=new_comment.uuid)


helpers.api_route_create(router, create_node_comment)


#
# READ
#


# def get_all_node_directives(db: Session = Depends(get_db)):
#     return crud.read_all(db_table=NodeDirective, db=db)


def get_node_comment(uuid: UUID, db: Session = Depends(get_db)):
    return crud.read(uuid=uuid, db_table=NodeComment, db=db)


# It does not make sense to have a get_all_node_comments route at this point (and certainly not without pagination).
# helpers.api_route_read_all(router, get_all_node_directives, List[NodeDirectiveRead])
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
    # Read the current node comment from the database
    db_node_comment: NodeComment = crud.read(uuid=uuid, db_table=NodeComment, db=db)

    # Read the node from the database
    db_node = crud.read(uuid=db_node_comment.node_uuid, db_table=Node, db=db)

    # Set the new comment value
    db_node_comment.value = node_comment.value

    # Modifying the comment counts as modifying the node, so it should receive a new version
    db_node.version = uuid4()

    crud.commit(db)

    response.headers["Content-Location"] = request.url_for("get_node_comment", uuid=uuid)


helpers.api_route_update(router, update_node_comment)


#
# DELETE
#


def delete_node_comment(uuid: UUID, db: Session = Depends(get_db)):
    crud.delete(uuid=uuid, db_table=NodeComment, db=db)


helpers.api_route_delete(router, delete_node_comment)
