from sqlalchemy.orm import Session

from api_models.node_tag import NodeTagCreate
from db import crud


def create_or_read(value: str, db: Session):
    return crud.node_tag.create_or_read(model=NodeTagCreate(value=value), db=db)
