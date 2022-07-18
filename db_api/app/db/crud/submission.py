import json
import time

from datetime import datetime
from api_models.analysis_metadata import AnalysisMetadataRead
from api_models.summaries import URLDomainSummary
from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_, func, not_, or_, select
from sqlalchemy.orm import Session
from sqlalchemy.sql.selectable import Select
from typing import Optional, Union
from uuid import UUID, uuid4

from api_models.analysis import AnalysisSubmissionTreeRead
from api_models.observable import (
    ObservableDispositionHistoryIndividual,
    ObservableMatchingEventIndividual,
    ObservableSubmissionTreeRead,
)
from api_models.submission import (
    SubmissionCreate,
    SubmissionMatchingEventByStatus,
    SubmissionMatchingEventIndividual,
    SubmissionTreeRead,
    SubmissionUpdate,
)
from db import crud
from db.schemas.alert_disposition import AlertDisposition
from db.schemas.analysis import Analysis
from db.schemas.analysis_child_observable_mapping import analysis_child_observable_mapping
from db.schemas.event import Event
from db.schemas.event_status import EventStatus
from db.schemas.metadata_tag import MetadataTag
from db.schemas.observable import Observable
from db.schemas.observable_type import ObservableType
from db.schemas.queue import Queue
from db.schemas.submission import Submission, SubmissionHistory
from db.schemas.submission_analysis_mapping import submission_analysis_mapping
from db.schemas.submission_tool import SubmissionTool
from db.schemas.submission_tool_instance import SubmissionToolInstance
from db.schemas.submission_type import SubmissionType
from db.schemas.user import User
from exceptions.db import VersionMismatch


def _associate_metadata_with_observable(analysis_uuids: list[UUID], o: Observable):
    """Adds the matching analysis metadata from the given analysis UUIDs to the observable."""

    # Set the observable's analysis_metadata property with an empty AnalysisMetadataRead object
    o.analysis_metadata = AnalysisMetadataRead()

    # Loop over each analysis metadata that has ever been added to the observable and only
    # include ones that were added by analyses with a UUID in the given analysis_uuids list.
    for m in o.all_analysis_metadata:
        # Skip this metadata if it is not from one of the given analysis UUIDs
        if m.analysis_uuid not in analysis_uuids:
            continue

        # Add each detection point
        if m.metadata_object.metadata_type == "detection_point":
            o.analysis_metadata.detection_points.append(m.metadata_object)

        # Add each directive metadata
        elif m.metadata_object.metadata_type == "directive":
            o.analysis_metadata.directives.append(m.metadata_object)

        # Only add the display_type metadata if one was not already set
        elif m.metadata_object.metadata_type == "display_type" and not o.analysis_metadata.display_type:
            o.analysis_metadata.display_type = m.metadata_object

        # Only add the display_value metadata if one was not already set
        elif m.metadata_object.metadata_type == "display_value" and not o.analysis_metadata.display_value:
            o.analysis_metadata.display_value = m.metadata_object

        # Only add the sort metadata if one was not already set
        elif m.metadata_object.metadata_type == "sort" and not o.analysis_metadata.sort:
            o.analysis_metadata.sort = m.metadata_object

        # Add each tag metadata
        elif m.metadata_object.metadata_type == "tag":
            o.analysis_metadata.tags.append(m.metadata_object)

        # Only add the time metadata if one was not already set
        elif m.metadata_object.metadata_type == "time" and not o.analysis_metadata.time:
            o.analysis_metadata.time = m.metadata_object

    # Dedup and sort the analysis metadata on the observable that is a list
    o.analysis_metadata.detection_points = sorted(set(o.analysis_metadata.detection_points), key=lambda x: x.value)
    o.analysis_metadata.directives = sorted(set(o.analysis_metadata.directives), key=lambda x: x.value)
    o.analysis_metadata.tags = sorted(set(o.analysis_metadata.tags), key=lambda m: m.value)


def _build_disposition_history(o: Observable):
    """Counts the alert dispositions and adds the disposition history information to the given observable."""

    counts: dict[Optional[AlertDisposition], int] = {}
    for disposition in o.alert_dispositions:
        if disposition not in counts:
            counts[disposition] = 0

        counts[disposition] += 1

    # Sort the dispositions by their rank, where None disposition is at the end of the list
    sorted_dispositions: list[AlertDisposition] = sorted(counts.keys(), key=lambda x: x.rank if x else float("inf"))

    # Loop through the sorted dispositions and build the disposition history objects to add to the observable
    o.disposition_history = []
    for disposition in sorted_dispositions:
        disposition_value = disposition.value if disposition else "OPEN"
        o.disposition_history.append(
            ObservableDispositionHistoryIndividual(
                disposition=disposition_value,
                count=counts[disposition],
                percent=int(counts[disposition] / len(o.alert_dispositions) * 100),
            )
        )


def _build_matching_observable_events(o: Observable):
    """Counts the event statuses and adds the matching event information to the given observable."""

    counts: dict[Optional[EventStatus], int] = {}
    for status in o.event_statuses:
        if status not in counts:
            counts[status] = 0

        counts[status] += 1

    # Sort the statuses by their value
    sorted_statuses: list[EventStatus] = sorted(counts.keys(), key=lambda x: x.value)

    # Loop through the sorted statuses and build the matching event objects to add to the observable
    o.matching_events = [
        ObservableMatchingEventIndividual(
            status=status.value,
            count=counts[status],
        )
        for status in sorted_statuses
    ]


