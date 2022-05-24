from sqlalchemy.orm import Session
from uuid import UUID

from api_models.node_relationship_type import NodeRelationshipTypeCreate
from db import crud
from db.schemas.node_relationship_type import NodeRelationshipType


def create_or_read(model: NodeRelationshipTypeCreate, db: Session) -> NodeRelationshipType:
    obj = NodeRelationshipType(description=model.description, uuid=model.uuid, value=model.value)

    if crud.helpers.create(obj=obj, db=db):
        return obj

    return read_by_value(value=model.value, db=db)


def read_by_uuid(uuid: UUID, db: Session) -> NodeRelationshipType:
    return crud.helpers.read_by_uuid(db_table=NodeRelationshipType, uuid=uuid, db=db)


def read_by_value(value: str, db: Session) -> NodeRelationshipType:
    return crud.helpers.read_by_value(db_table=NodeRelationshipType, value=value, db=db)
