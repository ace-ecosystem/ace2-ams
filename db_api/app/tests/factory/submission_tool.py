from sqlalchemy.orm import Session

from api_models.submission_tool import SubmissionToolCreate
from db import crud


def create_or_read(value: str, db: Session):
    return crud.submission_tool.create_or_read(model=SubmissionToolCreate(value=value), db=db)
