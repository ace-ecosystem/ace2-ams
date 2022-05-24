from sqlalchemy.orm import Session

from api_models.node_comment import NodeCommentCreate
from db import crud
from db.schemas.node import Node
from tests import factory


def create_or_read(node: Node, username: str, value: str, db: Session):
    factory.user.create_or_read(username=username, db=db)

    obj = crud.node_comment.create_or_read(
        model=NodeCommentCreate(node_uuid=node.uuid, username=username, value=value), db=db
    )

    db.commit()
    return obj
