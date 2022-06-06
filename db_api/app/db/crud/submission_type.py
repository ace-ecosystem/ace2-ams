from sqlalchemy.orm import Session
from uuid import UUID

from api_models.submission_type import SubmissionTypeCreate, SubmissionTypeUpdate
from db import crud
from db.schemas.submission_type import SubmissionType


def create_or_read(model: SubmissionTypeCreate, db: Session) -> SubmissionType:
    obj = SubmissionType(**model.dict())

    if crud.helpers.create(obj=obj, db=db):
        return obj

    return read_by_value(value=model.value, db=db)


def delete(uuid: UUID, db: Session) -> bool:
    return crud.helpers.delete(uuid=uuid, db_table=SubmissionType, db=db)


def read_all(db: Session) -> list[SubmissionType]:
    return crud.helpers.read_all(db_table=SubmissionType, order_by=SubmissionType.value, db=db)


def read_by_uuid(uuid: UUID, db: Session) -> SubmissionType:
    return crud.helpers.read_by_uuid(db_table=SubmissionType, uuid=uuid, db=db)


def read_by_value(value: str, db: Session) -> SubmissionType:
    return crud.helpers.read_by_value(db_table=SubmissionType, value=value, db=db)


def update(uuid: UUID, model: SubmissionTypeUpdate, db: Session) -> bool:
    return crud.helpers.update(uuid=uuid, update_model=model, db_table=SubmissionType, db=db)
