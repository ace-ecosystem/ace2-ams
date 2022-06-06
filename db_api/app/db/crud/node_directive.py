from sqlalchemy.orm import Session
from uuid import UUID

from api_models.node_directive import NodeDirectiveCreate, NodeDirectiveUpdate
from db import crud
from db.schemas.node_directive import NodeDirective


def create_or_read(model: NodeDirectiveCreate, db: Session) -> NodeDirective:
    obj = NodeDirective(**model.dict())

    if crud.helpers.create(obj=obj, db=db):
        return obj

    return read_by_value(value=model.value, db=db)


def delete(uuid: UUID, db: Session) -> bool:
    return crud.helpers.delete(uuid=uuid, db_table=NodeDirective, db=db)


def read_all(db: Session) -> list[NodeDirective]:
    return crud.helpers.read_all(db_table=NodeDirective, order_by=NodeDirective.value, db=db)


def read_by_uuid(uuid: UUID, db: Session) -> NodeDirective:
    return crud.helpers.read_by_uuid(db_table=NodeDirective, uuid=uuid, db=db)


def read_by_value(value: str, db: Session) -> NodeDirective:
    return crud.helpers.read_by_value(db_table=NodeDirective, value=value, db=db)


def read_by_values(values: list[str], db: Session) -> list[NodeDirective]:
    return crud.helpers.read_by_values(db_table=NodeDirective, values=values, db=db)


def update(uuid: UUID, model: NodeDirectiveUpdate, db: Session) -> bool:
    return crud.helpers.update(uuid=uuid, update_model=model, db_table=NodeDirective, db=db)
