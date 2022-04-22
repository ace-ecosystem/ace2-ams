from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Optional
from uuid import uuid4

from db.crud.observable_type import read_observable_type
from db.schemas.observable import Observable
from db.schemas.observable_type import ObservableType


def create_observable(
    type: str,
    value: str,
    db: Session,
    context: Optional[str] = None,
    expires_on: Optional[datetime] = None,
    for_detection: bool = False,
    redirection: Optional[Observable] = None,
    time: Optional[datetime] = None,
) -> Observable:
    obj = read_observable(type=type, value=value, db=db)

    if obj is None:
        if time is None:
            time = datetime.now(timezone.utc)

        obj = Observable(
            context=context,
            expires_on=expires_on,
            for_detection=for_detection,
            redirection=redirection,
            time=time,
            type=read_observable_type(value=type, db=db),
            uuid=uuid4(),
            value=value,
            version=uuid4(),
        )

    return obj


def read_observable(type: str, value: str, db: Session) -> Optional[Observable]:
    """Returns the Observable with the given type and value if it exists."""

    return (
        db.execute(
            select(Observable).join(ObservableType).where(ObservableType.value == type, Observable.value == value)
        )
        .scalars()
        .one_or_none()
    )
