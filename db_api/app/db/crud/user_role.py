from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql.selectable import Select
from uuid import UUID

from api_models.user_role import UserRoleCreate, UserRoleUpdate
from db import crud
from db.schemas.user_role import UserRole


def build_read_all_query() -> Select:
    return select(UserRole).order_by(UserRole.value)


def create_or_read(model: UserRoleCreate, db: Session) -> UserRole:
    obj = UserRole(**model.dict())

    if crud.helpers.create(obj=obj, db=db):
        return obj

    return read_by_value(value=model.value, db=db)


def delete(uuid: UUID, db: Session) -> bool:
    return crud.helpers.delete(uuid=uuid, db_table=UserRole, db=db)


def read_all(db: Session) -> list[UserRole]:
    return db.execute(build_read_all_query()).scalars().all()


def read_by_uuid(uuid: UUID, db: Session) -> UserRole:
    return crud.helpers.read_by_uuid(db_table=UserRole, uuid=uuid, db=db)


def read_by_value(value: str, db: Session) -> UserRole:
    return crud.helpers.read_by_value(db_table=UserRole, value=value, db=db)


def read_by_values(values: list[str], db: Session) -> list[UserRole]:
    return crud.helpers.read_by_values(db_table=UserRole, values=values, db=db)


def update(uuid: UUID, model: UserRoleUpdate, db: Session) -> bool:
    return crud.helpers.update(uuid=uuid, update_model=model, db_table=UserRole, db=db)
