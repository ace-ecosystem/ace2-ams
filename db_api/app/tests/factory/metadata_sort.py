from sqlalchemy.orm import Session

from api_models.metadata_sort import MetadataSortCreate
from db import crud


def create_or_read(value: int, db: Session):
    return crud.metadata_sort.create_or_read(model=MetadataSortCreate(value=value), db=db)
