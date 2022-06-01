from sqlalchemy.orm import Session

from api_models.user_role import UserRoleCreate
from db import crud


def create_or_read(value: str, db: Session):
    return crud.user_role.create_or_read(model=UserRoleCreate(value=value), db=db)
