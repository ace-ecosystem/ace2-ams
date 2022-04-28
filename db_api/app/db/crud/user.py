from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Optional

from core.auth import verify_password
from db.schemas.user import User


def auth(username: str, password: str, db: Session) -> Optional[User]:
    user = read_by_username(username=username, db=db)

    if user is not None:
        if not user.enabled or not verify_password(password, user.password):
            raise ValueError("Invalid username or password")

        return user

    return None


def read_by_username(username: str, db: Session) -> Optional[User]:
    return db.execute(select(User).where(User.username == username)).scalars().one_or_none()
