from sqlalchemy.orm import Session

from api_models.event_comment import EventCommentCreate
from db import crud
from db.schemas.event import Event
from tests import factory


def create_or_read(event: Event, username: str, value: str, db: Session):
    factory.user.create_or_read(username=username, db=db)

    obj = crud.event_comment.create_or_read(
        model=EventCommentCreate(node_uuid=event.uuid, username=username, value=value), db=db
    )

    db.commit()
    return obj
