from sqlalchemy.orm import Session

from api_models.node_directive import NodeDirectiveCreate
from db import crud


def create_or_read(value: str, db: Session):
    return crud.node_directive.create_or_read(model=NodeDirectiveCreate(value=value), db=db)