def _build_matching_submission_events(s: Submission):
    """Figures out which events match the given submission based on how many observables they share."""

    # Build a dictionary of the events that contain observables in this submission as well as how
    # many observables are shared between the submission and events.
    counts: dict[Event, int] = {}
    for observable in s.child_observables:
        for event in observable.events:
            if event not in counts:
                counts[event] = 0

            counts[event] += 1

    # Sort the events by their counts (with the highest count first)
    # NOTE: As of Python 3.7, dictionaries will maintain their insertion order:
    # https://mail.python.org/pipermail/python-dev/2017-December/151283.html
    sorted_counts: dict[Event, int] = dict(sorted(counts.items(), key=lambda item: item[1], reverse=True))

    # Build a dictionary to group the matching events by their status
    matching_events_by_status: dict[str, SubmissionMatchingEventByStatus] = {}
    num_submission_observables = len(s.child_observables)
    for item in sorted_counts.items():
        # Create the SubmissionMatchingEventByStatus object if the status hasn't been seen yet
        if item[0].status.value not in matching_events_by_status:
            matching_events_by_status[item[0].status.value] = SubmissionMatchingEventByStatus(
                status=item[0].status.value
            )

        # Add the matching event to its appropriate status group
        matching_events_by_status[item[0].status.value].events.append(
            SubmissionMatchingEventIndividual(
                event=item[0], count=item[1], percent=int(item[1] / num_submission_observables * 100)
            )
        )

    # Set the matching_events property on the submission
    # NOTE: Pydantic does not support list-like elements, so it must explicitly be a list.
    s.matching_events = list(matching_events_by_status.values())


def _read_analysis_uuids(submission_uuids: list[UUID], db: Session) -> list[UUID]:
    """Returns a list of the analysis UUIDs that exist within the given submission UUIDs."""

    return (
        db.execute(
            select(submission_analysis_mapping.c.analysis_uuid).where(
                submission_analysis_mapping.c.submission_uuid.in_(submission_uuids)
            )
        )
        .unique()
        .scalars()
        .all()
    )


