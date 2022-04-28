from sqlalchemy.orm import Session
from typing import Optional

from api_models.node_directive import NodeDirectiveCreate
from db import crud
from db.schemas.node_directive import NodeDirective


def create(model: NodeDirectiveCreate, db: Session) -> NodeDirective:
    obj = read_by_value(value=model.value, db=db)

    if obj is None:
        obj = NodeDirective(**model.dict())
        db.add(obj)
        db.flush()

    return obj


def read_by_value(value: str, db: Session) -> Optional[NodeDirective]:
    return crud.helpers.read_by_value(db_table=NodeDirective, value=value, db=db)


def read_by_values(values: list[str], db: Session) -> list[NodeDirective]:
    return crud.helpers.read_by_values(db_table=NodeDirective, values=values, db=db)
