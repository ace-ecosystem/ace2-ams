from sqlalchemy.orm import Session

from api_models.event import EventCreate
from db import crud
from db.schemas.event import Event


def create(model: EventCreate, db: Session) -> Event:
    # Create the new event Node using the data from the request
    obj: Event = crud.node.create(model=model, db_node_type=Event, db=db, exclude={"alert_uuids", "history_username"})

    # Set the various event properties
    obj.prevention_tools = crud.event_prevention_tool.read_by_values(values=model.prevention_tools, db=db)
    obj.owner = crud.user.read_by_username(username=model.owner, db=db)
    obj.queue = crud.queue.read_by_value(value=model.queue, db=db)
    obj.remediations = crud.event_remediation.read_by_values(values=model.remediations, db=db)
    obj.risk_level = crud.event_risk_level.read_by_value(value=model.risk_level, db=db)
    obj.source = crud.event_source.read_by_value(value=model.source, db=db)
    obj.status = crud.event_status.read_by_value(value=model.status, db=db)
    obj.type = crud.event_type.read_by_value(value=model.type, db=db)
    obj.vectors = crud.event_vector.read_by_values(values=model.vectors, db=db)

    db.add(obj)
    db.flush()

    # Add an event history entry if the history username was given.
    if model.history_username:
        crud.history.record_node_create_history(
            record_node=obj,
            action_by=crud.user.read_by_username(username=model.history_username, db=db),
            db=db,
        )

    return obj