def build_read_all_query(
    alert: Optional[bool] = None,
    disposition: Optional[list[str]] = None,
    disposition_user: Optional[list[str]] = None,
    dispositioned_after: Optional[list[datetime]] = None,
    dispositioned_before: Optional[list[datetime]] = None,
    event_uuid: Optional[list[UUID]] = None,
    event_time_after: Optional[list[datetime]] = None,
    event_time_before: Optional[list[datetime]] = None,
    insert_time_after: Optional[list[datetime]] = None,
    insert_time_before: Optional[list[datetime]] = None,
    name: Optional[list[str]] = None,
    not_disposition: Optional[list[str]] = None,
    not_disposition_user: Optional[list[str]] = None,
    not_event_uuid: Optional[list[UUID]] = None,
    not_name: Optional[list[str]] = None,
    not_observable: Optional[list[str]] = None,  # Example: type|value
    not_observable_types: Optional[list[str]] = None,
    not_observable_value: Optional[list[str]] = None,
    not_owner: Optional[list[str]] = None,
    not_queue: Optional[list[str]] = None,
    not_submission_type: Optional[list[str]] = None,
    not_tags: Optional[list[str]] = None,
    not_tool: Optional[list[str]] = None,
    not_tool_instance: Optional[list[str]] = None,
    observable: Optional[list[str]] = None,  # Example: type|value
    observable_types: Optional[list[str]] = None,
    observable_value: Optional[list[str]] = None,
    owner: Optional[list[str]] = None,
    queue: Optional[list[str]] = None,
    sort: Optional[str] = None,  # Example: event_time|desc
    submission_type: Optional[list[str]] = None,
    tags: Optional[list[str]] = None,
    tool: Optional[list[str]] = None,
    tool_instance: Optional[list[str]] = None,
) -> Select:
    def _join_as_subquery(query: Select, subquery: Select):
        s = subquery.subquery()
        return query.join(s, Submission.uuid == s.c.uuid).group_by(Submission.uuid)

    def _none_in_list(values: list):
        return "none" in [str(v).lower() for v in values]

    def _non_none_values(values: list) -> list:
        return [v for v in values if str(v).lower() != "none"]

    query = select(Submission)

    if alert:
        alert_query = select(Submission).where(Submission.alert == True)

        query = _join_as_subquery(query, alert_query)

    if disposition:
        disposition_query = select(Submission)
        if _none_in_list(disposition):
            values = _non_none_values(disposition)
            if values:
                disposition_query = disposition_query.outerjoin(AlertDisposition).where(
                    or_(AlertDisposition.value.in_(values), Submission.disposition_uuid == None)
                )
            else:
                disposition_query = disposition_query.where(Submission.disposition_uuid == None)
        else:
            disposition_query = disposition_query.join(AlertDisposition).where(AlertDisposition.value.in_(disposition))

        query = _join_as_subquery(query, disposition_query)

    if disposition_user:
        disposition_user_query = select(Submission)
        if _none_in_list(disposition_user):
            values = _non_none_values(disposition_user)
            if values:
                disposition_user_query = disposition_user_query.where(
                    or_(
                        Submission.disposition_user_uuid == None,
                        Submission.history.any(
                            and_(
                                SubmissionHistory.field == "disposition",
                                SubmissionHistory.action_by.has(User.username.in_(values)),
                            )
                        ),
                    )
                )
            else:
                disposition_user_query = disposition_user_query.where(Submission.disposition_user_uuid == None)
        else:
            disposition_user_query = disposition_user_query.where(
                Submission.history.any(
                    and_(
                        SubmissionHistory.field == "disposition",
                        SubmissionHistory.action_by.has(User.username.in_(disposition_user)),
                    )
                ),
            )

        query = _join_as_subquery(query, disposition_user_query)

    if dispositioned_after:
        dispositioned_after_query = select(Submission).where(
            Submission.history.any(
                and_(
                    SubmissionHistory.field == "disposition",
                    or_(SubmissionHistory.action_time > d for d in dispositioned_after),
                )
            )
        )
        query = _join_as_subquery(query, dispositioned_after_query)

    if dispositioned_before:
        dispositioned_before_query = select(Submission).where(
            Submission.history.any(
                and_(
                    SubmissionHistory.field == "disposition",
                    or_(SubmissionHistory.action_time < d for d in dispositioned_before),
                )
            )
        )
        query = _join_as_subquery(query, dispositioned_before_query)

    if event_time_after:
        event_time_after_query = select(Submission).where(or_(Submission.event_time > e for e in event_time_after))
        query = _join_as_subquery(query, event_time_after_query)

    if event_time_before:
        event_time_before_query = select(Submission).where(or_(Submission.event_time < e for e in event_time_before))
        query = _join_as_subquery(query, event_time_before_query)

    if event_uuid:
        event_uuid_query = select(Submission)
        if _none_in_list(event_uuid):
            values = _non_none_values(event_uuid)
            if values:
                event_uuid_query = event_uuid_query.where(
                    or_(Submission.event_uuid.in_(values), Submission.event_uuid == None)
                )
            else:
                event_uuid_query = event_uuid_query.where(Submission.event_uuid == None)
        else:
            event_uuid_query = event_uuid_query.where(Submission.event_uuid.in_(event_uuid))

        query = _join_as_subquery(query, event_uuid_query)

    if insert_time_after:
        insert_time_after_query = select(Submission).where(or_(Submission.insert_time > i for i in insert_time_after))
        query = _join_as_subquery(query, insert_time_after_query)

    if insert_time_before:
        insert_time_before_query = select(Submission).where(or_(Submission.insert_time < i for i in insert_time_before))
        query = _join_as_subquery(query, insert_time_before_query)

    if name:
        clauses = [Submission.name.ilike(f"%{n}%") for n in name]
        name_query = select(Submission).where(or_(*clauses))
        query = _join_as_subquery(query, name_query).order_by(Submission.name.asc())

    if not_disposition:
        not_disposition_query = select(Submission)
        if _none_in_list(not_disposition):
            values = _non_none_values(not_disposition)
            if values:
                not_disposition_query = not_disposition_query.join(AlertDisposition).where(
                    ~AlertDisposition.value.in_(values)
                )
            else:
                not_disposition_query = not_disposition_query.where(Submission.disposition_uuid != None)
        else:
            not_disposition_query = not_disposition_query.outerjoin(AlertDisposition).where(
                or_(~AlertDisposition.value.in_(not_disposition), Submission.disposition_uuid == None)
            )

        query = _join_as_subquery(query, not_disposition_query)

    if not_disposition_user:
        disposition_user_query = select(Submission)
        if _none_in_list(not_disposition_user):
            values = _non_none_values(not_disposition_user)
            if values:
                disposition_user_query = disposition_user_query.where(
                    and_(
                        Submission.disposition_user_uuid != None,
                        ~Submission.history.any(
                            and_(
                                SubmissionHistory.field == "disposition",
                                SubmissionHistory.action_by.has(User.username.in_(values)),
                            )
                        ),
                    )
                )
            else:
                disposition_user_query = disposition_user_query.where(Submission.disposition_user_uuid != None)
        else:
            disposition_user_query = disposition_user_query.where(
                or_(
                    Submission.disposition_uuid == None,
                    ~Submission.history.any(
                        and_(
                            SubmissionHistory.field == "disposition",
                            SubmissionHistory.action_by.has(User.username.in_(not_disposition_user)),
                        )
                    ),
                )
            )

        query = _join_as_subquery(query, disposition_user_query)

    if not_event_uuid:
        event_uuid_query = select(Submission)
        if _none_in_list(not_event_uuid):
            values = _non_none_values(not_event_uuid)
            if values:
                event_uuid_query = event_uuid_query.where(
                    and_(~Submission.event_uuid.in_(values), Submission.event_uuid != None)
                )
            else:
                event_uuid_query = event_uuid_query.where(Submission.event_uuid != None)
        else:
            event_uuid_query = event_uuid_query.where(
                or_(Submission.event_uuid == None, ~Submission.event_uuid.in_(not_event_uuid))
            )

        query = _join_as_subquery(query, event_uuid_query)

    if not_name:
        clauses = [~Submission.name.ilike(f"%{n}%") for n in not_name]
        not_name_query = select(Submission).where(and_(*clauses))
        query = _join_as_subquery(query, not_name_query).order_by(Submission.name.asc())

    if not_observable:
        observable_split = [o.split("|", maxsplit=1) for o in not_observable]
        observable_query = (
            select(Submission)
            .join(
                submission_analysis_mapping,
                onclause=submission_analysis_mapping.c.submission_uuid == Submission.uuid,
            )
            .join(
                analysis_child_observable_mapping,
                onclause=analysis_child_observable_mapping.c.analysis_uuid
                == submission_analysis_mapping.c.analysis_uuid,
            )
            .join(Observable, onclause=Observable.uuid == analysis_child_observable_mapping.c.observable_uuid)
            .join(ObservableType)
            .where(not_(or_(and_(ObservableType.value == o[0], Observable.value == o[1]) for o in observable_split)))
        )

        query = _join_as_subquery(query, observable_query)

    if not_observable_types:
        type_filters = []
        for o in not_observable_types:
            type_filters.append([func.count(1).filter(ObservableType.value == t) > 0 for t in o.split(",")])

        observable_types_query = (
            select(Submission)
            .join(
                submission_analysis_mapping, onclause=submission_analysis_mapping.c.submission_uuid == Submission.uuid
            )
            .join(
                analysis_child_observable_mapping,
                onclause=analysis_child_observable_mapping.c.analysis_uuid
                == submission_analysis_mapping.c.analysis_uuid,
            )
            .join(Observable, onclause=Observable.uuid == analysis_child_observable_mapping.c.observable_uuid)
            .join(ObservableType)
            .having(not_(or_(and_(*sub_type_filters) for sub_type_filters in type_filters)))
            .group_by(Submission.uuid)
        )

        query = _join_as_subquery(query, observable_types_query)

    if not_observable_value:
        observable_value_query = (
            select(Submission)
            .join(
                submission_analysis_mapping,
                onclause=submission_analysis_mapping.c.submission_uuid == Submission.uuid,
            )
            .join(
                analysis_child_observable_mapping,
                onclause=analysis_child_observable_mapping.c.analysis_uuid
                == submission_analysis_mapping.c.analysis_uuid,
            )
            .join(Observable, onclause=Observable.uuid == analysis_child_observable_mapping.c.observable_uuid)
            .where(~Observable.value.in_(not_observable_value))
        )

        query = _join_as_subquery(query, observable_value_query)

    if not_owner:
        owner_query = select(Submission)
        if _none_in_list(not_owner):
            values = _non_none_values(not_owner)
            if values:
                owner_query = owner_query.outerjoin(User, onclause=Submission.owner_uuid == User.uuid).where(
                    and_(Submission.owner_uuid != None, ~User.username.in_(values))
                )
            else:
                owner_query = owner_query.where(Submission.owner_uuid != None)
        else:
            owner_query = owner_query.outerjoin(User, onclause=Submission.owner_uuid == User.uuid).where(
                or_(~User.username.in_(not_owner), Submission.owner_uuid == None)
            )
        query = _join_as_subquery(query, owner_query)

    if not_queue:
        queue_query = select(Submission).join(Queue).where(~Queue.value.in_(not_queue))
        query = _join_as_subquery(query, queue_query)

    if not_submission_type:
        type_query = select(Submission).join(SubmissionType).where(~SubmissionType.value.in_(not_submission_type))
        query = _join_as_subquery(query, type_query)

    if not_tags:
        tag_filters = []
        for t in not_tags:
            if t:
                tag_sub_filters = []
                for tag in t.split(","):
                    tag_sub_filters.append(
                        and_(
                            ~Submission.tags.any(MetadataTag.value == tag),
                            ~Submission.child_analysis_tags.any(MetadataTag.value == tag),
                            ~Submission.child_tags.any(MetadataTag.value == tag),
                        )
                    )

                tag_filters.append(or_(*tag_sub_filters))

        tags_query = select(Submission).where(and_(*tag_filters))

        query = _join_as_subquery(query, tags_query)

    if not_tool:
        not_tool_query = select(Submission)
        if _none_in_list(not_tool):
            values = _non_none_values(not_tool)
            if values:
                not_tool_query = not_tool_query.join(SubmissionTool).where(~SubmissionTool.value.in_(values))
            else:
                not_tool_query = not_tool_query.where(Submission.tool_uuid != None)
        else:
            not_tool_query = not_tool_query.outerjoin(SubmissionTool).where(
                or_(~SubmissionTool.value.in_(not_tool), Submission.tool_uuid == None)
            )

        query = _join_as_subquery(query, not_tool_query)

    if not_tool_instance:
        not_tool_instance_query = select(Submission)
        if _none_in_list(not_tool_instance):
            values = _non_none_values(not_tool_instance)
            if values:
                not_tool_instance_query = not_tool_instance_query.join(SubmissionToolInstance).where(
                    ~SubmissionToolInstance.value.in_(values)
                )
            else:
                not_tool_instance_query = not_tool_instance_query.where(Submission.tool_instance_uuid != None)
        else:
            not_tool_instance_query = not_tool_instance_query.outerjoin(SubmissionToolInstance).where(
                or_(~SubmissionToolInstance.value.in_(not_tool_instance), Submission.tool_instance_uuid == None)
            )

        query = _join_as_subquery(query, not_tool_instance_query)

    if observable:
        observable_split = [o.split("|", maxsplit=1) for o in observable]
        observable_query = (
            select(Submission)
            .join(
                submission_analysis_mapping,
                onclause=submission_analysis_mapping.c.submission_uuid == Submission.uuid,
            )
            .join(
                analysis_child_observable_mapping,
                onclause=analysis_child_observable_mapping.c.analysis_uuid
                == submission_analysis_mapping.c.analysis_uuid,
            )
            .join(Observable, onclause=Observable.uuid == analysis_child_observable_mapping.c.observable_uuid)
            .join(ObservableType)
            .where(or_(and_(ObservableType.value == o[0], Observable.value == o[1]) for o in observable_split))
        )

        query = _join_as_subquery(query, observable_query)

    if observable_types:
        type_filters = []
        for o in observable_types:
            type_filters.append([func.count(1).filter(ObservableType.value == t) > 0 for t in o.split(",")])

        observable_types_query = (
            select(Submission)
            .join(
                submission_analysis_mapping, onclause=submission_analysis_mapping.c.submission_uuid == Submission.uuid
            )
            .join(
                analysis_child_observable_mapping,
                onclause=analysis_child_observable_mapping.c.analysis_uuid
                == submission_analysis_mapping.c.analysis_uuid,
            )
            .join(Observable, onclause=Observable.uuid == analysis_child_observable_mapping.c.observable_uuid)
            .join(ObservableType)
            .having(or_(and_(*sub_type_filters) for sub_type_filters in type_filters))
            .group_by(Submission.uuid)
        )

        query = _join_as_subquery(query, observable_types_query)

    if observable_value:
        observable_value_query = (
            select(Submission)
            .join(
                submission_analysis_mapping,
                onclause=submission_analysis_mapping.c.submission_uuid == Submission.uuid,
            )
            .join(
                analysis_child_observable_mapping,
                onclause=analysis_child_observable_mapping.c.analysis_uuid
                == submission_analysis_mapping.c.analysis_uuid,
            )
            .join(Observable, onclause=Observable.uuid == analysis_child_observable_mapping.c.observable_uuid)
            .where(Observable.value.in_(observable_value))
        )

        query = _join_as_subquery(query, observable_value_query)

    if owner:
        owner_query = select(Submission)
        if _none_in_list(owner):
            values = _non_none_values(owner)
            if values:
                owner_query = owner_query.outerjoin(User, onclause=Submission.owner_uuid == User.uuid).where(
                    or_(User.username.in_(values), Submission.owner_uuid == None)
                )
            else:
                owner_query = owner_query.where(Submission.owner_uuid == None)
        else:
            owner_query = owner_query.join(User, onclause=Submission.owner_uuid == User.uuid).where(
                User.username.in_(owner)
            )
        query = _join_as_subquery(query, owner_query)

    if queue:
        queue_query = select(Submission).join(Queue).where(Queue.value.in_(queue))
        query = _join_as_subquery(query, queue_query)

    if submission_type:
        type_query = select(Submission).join(SubmissionType).where(SubmissionType.value.in_(submission_type))
        query = _join_as_subquery(query, type_query)

    if tags:
        tag_filters = []
        for t in tags:
            if t:
                tag_sub_filters = []
                for tag in t.split(","):
                    tag_sub_filters.append(
                        or_(
                            Submission.tags.any(MetadataTag.value == tag),
                            Submission.child_analysis_tags.any(MetadataTag.value == tag),
                            Submission.child_tags.any(MetadataTag.value == tag),
                        )
                    )

                tag_filters.append(and_(*tag_sub_filters))

        tags_query = select(Submission).where(or_(*tag_filters))

        query = _join_as_subquery(query, tags_query)

    if tool:
        tool_query = select(Submission)
        if _none_in_list(tool):
            values = _non_none_values(tool)
            if values:
                tool_query = tool_query.outerjoin(SubmissionTool).where(
                    or_(SubmissionTool.value.in_(values), Submission.tool_uuid == None)
                )
            else:
                tool_query = tool_query.where(Submission.tool_uuid == None)
        else:
            tool_query = tool_query.join(SubmissionTool).where(SubmissionTool.value.in_(tool))

        query = _join_as_subquery(query, tool_query)

    if tool_instance:
        tool_instance_query = select(Submission)
        if _none_in_list(tool_instance):
            values = _non_none_values(tool_instance)
            if values:
                tool_instance_query = tool_instance_query.outerjoin(SubmissionToolInstance).where(
                    or_(SubmissionToolInstance.value.in_(values), Submission.tool_instance_uuid == None)
                )
            else:
                tool_instance_query = tool_instance_query.where(Submission.tool_instance_uuid == None)
        else:
            tool_instance_query = tool_instance_query.join(SubmissionToolInstance).where(
                SubmissionToolInstance.value.in_(tool_instance)
            )

        query = _join_as_subquery(query, tool_instance_query)

    if sort:
        sort_split = sort.split("|")
        sort_by = sort_split[0]
        order = sort_split[1]

        # Only sort by disposition if we are not also filtering by disposition
        if sort_by.lower() == "disposition" and not disposition:
            if order == "asc":
                query = query.outerjoin(AlertDisposition).order_by(AlertDisposition.value.asc())
            else:
                query = query.outerjoin(AlertDisposition).order_by(AlertDisposition.value.desc())

        elif sort_by.lower() == "disposition_time":
            if order == "asc":
                query = query.order_by(Submission.disposition_time.asc())
            else:
                query = query.order_by(Submission.disposition_time.desc())

        # Only sort by disposition_user if we are not also filtering by disposition_user
        elif sort_by.lower() == "disposition_user" and not disposition_user:
            query = query.outerjoin(User, onclause=Submission.disposition_user_uuid == User.uuid).group_by(
                Submission.uuid, User.username
            )
            if order == "asc":
                query = query.order_by(User.username.asc())
            else:
                query = query.order_by(User.username.desc())

        elif sort_by.lower() == "event_time":
            if order == "asc":
                query = query.order_by(Submission.event_time.asc())
            else:
                query = query.order_by(Submission.event_time.desc())

        elif sort_by.lower() == "insert_time":
            if order == "asc":
                query = query.order_by(Submission.insert_time.asc())
            else:
                query = query.order_by(Submission.insert_time.desc())

        elif sort_by.lower() == "name":
            if order == "asc":
                query = query.order_by(Submission.name.asc())
            else:
                query = query.order_by(Submission.name.desc())

        # Only sort by owner if we are not also filtering by owner
        elif sort_by.lower() == "owner" and not owner:
            query = query.outerjoin(User, onclause=Submission.owner_uuid == User.uuid).group_by(
                Submission.uuid, User.username
            )
            if order == "asc":
                query = query.order_by(User.username.asc())
            else:
                query = query.order_by(User.username.desc())

        # Only sort by queue if we are not also filtering by queue
        elif sort_by.lower() == "queue" and not queue:
            if order == "asc":
                query = query.join(Queue).order_by(Queue.value.asc())
            else:
                query = query.join(Queue).order_by(Queue.value.desc())

        # Only sort by submission type if we are not also filtering by submission type
        elif sort_by.lower() == "submission_type" and not submission_type:
            if order == "asc":
                query = query.join(SubmissionType).order_by(SubmissionType.value.asc())
            else:
                query = query.join(SubmissionType).order_by(SubmissionType.value.desc())

    return query


