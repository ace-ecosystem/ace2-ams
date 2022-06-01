from sqlalchemy.orm import Session

from api_models.node_relationship_type import NodeRelationshipTypeCreate
from db import crud


def create_or_read(value: str, db: Session):
    return crud.node_relationship_type.create_or_read(model=NodeRelationshipTypeCreate(value=value), db=db)
