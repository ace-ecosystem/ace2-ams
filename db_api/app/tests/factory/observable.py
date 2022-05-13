from datetime import datetime
from sqlalchemy.orm import Session
from typing import Optional
from uuid import uuid4

from api_models.node_directive import NodeDirectiveCreate
from api_models.node_tag import NodeTagCreate
from api_models.observable import ObservableCreate
from api_models.observable_type import ObservableTypeCreate
from db import crud
from db.schemas.analysis import Analysis
from db.schemas.observable import Observable
from tests import factory


def create(
    type: str,
    value: str,
    parent_analysis: Analysis,
    db: Session,
    context: Optional[str] = None,
    directives: Optional[list[str]] = None,
    expires_on: Optional[datetime] = None,
    for_detection: bool = False,
    history_username: Optional[str] = None,
    redirection: Optional[Observable] = None,
    tags: Optional[list[str]] = None,
    threat_actors: Optional[list[str]] = None,
    threats: Optional[list[str]] = None,
    time: Optional[datetime] = None,
) -> Observable:
    crud.observable_type.create_or_read(model=ObservableTypeCreate(value=type), db=db)

    obj = crud.observable.create_or_read(
        model=ObservableCreate(
            context=context,
            expires_on=expires_on,
            for_detection=for_detection,
            history_username=history_username,
            # The root_analysis_uuid does not matter in this case. It is only used when the observable
            # you are adding also includes child analysis objects so that they get associated with the
            # correct root analysis.
            root_analysis_uuid=uuid4(),
            time=time or crud.helpers.utcnow(),
            type=type,
            value=value,
        ),
        db=db,
    )

    if directives is not None:
        obj.directives = [crud.node_directive.create_or_read(model=NodeDirectiveCreate(value=d)) for d in directives]

    if redirection is not None:
        obj.redirection = redirection

    if tags is not None:
        obj.tags = [crud.node_tag.create_or_read(model=NodeTagCreate(value=t), db=db) for t in tags]

    if threat_actors:
        obj.threat_actors = [factory.node_threat_actor.create(value=t, db=db) for t in threat_actors]

    if threats:
        obj.threats = [factory.node_threat.create(value=t, db=db) for t in threats]

    # Add the observable to its parent analysis
    parent_analysis.child_observables.append(obj)

    return obj
