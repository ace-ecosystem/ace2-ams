from datetime import datetime
from sqlalchemy.orm import Session
from typing import Optional

from api_models.observable import ObservableCreate
from db import crud
from db.schemas.analysis import Analysis
from db.schemas.observable import Observable
from tests import factory


def create_or_read(
    type: str,
    value: str,
    parent_analysis: Analysis,
    db: Session,
    context: Optional[str] = None,
    detection_points: Optional[str] = None,
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
    factory.observable_type.create_or_read(value=type, db=db)

    if directives is not None:
        for directive in directives:
            factory.node_directive.create_or_read(value=directive, db=db)

    if tags is not None:
        for tag in tags:
            factory.tag.create_or_read(value=tag, db=db)

    if threat_actors:
        for threat_actor in threat_actors:
            factory.node_threat_actor.create_or_read(value=threat_actor, db=db)

    if threats:
        for threat in threats:
            factory.node_threat.create_or_read(value=threat, db=db)

    obj = crud.observable.create_or_read(
        model=ObservableCreate(
            context=context,
            detection_points=detection_points or [],
            directives=directives or [],
            expires_on=expires_on,
            for_detection=for_detection,
            history_username=history_username,
            tags=tags or [],
            threat_actors=threat_actors or [],
            threats=threats or [],
            time=time or crud.helpers.utcnow(),
            type=type,
            value=value,
        ),
        parent_analysis=parent_analysis,
        db=db,
    )

    if redirection is not None:
        obj.redirection = redirection

    # Add the observable to its parent analysis
    parent_analysis.child_observables.append(obj)

    return obj
