from sqlalchemy.orm import Session

from api_models.metadata_tag import MetadataTagCreate
from db import crud


def create_or_read(value: str, db: Session):
    return crud.metadata_tag.create_or_read(model=MetadataTagCreate(value=value), db=db)
