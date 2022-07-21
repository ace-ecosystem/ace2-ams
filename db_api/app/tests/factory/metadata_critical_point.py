from sqlalchemy.orm import Session

from api_models.metadata_critical_point import MetadataCriticalPointCreate
from db import crud


def create_or_read(value: str, db: Session):
    return crud.metadata_critical_point.create_or_read(model=MetadataCriticalPointCreate(value=value), db=db)