def create_or_read(model: SubmissionCreate, db: Session) -> Submission:
    # Create the new submission using the data from the request
    obj = Submission(**model.dict(exclude={"details", "history_username", "observables"}))

    # Set the various submission properties
    obj.alert = model.alert
    obj.description = model.description
    obj.event_time = model.event_time
    obj.insert_time = model.insert_time
    obj.instructions = model.instructions
    obj.name = model.name
    if model.owner:
        obj.owner = crud.user.read_by_username(username=model.owner, db=db)
        obj.ownership_time = crud.helpers.utcnow()
    obj.queue = crud.queue.read_by_value(value=model.queue, db=db)
    obj.root_analysis = crud.analysis.create_root(details=model.details, db=db)
    obj.tags = crud.metadata_tag.read_by_values(values=model.tags, db=db)
    if model.tool:
        obj.tool = crud.submission_tool.read_by_value(value=model.tool, db=db)
    if model.tool_instance:
        obj.tool_instance = crud.submission_tool_instance.read_by_value(value=model.tool_instance, db=db)
    obj.type = crud.submission_type.read_by_value(value=model.type, db=db)
    obj.uuid = model.uuid

    # If the submission could not be created, that implies that one already exists with the given UUID.
    # This is really only going to happen during testing when sometimes we add a submission with a predefined UUID.
    if not crud.helpers.create(obj=obj, db=db):
        return read_by_uuid(uuid=model.uuid, db=db)

    # Associate the root analysis with the submission
    crud.submission_analysis_mapping.create(analysis_uuid=obj.root_analysis_uuid, submission_uuid=obj.uuid, db=db)

    # Create any child observables
    for observable in model.observables:
        crud.observable.create_or_read(model=observable, parent_analysis=obj.root_analysis, db=db)

    # Add a submission history entry if the history username was given. This would typically only be
    # supplied by the GUI when an analyst creates a manual alert.
    if model.history_username is not None:
        crud.history.record_create_history(
            history_table=SubmissionHistory,
            action_by=crud.user.read_by_username(username=model.history_username, db=db),
            record=obj,
            db=db,
        )

    db.flush()
    return obj


