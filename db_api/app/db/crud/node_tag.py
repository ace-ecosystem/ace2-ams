from sqlalchemy.orm import Session
from typing import Optional

from api_models.node_tag import NodeTagCreate
from db import crud
from db.schemas.node_tag import NodeTag


def create(model: NodeTagCreate, db: Session) -> NodeTag:
    obj = read_by_value(value=model.value, db=db)

    if obj is None:
        obj = NodeTag(**model.dict())
        db.add(obj)
        db.flush()

    return obj


def read_by_value(value: str, db: Session) -> Optional[NodeTag]:
    return crud.helpers.read_by_value(db_table=NodeTag, value=value, db=db)


def read_by_values(values: list[str], db: Session) -> list[NodeTag]:
    return crud.helpers.read_by_values(db_table=NodeTag, values=values, db=db)
