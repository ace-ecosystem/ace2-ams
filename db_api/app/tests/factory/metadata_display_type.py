from sqlalchemy.orm import Session

from api_models.metadata_display_type import MetadataDisplayTypeCreate
from db import crud


def create_or_read(value: str, db: Session):
    return crud.metadata_display_type.create_or_read(model=MetadataDisplayTypeCreate(value=value), db=db)
