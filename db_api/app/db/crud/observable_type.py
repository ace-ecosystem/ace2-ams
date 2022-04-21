from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Optional

from db.schemas.observable_type import ObservableType


def create_observable_type(value: str, db: Session, description: str = None) -> ObservableType:
    return read_observable_type(value=value, db=db) or ObservableType(description=description, value=value)


def read_observable_type(value: str, db: Session) -> Optional[ObservableType]:
    return db.execute(select(ObservableType).where(ObservableType.value == value)).scalars().one_or_none()
