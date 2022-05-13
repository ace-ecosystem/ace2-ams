from dataclasses import dataclass
from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeMeta, Session
from sqlalchemy.sql.selectable import Select
from typing import Optional, Union
from uuid import UUID

from db import crud
from db.schemas.alert import AlertHistory
from db.schemas.event import EventHistory
from db.schemas.history import HasHistory
from db.schemas.node import Node
from db.schemas.observable import ObservableHistory
from db.schemas.user import User


@dataclass
class Diff:
    field: str
    old_value: Optional[Union[str, list[str]]] = None
    new_value: Optional[Union[str, list[str]]] = None
    added_to_list: Optional[list[str]] = None
    removed_from_list: Optional[list[str]] = None


def build_read_history_query(history_table: DeclarativeMeta, record_uuid: UUID) -> Select:
    return (
        select(history_table).where(history_table.record_uuid == record_uuid).order_by(history_table.action_time.asc())
    )


def create_diff(
    field: str,
    old: Union[None, str, list[str], datetime, UUID] = None,
    new: Union[None, str, list[str], datetime, UUID] = None,
) -> Diff:
    # Convert datetime objects to UTC strings
    if isinstance(old, datetime):
        old = old.astimezone(timezone.utc).isoformat()
    if isinstance(new, datetime):
        new = new.astimezone(timezone.utc).isoformat()

    # Convert UUID objects to strings
    if isinstance(old, UUID):
        old = str(old)
    if isinstance(new, UUID):
        new = str(new)

    if isinstance(old, list) and isinstance(new, list):
        added = sorted({x for x in new if x not in old})
        removed = sorted({x for x in old if x not in new})
        return Diff(field=field, added_to_list=added, removed_from_list=removed)

    return Diff(field=field, old_value=old, new_value=new, added_to_list=[], removed_from_list=[])


def record_create_history(
    history_table: DeclarativeMeta,
    action_by: User,
    record: Union[Node, User, HasHistory],
    db: Session,
):
    db.add(
        history_table(
            action="CREATE",
            action_by=action_by,
            action_time=crud.helpers.utcnow(),
            record_uuid=record.uuid,
            snapshot=record.history_snapshot,
        )
    )
    db.flush()


def record_node_create_history(
    record_node: Union[Node, HasHistory],
    action_by: User,
    db: Session,
):
    if record_node.node_type == "alert":
        record_create_history(
            history_table=AlertHistory,
            action_by=action_by,
            record=record_node,
            db=db,
        )
    elif record_node.node_type == "event":
        record_create_history(
            history_table=EventHistory,
            action_by=action_by,
            record=record_node,
            db=db,
        )
    elif record_node.node_type == "observable":
        record_create_history(
            history_table=ObservableHistory,
            action_by=action_by,
            record=record_node,
            db=db,
        )


def record_node_update_history(
    record_node: Union[Node, HasHistory],
    action_by: User,
    diffs: list[Diff],
    db: Session,
    action_time: Optional[datetime] = None,
):
    if record_node.node_type == "alert":
        record_update_history(
            history_table=AlertHistory,
            action_by=action_by,
            action_time=action_time,
            record=record_node,
            diffs=diffs,
            db=db,
        )
    elif record_node.node_type == "event":
        record_update_history(
            history_table=EventHistory,
            action_by=action_by,
            action_time=action_time,
            record=record_node,
            diffs=diffs,
            db=db,
        )
    elif record_node.node_type == "observable":
        record_update_history(
            history_table=ObservableHistory,
            action_by=action_by,
            action_time=action_time,
            record=record_node,
            diffs=diffs,
            db=db,
        )


def record_update_history(
    history_table: DeclarativeMeta,
    action_by: User,
    record: Union[Node, User, HasHistory],
    diffs: list[Diff],
    db: Session,
    action_time: Optional[datetime] = None,
):
    if action_time is None:
        action_time = crud.helpers.utcnow()

    for diff in diffs:
        if diff:
            db.add(
                history_table(
                    action="UPDATE",
                    action_by=action_by,
                    action_time=action_time,
                    record_uuid=record.uuid,
                    field=diff.field,
                    diff={
                        "old_value": diff.old_value,
                        "new_value": diff.new_value,
                        "added_to_list": diff.added_to_list,
                        "removed_from_list": diff.removed_from_list,
                    },
                    snapshot=record.history_snapshot,
                )
            )

    db.flush()
