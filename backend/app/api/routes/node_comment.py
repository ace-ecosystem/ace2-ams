from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID, uuid4

from api.models.node_comment import NodeCommentCreate, NodeCommentRead, NodeCommentUpdate
from api.routes import helpers
from core.auth import validate_access_token
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


def create_node_comments(
    node_comments: List[NodeCommentCreate],
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
    username: str = Depends(validate_access_token),
):
    for node_comment in node_comments:
        # Create the new node comment
        new_comment = NodeComment(**node_comment.dict())

        # Make sure the node actually exists
        db_node: Node = crud.read(uuid=node_comment.node_uuid, db_table=Node, db=db)

        # This counts a modifying the node, so it should receive a new version.
        db_node.version = uuid4()

        # Set the user on the comment
        new_comment.user = crud.read_user_by_username(username=username, db=db)

        # Save the new comment to the database
        db.add(new_comment)
        crud.commit(db)

        # Add an entry to the correct history table based on the node_type.
        # Even though this is creating a comment, we treat it as though it is
        # modifying the node for history tracking purposes.
        diff = crud.Diff(field="comments", added_to_list=[node_comment.value])
        crud.record_comment_history(record_node=db_node, username=username, diff=diff, db=db)

        response.headers["Content-Location"] = request.url_for("get_node_comment", uuid=new_comment.uuid)


helpers.api_route_create(router, create_node_comments)


#
# READ
#


def get_node_comment(uuid: UUID, db: Session = Depends(get_db)):
    return crud.read(uuid=uuid, db_table=NodeComment, db=db)


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
    username: str = Depends(validate_access_token),
):
    # Read the current node comment from the database
    db_node_comment: NodeComment = crud.read(uuid=uuid, db_table=NodeComment, db=db)

    # Read the node from the database
    db_node: Node = crud.read(uuid=db_node_comment.node_uuid, db_table=Node, db=db)

    # Set the new comment value
    diff = crud.Diff(field="comments", added_to_list=[node_comment.value], removed_from_list=[db_node_comment.value])
    db_node_comment.value = node_comment.value

    # Modifying the comment counts as modifying the node, so it should receive a new version
    db_node.version = uuid4()

    crud.commit(db)

    # Add an entry to the correct history table based on the node_type.
    crud.record_comment_history(record_node=db_node, username=username, diff=diff, db=db)

    response.headers["Content-Location"] = request.url_for("get_node_comment", uuid=uuid)


helpers.api_route_update(router, update_node_comment)


#
# DELETE
#


def delete_node_comment(uuid: UUID, db: Session = Depends(get_db), username: str = Depends(validate_access_token)):
    # Read the current node comment from the database to get its value
    db_node_comment: NodeComment = crud.read(uuid=uuid, db_table=NodeComment, db=db)

    # Add an entry to the correct history table based on the node_type.
    diff = crud.Diff(field="comments", removed_from_list=[db_node_comment.value])
    crud.record_comment_history(record_node=db_node_comment.node, username=username, diff=diff, db=db)

    # Delete the comment
    crud.delete(uuid=uuid, db_table=NodeComment, db=db)


helpers.api_route_delete(router, delete_node_comment)
