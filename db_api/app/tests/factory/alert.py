from datetime import datetime
from sqlalchemy.orm import Session
from typing import Optional, Union
from uuid import UUID, uuid4

from api_models.alert import AlertCreate
from api_models.alert_disposition import AlertDispositionCreate
from api_models.alert_type import AlertTypeCreate
from api_models.analysis_module_type import AnalysisModuleTypeCreate
from api_models.node_tag import NodeTagCreate
from api_models.node_threat_actor import NodeThreatActorCreate
from api_models.observable import ObservableCreate
from api_models.observable_type import ObservableTypeCreate
from db import crud
from db.schemas.event import Event
from tests import factory


def create(
    db: Session,
    alert_queue: str = "external",
    alert_type: str = "test_type",
    alert_uuid: Optional[Union[str, UUID]] = None,
    disposition: Optional[str] = None,
    event: Optional[Event] = None,
    event_time: datetime = None,
    history_username: Optional[str] = None,
    insert_time: datetime = None,
    name: str = "Test Alert",
    observables: Optional[list[ObservableCreate]] = None,
    owner: Optional[str] = None,
    tags: Optional[list[str]] = None,
    threat_actors: Optional[list[str]] = None,
    threats: Optional[list[str]] = None,
    tool: str = "test_tool",
    tool_instance: str = "test_tool_instance",
    update_time: Optional[datetime] = None,
    updated_by_user: str = "analyst",
):
    diffs = []

    # Set default values
    if alert_uuid is None:
        alert_uuid = uuid4()

    if event_time is None:
        event_time = crud.helpers.utcnow()

    if insert_time is None:
        insert_time = crud.helpers.utcnow()

    if observables is None:
        observables = []

    if update_time is None:
        update_time = crud.helpers.utcnow()

    # Create the alert type
    crud.alert_type.create(model=AlertTypeCreate(value=alert_type), db=db)

    # Create the owner user if one was given
    if owner is not None:
        factory.user.create(email=f"{owner}@{owner}.com", username=owner, db=db, alert_queue=alert_queue)
        diffs.append(crud.history.create_diff(field="owner", old=None, new=owner))

    # Create observable types for each observable that was given
    for observable in observables:
        crud.observable_type.create(model=ObservableTypeCreate(value=observable.type), db=db)

        for analysis in observable.analyses:
            # TODO: Make a factory function to create an analysis module type
            # crud.analysis_module_type.create(model=AnalysisModuleTypeCreate())
            pass

    alert = crud.alert.create(
        model=AlertCreate(
            event_time=event_time,
            insert_time=insert_time,
            name=name,
            owner=owner,
            queue=alert_queue,
            root_observables=observables,
            tool=tool,
            tool_instance=tool_instance,
            type=alert_type,
            uuid=alert_uuid,
        ),
        db=db,
    )

    if disposition:
        alert.disposition = crud.alert_disposition.create(model=AlertDispositionCreate(value=disposition), db=db)
        alert.disposition_time = update_time
        alert.disposition_user = factory.user.create(username=updated_by_user, display_name=updated_by_user, db=db)
        diffs.append(crud.history.create_diff(field="disposition", old=None, new=disposition))

    if event:
        alert.event = event

    if tags:
        alert.tags = [crud.node_tag.create(model=NodeTagCreate(value=t)) for t in tags]

    if threat_actors:
        alert.threat_actors = [
            crud.node_threat_actor.create(model=NodeThreatActorCreate(value=t)) for t in threat_actors
        ]

    if threats:
        alert.threats = [factory.node_threat.create(value=threat, db=db) for threat in threats]

    if history_username:
        # Add an entry to the history table
        crud.history.record_node_create_history(
            record_node=alert,
            action_by=factory.user.create(username=history_username, db=db),
            db=db,
        )

        if diffs and updated_by_user:
            crud.history.record_node_update_history(
                record_node=alert,
                action_by=factory.user.create(username=updated_by_user, db=db),
                action_time=update_time,
                diffs=diffs,
                db=db,
            )

    return alert
