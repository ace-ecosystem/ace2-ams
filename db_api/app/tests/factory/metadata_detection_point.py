from sqlalchemy.orm import Session

from api_models.metadata_detection_point import MetadataDetectionPointCreate
from db import crud


def create_or_read(value: str, db: Session):
    return crud.metadata_detection_point.create_or_read(model=MetadataDetectionPointCreate(value=value), db=db)
