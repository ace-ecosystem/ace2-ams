from sqlalchemy.orm import Session
from typing import Optional

from api_models.observable_relationship import ObservableRelationshipCreate
from db import crud
from db.schemas.observable import Observable
from tests import factory


def create_or_read(
    observable: Observable,
    related_observable: Observable,
    type: str,
    db: Session,
    history_username: Optional[str] = None,
):
    factory.observable_relationship_type.create_or_read(value=type, db=db)

    obj = crud.observable_relationship.create_or_read(
        model=ObservableRelationshipCreate(
            history_username=history_username,
            observable_uuid=observable.uuid,
            related_observable_uuid=related_observable.uuid,
            type=type,
        ),
        db=db,
    )

    db.commit()
    return obj