def read_all(
    db: Session,
    alert: Optional[bool] = None,
    disposition: Optional[list[str]] = None,
    disposition_user: Optional[list[str]] = None,
    dispositioned_after: Optional[list[datetime]] = None,
    dispositioned_before: Optional[list[datetime]] = None,
    event_uuid: Optional[list[UUID]] = None,
    event_time_after: Optional[list[datetime]] = None,
    event_time_before: Optional[list[datetime]] = None,
    insert_time_after: Optional[list[datetime]] = None,
    insert_time_before: Optional[list[datetime]] = None,
    name: Optional[list[str]] = None,
    not_disposition: Optional[list[str]] = None,
    not_disposition_user: Optional[list[str]] = None,
    not_event_uuid: Optional[list[UUID]] = None,
    not_name: Optional[list[str]] = None,
    not_observable: Optional[list[str]] = None,  # Example: type|value
    not_observable_types: Optional[list[str]] = None,
    not_observable_value: Optional[list[str]] = None,
    not_owner: Optional[list[str]] = None,
    not_queue: Optional[list[str]] = None,
    not_submission_type: Optional[list[str]] = None,
    not_tags: Optional[list[str]] = None,
    not_tool: Optional[list[str]] = None,
    not_tool_instance: Optional[list[str]] = None,
    observable: Optional[list[str]] = None,  # Example: type|value
    observable_types: Optional[list[str]] = None,
    observable_value: Optional[list[str]] = None,
    owner: Optional[list[str]] = None,
    queue: Optional[list[str]] = None,
    sort: Optional[str] = None,  # Example: event_time|desc
    submission_type: Optional[list[str]] = None,
    tags: Optional[list[str]] = None,
    tool: Optional[list[str]] = None,
    tool_instance: Optional[list[str]] = None,
) -> list[Submission]:
    return (
        db.execute(
            build_read_all_query(
                alert=alert,
                disposition=disposition,
                disposition_user=disposition_user,
                dispositioned_after=dispositioned_after,
                dispositioned_before=dispositioned_before,
                event_uuid=event_uuid,
                event_time_after=event_time_after,
                event_time_before=event_time_before,
                insert_time_after=insert_time_after,
                insert_time_before=insert_time_before,
                name=name,
                not_disposition=not_disposition,
                not_disposition_user=not_disposition_user,
                not_event_uuid=not_event_uuid,
                not_name=not_name,
                not_observable=not_observable,  # Example: type|value
                not_observable_types=not_observable_types,
                not_observable_value=not_observable_value,
                not_owner=not_owner,
                not_queue=not_queue,
                not_submission_type=not_submission_type,
                not_tags=not_tags,
                not_tool=not_tool,
                not_tool_instance=not_tool_instance,
                observable=observable,  # Example: type|value
                observable_types=observable_types,
                observable_value=observable_value,
                owner=owner,
                queue=queue,
                sort=sort,  # Example: event_time|desc
                submission_type=submission_type,
                tags=tags,
                tool=tool,
                tool_instance=tool_instance,
            )
        )
        .scalars()
        .all()
    )


