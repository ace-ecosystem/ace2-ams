from sqlalchemy.orm import Session
from uuid import UUID

from api_models.node_tag import NodeTagCreate
from db import crud
from db.schemas.node_tag import NodeTag


def create_or_read(model: NodeTagCreate, db: Session) -> NodeTag:
    obj = NodeTag(**model.dict())

    if crud.helpers.create(obj=obj, db=db):
        return obj

    return read_by_value(value=model.value, db=db)


def read_by_uuid(uuid: UUID, db: Session) -> NodeTag:
    return crud.helpers.read_by_uuid(db_table=NodeTag, uuid=uuid, db=db)


def read_by_value(value: str, db: Session) -> NodeTag:
    return crud.helpers.read_by_value(db_table=NodeTag, value=value, db=db)


def read_by_values(values: list[str], db: Session) -> list[NodeTag]:
    return crud.helpers.read_by_values(db_table=NodeTag, values=values, db=db)
