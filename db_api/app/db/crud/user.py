from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Optional

from api_models.user import UserCreate
from core.auth import hash_password, verify_password
from db import crud
from db.schemas.user import User


def auth(username: str, password: str, db: Session) -> Optional[User]:
    user = read_by_username(username=username, db=db)

    if user is not None:
        if not user.enabled or not verify_password(password, user.password):
            raise ValueError("Invalid username or password")

        return user

    return None


def create_or_read(model: UserCreate, db: Session) -> User:
    obj = User(
        default_alert_queue=crud.queue.read_by_value(value=model.default_alert_queue, db=db),
        default_event_queue=crud.queue.read_by_value(value=model.default_event_queue, db=db),
        display_name=model.display_name,
        email=model.email,
        enabled=model.enabled,
        password=hash_password(model.password),
        roles=crud.user_role.read_by_values(values=model.roles, db=db),
        username=model.username,
    )

    if crud.helpers.create(obj=obj, db=db):
        return obj

    return read_by_username(username=model.username, db=db)


def read_by_username(username: Optional[str], db: Session) -> User:

    return db.execute(select(User).where(User.username == username)).scalars().one()