def read_all_history(uuid: UUID, db: Session) -> list[SubmissionHistory]:
    return (
        db.execute(crud.history.build_read_history_query(history_table=SubmissionHistory, record_uuid=uuid))
        .scalars()
        .all()
    )


def read_by_uuid(uuid: UUID, db: Session) -> Submission:
    return crud.helpers.read_by_uuid(db_table=Submission, uuid=uuid, db=db)


def read_observables(uuids: list[UUID], db: Session) -> list[Observable]:
    """Returns a list of the unique observables contained within the given submission UUIDs."""

    # Get a list of all the observables contained within the given submission UUIDs
    query = (
        select(Observable)
        .join(
            analysis_child_observable_mapping,
            onclause=analysis_child_observable_mapping.c.observable_uuid == Observable.uuid,
        )
        .join(
            submission_analysis_mapping,
            onclause=and_(
                submission_analysis_mapping.c.submission_uuid.in_(uuids),
                submission_analysis_mapping.c.analysis_uuid == analysis_child_observable_mapping.c.analysis_uuid,
            ),
        )
        .join(ObservableType, onclause=ObservableType.uuid == Observable.type_uuid)
        .order_by(ObservableType.value.asc(), Observable.value.asc())
    )
    observables: list[Observable] = db.execute(query).unique().scalars().all()

    # Associate the analysis metadata with the observables
    analysis_uuids = _read_analysis_uuids(submission_uuids=uuids, db=db)
    for observable in observables:
        _associate_metadata_with_observable(analysis_uuids=analysis_uuids, o=observable)
        _build_disposition_history(o=observable)
        _build_matching_observable_events(o=observable)

    return observables


