from sqlalchemy.orm import Session
from uuid import UUID

from api_models.submission_tool_instance import SubmissionToolInstanceCreate, SubmissionToolInstanceUpdate
from db import crud
from db.schemas.submission_tool_instance import SubmissionToolInstance


def create_or_read(model: SubmissionToolInstanceCreate, db: Session) -> SubmissionToolInstance:
    obj = SubmissionToolInstance(**model.dict())

    if crud.helpers.create(obj=obj, db=db):
        return obj

    return read_by_value(value=model.value, db=db)


def delete(uuid: UUID, db: Session) -> bool:
    return crud.helpers.delete(uuid=uuid, db_table=SubmissionToolInstance, db=db)


def read_all(db: Session) -> list[SubmissionToolInstance]:
    return crud.helpers.read_all(db_table=SubmissionToolInstance, order_by=SubmissionToolInstance.value, db=db)


def read_by_uuid(uuid: UUID, db: Session) -> SubmissionToolInstance:
    return crud.helpers.read_by_uuid(db_table=SubmissionToolInstance, uuid=uuid, db=db)


def read_by_value(value: str, db: Session) -> SubmissionToolInstance:
    return crud.helpers.read_by_value(db_table=SubmissionToolInstance, value=value, db=db)


def update(uuid: UUID, model: SubmissionToolInstanceUpdate, db: Session) -> bool:
    return crud.helpers.update(uuid=uuid, update_model=model, db_table=SubmissionToolInstance, db=db)
