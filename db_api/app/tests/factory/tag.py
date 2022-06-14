from sqlalchemy.orm import Session

from api_models.tag import TagCreate
from db import crud


def create_or_read(value: str, db: Session):
    return crud.tag.create_or_read(model=TagCreate(value=value), db=db)