def read_tree(uuid: UUID, db: Session) -> SubmissionTreeRead:
    """
    This function reads a submission from the database and constructs its nested tree structure.

    When the submission dattabase object is obtained, it contains flat lists of analyses and observables that
    make up the submission.

    Using the following circular alert as an example:

        RootAnalysis
            O1
                A1
                    O2
                        A2
                            O1 <-- cut off the loop here

    These lists would look like:

    submission.analyses = [RootAnalysis, A1, A2]
    submission.child_observables = [O1, O2]

    Each analysis object knows its target (parent) observable as well as any child observables it produced. Using
    this information, we can construct the nested structure shown above from these two flat lists.

    The general idea is to first produce individual instances of the observables contained in the submission. As shown
    above, the flat list of child_observables only has two objects, but the nested tree structure contains O1 twice.

    Once the observable instances are created, we can begin associating the analysis/observable objects with their
    children. Beginning with the analysis objects, their child observable instances are added as children. That would
    produce a result such as:

        RootAnalysis
            O1

        A1
            O2

        A2
            O1

    Next, the analysis objects must be added as children to their target (parent) observable instances. However, to
    avoid an infinite loop, analyses are only added as children to an observable if the observable is the first of its
    kind in the tree. Using the example above, this means that only the first instance of O1 will have child analyses.
    This is the step that produces the final nested tree structure.
    """

    # Read the submission from the database
    db_submission = read_by_uuid(uuid=uuid, db=db)

    # Build the matching events information and add it to the Submission object
    _build_matching_submission_events(s=db_submission)

    # Set the number_of_observables property on the Submission database object. This is not done automatically
    # by the Submission SQLAlchemy class because the child_observables relationship is lazy-loaded.
    db_submission.number_of_observables = len(db_submission.child_observables)

    # Associate metadata and other alert-specific information with the observable database objects
    for db_observable in db_submission.child_observables:
        _associate_metadata_with_observable(analysis_uuids=db_submission.analysis_uuids, o=db_observable)
        _build_disposition_history(o=db_observable)
        _build_matching_observable_events(o=db_observable)

    # Build lookup dictionaries of the analyses that are used to more efficiently build the nested tree structure.
    analysis_instances: dict[UUID, AnalysisSubmissionTreeRead] = {
        a.uuid: a.convert_to_pydantic() for a in db_submission.analyses
    }
    db_analyses_by_uuid: dict[UUID, Analysis] = {a.uuid: a for a in db_submission.analyses}
    db_analyses_by_target_uuid: dict[UUID, list[Analysis]] = {}
    for db_analysis in db_submission.analyses:
        if db_analysis.target_uuid not in db_analyses_by_target_uuid:
            db_analyses_by_target_uuid[db_analysis.target_uuid] = []
        db_analyses_by_target_uuid[db_analysis.target_uuid].append(db_analysis)

    # Iterate through all of the analysis and observable objects in the submission to build the individual
    # observable instances used to construct the tree. The analysis and observable objects are iterated in reverse
    # order so that the end result of the tree structure is correct.
    observable_instances: dict[UUID, list[ObservableSubmissionTreeRead]] = {}
    unvisited: list[Union[Analysis, Observable]] = [db_submission.root_analysis]
    while unvisited:
        current = unvisited.pop(0)

        # If the current object is Analysis, just add each of its child observables to the unvisited list.
        if isinstance(current, Analysis):
            for idx in range(len(current.child_observables) - 1, -1, -1):
                unvisited.insert(0, current.child_observables[idx])

        # If the current object is Observable, only add its child analyses to the unvisited list if we have not
        # already seen this observable. Otherwise, add a "jump to" reference to the observable so that the GUI
        # can show a link that will take you to the place in the tree where the analysis exists. This is what cuts
        # off circular tree references.
        elif isinstance(current, Observable):
            instance = current.convert_to_pydantic()

            if current.uuid not in observable_instances:
                observable_instances[current.uuid] = []

                children = db_analyses_by_target_uuid.get(current.uuid, [])
                for idx in range(len(children) - 1, -1, -1):
                    unvisited.insert(0, children[idx])
            else:
                # Since this is a duplicate observable, add its "jump to" link so that the GUI can transport you
                # to the observable instance in the tree that actually contains the analysis.
                instance.jump_to_uuid = observable_instances[current.uuid][0].tree_uuid

            observable_instances[current.uuid].append(instance)

    # Associate the analyses with their child observable instances. Because an observable may appear multiple times
    # in the tree, a dictionary is used to keep track of which instance of the observable needs to be added as a child
    # to the analysis.
    observable_indices: dict[UUID, int] = {}
    for analysis_uuid in analysis_instances:
        for db_child_observable in db_analyses_by_uuid[analysis_uuid].child_observables:
            if db_child_observable.uuid not in observable_indices:
                observable_indices[db_child_observable.uuid] = 0

            analysis_instances[analysis_uuid].children.append(
                observable_instances[db_child_observable.uuid][observable_indices[db_child_observable.uuid]],
            )
            observable_indices[db_child_observable.uuid] += 1

        # Sort each analysis instance's child observables according to their sort metadata (if they have any). If
        # they do not have any sort metadata, then "infinity" will be used.
        analysis_instances[analysis_uuid].children.sort(
            key=lambda x: x.analysis_metadata.sort.value if x.analysis_metadata.sort else float("inf")
        )

    # Add each observable's child analyses, but only to the first instance of each observable. This is to cut off
    # any circular references. The GUI will use a "jump to analysis" link under each repeated observable in the tree.
    for observable_uuid in observable_instances:
        if observable_uuid in db_analyses_by_target_uuid:
            for db_analysis in db_analyses_by_target_uuid[observable_uuid]:
                observable_instances[observable_uuid][0].children.append(analysis_instances[db_analysis.uuid])

    # Create the SubmissionTree object and set its root analysis.
    tree = db_submission.convert_to_pydantic()
    tree.root_analysis = analysis_instances[db_submission.root_analysis_uuid]
    return tree


