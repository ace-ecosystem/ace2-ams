from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql.selectable import Select
from uuid import UUID

from api_models.observable_relationship_type import ObservableRelationshipTypeCreate, ObservableRelationshipTypeUpdate
from db import crud
from db.schemas.observable_relationship_type import ObservableRelationshipType


def build_read_all_query() -> Select:
    return select(ObservableRelationshipType).order_by(ObservableRelationshipType.value)


def create_or_read(model: ObservableRelationshipTypeCreate, db: Session) -> ObservableRelationshipType:
    obj = ObservableRelationshipType(description=model.description, uuid=model.uuid, value=model.value)

    if crud.helpers.create(obj=obj, db=db):
        return obj

    return read_by_value(value=model.value, db=db)


def delete(uuid: UUID, db: Session) -> bool:
    return crud.helpers.delete(uuid=uuid, db_table=ObservableRelationshipType, db=db)


def read_all(db: Session) -> list[ObservableRelationshipType]:
    return db.execute(build_read_all_query()).scalars().all()


def read_by_uuid(uuid: UUID, db: Session) -> ObservableRelationshipType:
    return crud.helpers.read_by_uuid(db_table=ObservableRelationshipType, uuid=uuid, db=db)


def read_by_value(value: str, db: Session) -> ObservableRelationshipType:
    return crud.helpers.read_by_value(db_table=ObservableRelationshipType, value=value, db=db)


def update(uuid: UUID, model: ObservableRelationshipTypeUpdate, db: Session) -> bool:
    return crud.helpers.update(uuid=uuid, update_model=model, db_table=ObservableRelationshipType, db=db)
