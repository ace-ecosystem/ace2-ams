from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql.selectable import Select
from uuid import UUID

from api_models.node_relationship_type import NodeRelationshipTypeCreate, NodeRelationshipTypeUpdate
from db import crud
from db.schemas.node_relationship_type import NodeRelationshipType


def build_read_all_query() -> Select:
    return select(NodeRelationshipType).order_by(NodeRelationshipType.value)


def create_or_read(model: NodeRelationshipTypeCreate, db: Session) -> NodeRelationshipType:
    obj = NodeRelationshipType(description=model.description, uuid=model.uuid, value=model.value)

    if crud.helpers.create(obj=obj, db=db):
        return obj

    return read_by_value(value=model.value, db=db)


def delete(uuid: UUID, db: Session) -> bool:
    return crud.helpers.delete(uuid=uuid, db_table=NodeRelationshipType, db=db)


def read_all(db: Session) -> list[NodeRelationshipType]:
    return db.execute(build_read_all_query()).scalars().all()


def read_by_uuid(uuid: UUID, db: Session) -> NodeRelationshipType:
    return crud.helpers.read_by_uuid(db_table=NodeRelationshipType, uuid=uuid, db=db)


def read_by_value(value: str, db: Session) -> NodeRelationshipType:
    return crud.helpers.read_by_value(db_table=NodeRelationshipType, value=value, db=db)


def update(uuid: UUID, model: NodeRelationshipTypeUpdate, db: Session) -> bool:
    return crud.helpers.update(uuid=uuid, update_model=model, db_table=NodeRelationshipType, db=db)
