from sqlalchemy.orm import Session

from api_models.metadata_display_value import MetadataDisplayValueCreate
from db import crud


def create_or_read(value: str, db: Session):
    return crud.metadata_display_value.create_or_read(model=MetadataDisplayValueCreate(value=value), db=db)
