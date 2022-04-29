from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Optional

from api_models.observable import ObservableCreate
from db import crud
from db.schemas.observable import Observable
from db.schemas.observable_type import ObservableType


def create(
    model: ObservableCreate,
    db: Session,
) -> Observable:
    obj = read_by_type_value(type=model.type, value=model.value, db=db)

    # TODO: Add the Analysis objects if the ObservableCreate has analyses

    if obj is None:
        obj = Observable(
            context=model.context,
            expires_on=model.expires_on,
            for_detection=model.for_detection,
            redirection=create(model=model.redirection, db=db) if model.redirection else None,
            time=model.time,
            type=crud.observable_type.read_by_value(value=model.type, db=db),
            value=model.value,
        )

        db.add(obj)
        db.flush()

    return obj


def read_by_type_value(type: str, value: str, db: Session) -> Optional[Observable]:
    """Returns the Observable with the given type and value if it exists."""

    return (
        db.execute(
            select(Observable).join(ObservableType).where(ObservableType.value == type, Observable.value == value)
        )
        .scalars()
        .one_or_none()
    )
