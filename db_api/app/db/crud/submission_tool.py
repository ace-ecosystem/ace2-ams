from sqlalchemy.orm import Session
from uuid import UUID

from api_models.submission_tool import SubmissionToolCreate, SubmissionToolUpdate
from db import crud
from db.schemas.submission_tool import SubmissionTool


def create_or_read(model: SubmissionToolCreate, db: Session) -> SubmissionTool:
    obj = SubmissionTool(**model.dict())

    if crud.helpers.create(obj=obj, db=db):
        return obj

    return read_by_value(value=model.value, db=db)


def delete(uuid: UUID, db: Session) -> bool:
    return crud.helpers.delete(uuid=uuid, db_table=SubmissionTool, db=db)


def read_all(db: Session) -> list[SubmissionTool]:
    return crud.helpers.read_all(db_table=SubmissionTool, order_by=SubmissionTool.value, db=db)


def read_by_uuid(uuid: UUID, db: Session) -> SubmissionTool:
    return crud.helpers.read_by_uuid(db_table=SubmissionTool, uuid=uuid, db=db)


def read_by_value(value: str, db: Session) -> SubmissionTool:
    return crud.helpers.read_by_value(db_table=SubmissionTool, value=value, db=db)


def update(uuid: UUID, model: SubmissionToolUpdate, db: Session) -> bool:
    return crud.helpers.update(uuid=uuid, update_model=model, db_table=SubmissionTool, db=db)
