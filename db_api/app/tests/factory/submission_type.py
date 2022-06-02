from sqlalchemy.orm import Session

from api_models.submission_type import SubmissionTypeCreate
from db import crud


def create_or_read(value: str, db: Session):
    return crud.submission_type.create_or_read(model=SubmissionTypeCreate(value=value), db=db)