def read_summary_url_domain(uuid: UUID, db: Session) -> URLDomainSummary:
    # Verify the submission exists
    read_by_uuid(uuid=uuid, db=db)

    observables = read_observables(uuids=[uuid], db=db)
    urls = [observable for observable in observables if observable.type.value == "url"]

    return crud.helpers.read_summary_url_domain(url_observables=urls)


def update(model: SubmissionUpdate, db: Session):
    # Read the current submission
    submission = read_by_uuid(uuid=model.uuid, db=db)

    # Capture all of the diffs that were made (for adding to the history tables)
    diffs: list[crud.history.Diff] = []

    # Get the data that was given in the request and use it to update the database object
    update_data = model.dict(exclude_unset=True)

    # Return an exception if the passed in version does not match the submission's current version
    if "version" in update_data and update_data["version"] != submission.version:
        raise VersionMismatch(
            f"Submission version {update_data['version']} does not match the database version {submission.version}"
        )

    # Update the current version
    submission.version = uuid4()

    if "description" in update_data:
        diffs.append(
            crud.history.create_diff(field="description", old=submission.description, new=update_data["description"])
        )
        submission.description = update_data["description"]

    if "disposition" in update_data and model.history_username:
        old_value = submission.disposition.value if submission.disposition else None
        diffs.append(crud.history.create_diff(field="disposition", old=old_value, new=update_data["disposition"]))
        if update_data["disposition"]:
            submission.disposition = crud.alert_disposition.read_by_value(value=update_data["disposition"], db=db)
            submission.disposition_time = crud.helpers.utcnow()
            submission.disposition_user = crud.user.read_by_username(username=model.history_username, db=db)
        else:
            submission.disposition = None

    if "event_uuid" in update_data:
        diffs.append(
            crud.history.create_diff(field="event_uuid", old=submission.event_uuid, new=update_data["event_uuid"])
        )
        if update_data["event_uuid"]:
            submission.event = crud.event.read_by_uuid(uuid=update_data["event_uuid"], db=db)

            # This counts as editing the event, so it should receive a new version.
            submission.event.version = uuid4()
        else:
            submission.event = None

    if "event_time" in update_data:
        diffs.append(
            crud.history.create_diff(field="event_time", old=submission.event_time, new=update_data["event_time"])
        )
        submission.event_time = update_data["event_time"]

    if "instructions" in update_data:
        diffs.append(
            crud.history.create_diff(field="instructions", old=submission.instructions, new=update_data["instructions"])
        )
        submission.instructions = update_data["instructions"]

    if "owner" in update_data:
        old_value = submission.owner.username if submission.owner else None
        diffs.append(crud.history.create_diff(field="owner", old=old_value, new=update_data["owner"]))
        if update_data["owner"]:
            submission.owner = crud.user.read_by_username(username=update_data["owner"], db=db)
            submission.ownership_time = crud.helpers.utcnow()
        else:
            submission.owner = None

    if "queue" in update_data:
        diffs.append(crud.history.create_diff(field="queue", old=submission.queue.value, new=update_data["queue"]))
        submission.queue = crud.queue.read_by_value(value=update_data["queue"], db=db)

    if "tags" in update_data:
        diffs.append(
            crud.history.create_diff(
                field="tags",
                old=[x.value for x in submission.tags],
                new=update_data["tags"],
            )
        )

        if update_data["tags"]:
            submission.tags = crud.metadata_tag.read_by_values(values=update_data["tags"], db=db)
        else:
            submission.tags = []

    db.flush()

    # Add a submission history entry if the history username was given. This would typically only be
    # supplied by the GUI when an analyst updates an alert.
    if model.history_username is not None:
        crud.history.record_update_history(
            history_table=SubmissionHistory,
            action_by=crud.user.read_by_username(username=model.history_username, db=db),
            record=submission,
            diffs=diffs,
            db=db,
        )


def update_submission_versions(analysis_uuid: UUID, db: Session):
    """Updates the version of any submission in the database that contains the given analysis UUID."""

    # Query the database for every submission that contains this analysis
    query = select(Submission).join(
        submission_analysis_mapping,
        onclause=and_(
            submission_analysis_mapping.c.submission_uuid == Submission.uuid,
            submission_analysis_mapping.c.analysis_uuid == analysis_uuid,
        ),
    )

    submissions: list[Submission] = db.execute(query).unique().scalars().all()

    # Update each submission's version
    for submission in submissions:
        submission.version = uuid4()

    db.flush()
