from sqlalchemy.orm import Session

from api_models.metadata_directive import MetadataDirectiveCreate
from db import crud


def create_or_read(value: str, db: Session):
    return crud.metadata_directive.create_or_read(model=MetadataDirectiveCreate(value=value), db=db)
