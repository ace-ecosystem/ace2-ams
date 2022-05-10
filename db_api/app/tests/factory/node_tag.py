from sqlalchemy.orm import Session

from api_models.node_tag import NodeTagCreate
from db import crud


def create(value: str, db: Session):
    return crud.node_tag.create(model=NodeTagCreate(value=value), db=db)
