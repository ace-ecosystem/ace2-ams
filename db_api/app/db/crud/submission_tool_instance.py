from sqlalchemy.orm import Session
from uuid import UUID

from api_models.submission_tool_instance import SubmissionToolInstanceCreate
from db import crud
from db.schemas.submission_tool_instance import SubmissionToolInstance


def create_or_read(model: SubmissionToolInstanceCreate, db: Session) -> SubmissionToolInstance:
    obj = SubmissionToolInstance(**model.dict())

    if crud.helpers.create(obj=obj, db=db):
        return obj

    return read_by_value(value=model.value, db=db)


def read_by_uuid(uuid: UUID, db: Session) -> SubmissionToolInstance:
    return crud.helpers.read_by_uuid(db_table=SubmissionToolInstance, uuid=uuid, db=db)


def read_by_value(value: str, db: Session) -> SubmissionToolInstance:
    return crud.helpers.read_by_value(db_table=SubmissionToolInstance, value=value, db=db)
