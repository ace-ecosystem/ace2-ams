from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from api_models.user_role import UserRoleCreate
from db import crud
from db.schemas.user_role import UserRole


def create(model: UserRoleCreate, db: Session) -> UserRole:
    obj = read_by_value(value=model.value, db=db)

    if obj is None:
        obj = UserRole(**model.dict())
        db.add(obj)
        db.flush()

    return obj


def read_by_uuid(uuid: UUID, db: Session) -> UserRole:
    return crud.helpers.read_by_uuid(db_table=UserRole, uuid=uuid, db=db)


def read_by_value(value: str, db: Session) -> Optional[UserRole]:
    return crud.helpers.read_by_value(db_table=UserRole, value=value, db=db)
