from sqlalchemy.orm import Session

from api_models.observable_relationship_type import ObservableRelationshipTypeCreate
from db import crud


def create_or_read(value: str, db: Session):
    return crud.observable_relationship_type.create_or_read(model=ObservableRelationshipTypeCreate(value=value), db=db)
