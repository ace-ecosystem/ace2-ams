from datetime import datetime
from datetime import datetime
from deepdiff import DeepHash
from sqlalchemy import and_, func, or_, select
from sqlalchemy.orm import Load, Session
from sqlalchemy.sql.selectable import Select
from typing import Optional
from urllib.parse import urlparse
from uuid import UUID
from api_models.analysis_details import FAQueueAnalysisDetails, SandboxProcess

from api_models.event import EventCreate, EventUpdate
from api_models.event_summaries import (
    DetectionSummary,
    EmailHeadersBody,
    EmailSummary,
    ObservableSummary,
    SandboxSummary,
    UserSummary,
)
from api_models.summaries import URLDomainSummary
from db import crud
from db.schemas.alert_disposition import AlertDisposition
from db.schemas.analysis import Analysis
from db.schemas.analysis_child_observable_mapping import analysis_child_observable_mapping
from db.schemas.analysis_module_type import AnalysisModuleType
from db.schemas.event import Event, EventHistory
from db.schemas.event_prevention_tool import EventPreventionTool
from db.schemas.event_remediation import EventRemediation
from db.schemas.event_risk_level import EventRiskLevel
from db.schemas.event_source import EventSource
from db.schemas.event_status import EventStatus
from db.schemas.event_type import EventType
from db.schemas.event_vector import EventVector
from db.schemas.node import Node
from db.schemas.node_detection_point import NodeDetectionPoint
from db.schemas.node_tag import NodeTag
from db.schemas.node_threat import NodeThreat
from db.schemas.node_threat_actor import NodeThreatActor
from db.schemas.observable import Observable
from db.schemas.observable_type import ObservableType
from db.schemas.queue import Queue
from db.schemas.submission import Submission, SubmissionHistory
from db.schemas.submission_analysis_mapping import submission_analysis_mapping
from db.schemas.user import User


def build_read_all_query(
    alert_time_after: Optional[datetime] = None,
    alert_time_before: Optional[datetime] = None,
    contain_time_after: Optional[datetime] = None,
    contain_time_before: Optional[datetime] = None,
    created_time_after: Optional[datetime] = None,
    created_time_before: Optional[datetime] = None,
    disposition: Optional[str] = None,
    disposition_time_after: Optional[datetime] = None,
    disposition_time_before: Optional[datetime] = None,
    event_type: Optional[str] = None,
    name: Optional[str] = None,
    observable: Optional[str] = None,  # type|value
    observable_types: Optional[str] = None,
    observable_value: Optional[str] = None,
    owner: Optional[str] = None,
    prevention_tools: Optional[str] = None,
    queue: Optional[str] = None,
    remediation_time_after: Optional[datetime] = None,
    remediation_time_before: Optional[datetime] = None,
    remediations: Optional[str] = None,
    risk_level: Optional[str] = None,
    sort: Optional[str] = None,  # Example: created_time|desc,
    source: Optional[str] = None,
    status: Optional[str] = None,
    tags: Optional[str] = None,
    threat_actors: Optional[str] = None,
    threats: Optional[str] = None,
    vectors: Optional[str] = None,
):
    def _join_as_subquery(query: Select, subquery: Select):
        s = subquery.subquery()
        return query.join(s, Event.uuid == s.c.uuid).group_by(Event.uuid, Node.uuid)

    query = select(Event)

    if alert_time_after:
        # Outer join is used in case the event does not have any alerts (for some reason).
        alert_time_after_query = (
            select(Event)
            .outerjoin(Submission, onclause=Submission.event_uuid == Event.uuid)
            .where(or_(Event.alert_time > alert_time_after, Submission.insert_time > alert_time_after))
        )
        query = _join_as_subquery(query, alert_time_after_query)

    if alert_time_before:
        # Outer join is used in case the event does not have any alerts (for some reason).
        alert_time_before_query = (
            select(Event)
            .outerjoin(Submission, onclause=Submission.event_uuid == Event.uuid)
            .where(or_(Event.alert_time < alert_time_before, Submission.insert_time < alert_time_before))
        )
        query = _join_as_subquery(query, alert_time_before_query)

    if contain_time_after:
        contain_time_after_query = select(Event).where(Event.contain_time > contain_time_after)
        query = _join_as_subquery(query, contain_time_after_query).order_by(Event.contain_time.asc())

    if contain_time_before:
        contain_time_before_query = select(Event).where(Event.contain_time < contain_time_before)
        query = _join_as_subquery(query, contain_time_before_query).order_by(Event.contain_time.asc())

    if created_time_after:
        created_time_after_query = select(Event).where(Event.created_time > created_time_after)
        query = _join_as_subquery(query, created_time_after_query).order_by(Event.created_time.asc())

    if created_time_before:
        created_time_before_query = select(Event).where(Event.created_time < created_time_before)
        query = _join_as_subquery(query, created_time_before_query).order_by(Event.created_time.asc())

    if disposition:
        disposition_query = select(Event).join(Submission, onclause=Submission.event_uuid == Event.uuid)
        if disposition.lower() == "none":
            disposition_query = disposition_query.where(
                Submission.disposition_uuid == None  # pylint: disable=singleton-comparison
            )
        else:
            disposition_query = disposition_query.join(AlertDisposition).where(AlertDisposition.value == disposition)

        query = _join_as_subquery(query, disposition_query)

    if disposition_time_after:
        disposition_time_after_query = (
            select(Event)
            .join(Submission, onclause=Submission.event_uuid == Event.uuid)
            .where(
                or_(
                    Event.disposition_time > disposition_time_after,
                    Submission.history.any(
                        and_(
                            SubmissionHistory.field == "disposition",
                            SubmissionHistory.action_time > disposition_time_after,
                        )
                    ),
                )
            )
        )
        query = _join_as_subquery(query, disposition_time_after_query)

    if disposition_time_before:
        disposition_time_before_query = (
            select(Event)
            .join(Submission, onclause=Submission.event_uuid == Event.uuid)
            .where(
                or_(
                    Event.disposition_time < disposition_time_before,
                    Submission.history.any(
                        and_(
                            SubmissionHistory.field == "disposition",
                            SubmissionHistory.action_time < disposition_time_before,
                        )
                    ),
                )
            )
        )
        query = _join_as_subquery(query, disposition_time_before_query)

    if event_type:
        type_query = select(Event).join(EventType).where(EventType.value == event_type)
        query = _join_as_subquery(query, type_query)

    if name:
        name_query = select(Event).where(Event.name.ilike(f"%{name}%"))
        query = _join_as_subquery(query, name_query).order_by(Event.name.asc())

    if observable:
        observable_split = observable.split("|", maxsplit=1)
        observable_types_query = (
            select(Event)
            .join(Submission, onclause=Submission.event_uuid == Event.uuid)
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
            .where(ObservableType.value == observable_split[0], Observable.value == observable_split[1])
        )

        query = _join_as_subquery(query, observable_types_query)

    if observable_types:
        type_filters = [func.count(1).filter(ObservableType.value == t) > 0 for t in observable_types.split(",")]
        observable_types_query = (
            select(Event)
            .join(Submission, onclause=Submission.event_uuid == Event.uuid)
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
            .having(and_(*type_filters))
            .group_by(Event.uuid, Node.uuid)
        )

        query = _join_as_subquery(query, observable_types_query)

    if observable_value:
        observable_value_query = (
            select(Event)
            .join(Submission, onclause=Submission.event_uuid == Event.uuid)
            .join(
                submission_analysis_mapping, onclause=submission_analysis_mapping.c.submission_uuid == Submission.uuid
            )
            .join(
                analysis_child_observable_mapping,
                onclause=analysis_child_observable_mapping.c.analysis_uuid
                == submission_analysis_mapping.c.analysis_uuid,
            )
            .join(Observable, onclause=Observable.uuid == analysis_child_observable_mapping.c.observable_uuid)
            .where(Observable.value == observable_value)
        )

        query = _join_as_subquery(query, observable_value_query)

    if owner:
        owner_query = select(Event).join(User, onclause=Event.owner_uuid == User.uuid).where(User.username == owner)
        query = _join_as_subquery(query, owner_query)

    if prevention_tools:
        prevention_tool_filters = []
        for prevention_tool in prevention_tools.split(","):
            prevention_tool_filters.append(Event.prevention_tools.any(EventPreventionTool.value == prevention_tool))

        prevention_tools_query = select(Event).where(and_(*prevention_tool_filters))
        query = _join_as_subquery(query, prevention_tools_query)

    if queue:
        queue_query = select(Event).join(Queue).where(Queue.value == queue)
        query = _join_as_subquery(query, queue_query)

    if remediation_time_after:
        remediation_time_after_query = select(Event).where(Event.remediation_time > remediation_time_after)
        query = _join_as_subquery(query, remediation_time_after_query)

    if remediation_time_before:
        remediation_time_before_query = select(Event).where(Event.remediation_time < remediation_time_before)
        query = _join_as_subquery(query, remediation_time_before_query)

    if remediations:
        remediation_filters = []
        for remediation in remediations.split(","):
            remediation_filters.append(Event.remediations.any(EventRemediation.value == remediation))

        remediations_query = select(Event).where(and_(*remediation_filters))
        query = _join_as_subquery(query, remediations_query)

    if risk_level:
        risk_level_query = select(Event).join(EventRiskLevel).where(EventRiskLevel.value == risk_level)
        query = _join_as_subquery(query, risk_level_query)

    if source:
        source_query = select(Event).join(EventSource).where(EventSource.value == source)
        query = _join_as_subquery(query, source_query)

    if status:
        status_query = select(Event).join(EventStatus).where(EventStatus.value == status)
        query = _join_as_subquery(query, status_query)

    if tags:
        tag_filters = []
        for tag in tags.split(","):
            tag_filters.append(
                or_(
                    Event.tags.any(NodeTag.value == tag),
                    Event.alerts.any(Submission.tags.any(NodeTag.value == tag)),
                    Event.alerts.any(Submission.child_tags.any(NodeTag.value == tag)),
                )
            )
        tags_query = select(Event).where(and_(*tag_filters))

        query = _join_as_subquery(query, tags_query)

    if threat_actors:
        threat_actor_filters = []
        for threat in threat_actors.split(","):
            threat_actor_filters.append(
                or_(
                    Event.threat_actors.any(NodeThreatActor.value == threat),
                    Event.alerts.any(Submission.threat_actors.any(NodeThreatActor.value == threat)),
                    Event.alerts.any(Submission.child_threat_actors.any(NodeThreatActor.value == threat)),
                )
            )
        threat_actors_query = select(Event).where(and_(*threat_actor_filters))

        query = _join_as_subquery(query, threat_actors_query)

    if threats:
        threat_filters = []
        for threat in threats.split(","):
            threat_filters.append(
                or_(
                    Event.threats.any(NodeThreat.value == threat),
                    Event.alerts.any(Submission.threats.any(NodeThreat.value == threat)),
                    Event.alerts.any(Submission.child_threats.any(NodeThreat.value == threat)),
                )
            )
        threats_query = select(Event).where(and_(*threat_filters))

        query = _join_as_subquery(query, threats_query)

    if vectors:
        vector_filters = []
        for vector in vectors.split(","):
            vector_filters.append(Event.vectors.any(EventVector.value == vector))

        vectors_query = select(Event).where(and_(*vector_filters))
        query = _join_as_subquery(query, vectors_query)

    if sort:
        sort_split = sort.split("|")
        sort_by = sort_split[0]
        order = sort_split[1]

        if sort_by.lower() == "created_time":
            if order == "asc":
                query = query.order_by(Event.created_time.asc())
            elif order == "desc":
                query = query.order_by(Event.created_time.desc())

        # Only sort by event_type if we are not also filtering by event_type
        elif sort_by.lower() == "event_type" and not event_type:
            query = query.outerjoin(EventType, onclause=EventType.uuid == Event.type_uuid).group_by(
                Event.uuid, Node.uuid, EventType.value
            )
            if order == "asc":
                query = query.order_by(EventType.value.asc())
            elif order == "desc":
                query = query.order_by(EventType.value.desc())

        elif sort_by.lower() == "name":
            if order == "asc":
                query = query.order_by(Event.name.asc())
            elif order == "desc":
                query = query.order_by(Event.name.desc())

        # Only sort by owner if we are not also filtering by owner
        elif sort_by.lower() == "owner" and not owner:
            query = query.outerjoin(User, onclause=Event.owner_uuid == User.uuid).group_by(
                Event.uuid, Node.uuid, User.username
            )
            if order == "asc":
                query = query.order_by(User.username.asc())
            elif order == "desc":
                query = query.order_by(User.username.desc())

        # Only sort by risk_level if we are not also filtering by risk_level
        elif sort_by.lower() == "risk_level" and not risk_level:
            query = query.outerjoin(EventRiskLevel, onclause=EventRiskLevel.uuid == Event.risk_level_uuid).group_by(
                Event.uuid, Node.uuid, EventRiskLevel.value
            )
            if order == "asc":
                query = query.order_by(EventRiskLevel.value.asc())
            elif order == "desc":
                query = query.order_by(EventRiskLevel.value.desc())

        # Only sort by status if we are not also filtering by status
        elif sort_by.lower() == "status" and not status:
            query = query.join(EventStatus, onclause=EventStatus.uuid == Event.status_uuid).group_by(
                Event.uuid, Node.uuid, EventStatus.value
            )
            if order == "asc":
                query = query.order_by(EventStatus.value.asc())
            elif order == "desc":
                query = query.order_by(EventStatus.value.desc())

    return query


def create_or_read(model: EventCreate, db: Session) -> Event:
    # Create the new event Node using the data from the request
    obj: Event = crud.node.create(model=model, db_node_type=Event, db=db, exclude={"alert_uuids", "history_username"})

    # Set the various event properties
    obj.prevention_tools = crud.event_prevention_tool.read_by_values(values=model.prevention_tools, db=db)
    if model.owner:
        obj.owner = crud.user.read_by_username(username=model.owner, db=db)
    obj.queue = crud.queue.read_by_value(value=model.queue, db=db)
    obj.remediations = crud.event_remediation.read_by_values(values=model.remediations, db=db)
    if model.risk_level:
        obj.risk_level = crud.event_risk_level.read_by_value(value=model.risk_level, db=db)
    if model.source:
        obj.source = crud.event_source.read_by_value(value=model.source, db=db)
    obj.status = crud.event_status.read_by_value(value=model.status, db=db)
    if model.type:
        obj.type = crud.event_type.read_by_value(value=model.type, db=db)
    obj.uuid = model.uuid
    obj.vectors = crud.event_vector.read_by_values(values=model.vectors, db=db)

    # If the event could not be created, that implies that one already exists with the given UUID.
    # This is really only going to happen during testing when sometimes we add an event with a predefined UUID.
    if not crud.helpers.create(obj=obj, db=db):
        return read_by_uuid(uuid=model.uuid, db=db)

    # Add an event history entry if the history username was given.
    if model.history_username:
        crud.history.record_node_create_history(
            record_node=obj,
            action_by=crud.user.read_by_username(username=model.history_username, db=db),
            db=db,
        )

    return obj


def read_all(
    db: Session,
    alert_time_after: Optional[datetime] = None,
    alert_time_before: Optional[datetime] = None,
    contain_time_after: Optional[datetime] = None,
    contain_time_before: Optional[datetime] = None,
    created_time_after: Optional[datetime] = None,
    created_time_before: Optional[datetime] = None,
    disposition: Optional[str] = None,
    disposition_time_after: Optional[datetime] = None,
    disposition_time_before: Optional[datetime] = None,
    event_type: Optional[str] = None,
    name: Optional[str] = None,
    observable: Optional[str] = None,  # type|value
    observable_types: Optional[str] = None,
    observable_value: Optional[str] = None,
    owner: Optional[str] = None,
    prevention_tools: Optional[str] = None,
    queue: Optional[str] = None,
    remediation_time_after: Optional[datetime] = None,
    remediation_time_before: Optional[datetime] = None,
    remediations: Optional[str] = None,
    risk_level: Optional[str] = None,
    sort: Optional[str] = None,  # Example: created_time|desc,
    source: Optional[str] = None,
    status: Optional[str] = None,
    tags: Optional[str] = None,
    threat_actors: Optional[str] = None,
    threats: Optional[str] = None,
    vectors: Optional[str] = None,
) -> list[Event]:
    return (
        db.execute(
            build_read_all_query(
                alert_time_after=alert_time_after,
                alert_time_before=alert_time_before,
                contain_time_after=contain_time_after,
                contain_time_before=contain_time_before,
                created_time_after=created_time_after,
                created_time_before=created_time_before,
                disposition=disposition,
                disposition_time_after=disposition_time_after,
                disposition_time_before=disposition_time_before,
                event_type=event_type,
                name=name,
                observable=observable,
                observable_types=observable_types,
                observable_value=observable_value,
                owner=owner,
                prevention_tools=prevention_tools,
                queue=queue,
                remediation_time_after=remediation_time_after,
                remediation_time_before=remediation_time_before,
                remediations=remediations,
                risk_level=risk_level,
                sort=sort,
                source=source,
                status=status,
                tags=tags,
                threat_actors=threat_actors,
                threats=threats,
                vectors=vectors,
            )
        )
        .scalars()
        .all()
    )


def read_all_history(uuid: UUID, db: Session) -> list[EventHistory]:
    return (
        db.execute(crud.history.build_read_history_query(history_table=EventHistory, record_uuid=uuid)).scalars().all()
    )


def read_analysis_type_from_event(
    analysis_module_type: str, uuid: UUID, db: Session, starts_with: bool = False
) -> list[tuple[UUID, Analysis]]:
    """
    Returns a list of tuples containing the alert UUID and the analysis object where the list contains every
    analysis of the given type that was performed in the given event UUID.
    """
    if starts_with:
        clause = AnalysisModuleType.value.startswith(analysis_module_type)
    else:
        clause = AnalysisModuleType.value == analysis_module_type

    # Get all the email analyses (and their parent alert UUIDs) performed in the event.
    query = (
        select([Submission.uuid, Analysis])
        .join(
            submission_analysis_mapping,
            onclause=submission_analysis_mapping.c.analysis_uuid == Analysis.uuid,
        )
        .join(
            AnalysisModuleType,
            onclause=and_(
                AnalysisModuleType.uuid == Analysis.analysis_module_type_uuid,
                clause,
            ),
        )
        .join(
            Submission,
            onclause=and_(
                Submission.uuid == submission_analysis_mapping.c.submission_uuid, Submission.event_uuid == uuid
            ),
        )
        .options(Load(Analysis).undefer("details"))
        .order_by(Analysis.run_time.asc())
    )

    return db.execute(query).unique().all()


def read_by_uuid(uuid: UUID, db: Session, inject_analysis_types: bool = False) -> Event:
    obj = crud.helpers.read_by_uuid(db_table=Event, uuid=uuid, db=db)

    if inject_analysis_types:
        query = (
            select(AnalysisModuleType)
            .join(Analysis, onclause=Analysis.analysis_module_type_uuid == AnalysisModuleType.uuid)
            .join(submission_analysis_mapping, onclause=submission_analysis_mapping.c.analysis_uuid == Analysis.uuid)
            .join(Submission, onclause=Submission.uuid == submission_analysis_mapping.c.submission_uuid)
            .where(Submission.event_uuid == uuid)
            .order_by(AnalysisModuleType.value)
            .distinct()
        )

        analysis_types: list[AnalysisModuleType] = db.execute(query).scalars().all()
        obj.analysis_types = [x.value for x in analysis_types]

    return obj


def read_observable_type_from_event(observable_type: str, uuid: UUID, db: Session) -> list[Observable]:
    query = (
        select(Observable)
        .join(
            analysis_child_observable_mapping,
            onclause=analysis_child_observable_mapping.c.observable_uuid == Observable.uuid,
        )
        .join(
            submission_analysis_mapping,
            onclause=submission_analysis_mapping.c.analysis_uuid == analysis_child_observable_mapping.c.analysis_uuid,
        )
        .join(
            Submission,
            onclause=and_(
                Submission.uuid == submission_analysis_mapping.c.submission_uuid, Submission.event_uuid == uuid
            ),
        )
        .where(Observable.type.has(ObservableType.value == observable_type))
    )

    return db.execute(query).unique().scalars().all()


def read_summary_detection_point(uuid: UUID, db: Session) -> list[DetectionSummary]:
    # Verify the event exists
    read_by_uuid(uuid=uuid, db=db)

    # Get all the detection points (and their parent alert UUIDs) performed in the event.
    # The query results are turned into a dictionary with the parent alert UUID as the key.
    query = (
        select([Submission.uuid, NodeDetectionPoint])
        .join(Observable, onclause=Observable.uuid == NodeDetectionPoint.node_uuid)
        .join(
            analysis_child_observable_mapping,
            onclause=analysis_child_observable_mapping.c.observable_uuid == Observable.uuid,
        )
        .join(
            submission_analysis_mapping,
            onclause=submission_analysis_mapping.c.analysis_uuid == analysis_child_observable_mapping.c.analysis_uuid,
        )
        .join(
            Submission,
            onclause=and_(
                Submission.uuid == submission_analysis_mapping.c.submission_uuid, Submission.event_uuid == uuid
            ),
        )
    )

    alert_uuid_and_detection: list[tuple[UUID, NodeDetectionPoint]] = db.execute(query).unique().all()

    # Loop through the database results to count the number of times each detection point value occurred
    results: dict[UUID, DetectionSummary] = {}
    for alert_uuid, detection_point in alert_uuid_and_detection:
        if detection_point.value not in results:
            results[detection_point.value] = detection_point
            results[detection_point.value].count = 1
            results[detection_point.value].alert_uuid = alert_uuid
        else:
            results[detection_point.value].count += 1

    # Return the summaries sorted by their values
    return sorted(results.values(), key=lambda x: x.value)


def read_summary_email(uuid: UUID, db: Session) -> list[EmailSummary]:
    # Verify the event exists
    read_by_uuid(uuid=uuid, db=db)

    alert_uuid_and_analysis = read_analysis_type_from_event(analysis_module_type="Email Analysis", uuid=uuid, db=db)
    results: list[EmailSummary] = []
    unique_emails = []
    for alert_uuid, analysis in alert_uuid_and_analysis:
        # Skip this email if it is a duplicate
        details_hash = DeepHash(analysis.details)[analysis.details]
        if details_hash in unique_emails:
            continue
        else:
            unique_emails.append(details_hash)

        results.append(EmailSummary(**analysis.details, alert_uuid=alert_uuid))

    # Return the summaries by the email time
    return sorted(results, key=lambda x: x.time)


def read_summary_email_headers_body(uuid: UUID, db: Session) -> Optional[EmailHeadersBody]:
    # Verify the event exists
    read_by_uuid(uuid=uuid, db=db)

    if alert_uuid_and_analysis := read_analysis_type_from_event(
        analysis_module_type="Email Analysis", uuid=uuid, db=db
    ):
        # Return the earliest email
        sorted_alert_and_analysis = sorted(alert_uuid_and_analysis, key=lambda x: x[1].details["time"])
        return EmailHeadersBody(**sorted_alert_and_analysis[0][1].details, alert_uuid=sorted_alert_and_analysis[0][0])

    return None


def read_summary_observable(uuid: UUID, db: Session) -> list[ObservableSummary]:
    # Verify the event exists
    read_by_uuid(uuid=uuid, db=db)

    alert_uuid_and_analysis = read_analysis_type_from_event(
        analysis_module_type="FA Queue", starts_with=True, uuid=uuid, db=db
    )

    # Loop over the FA Queue analyses and inject their results into the observables to create
    # the observable summaries.
    results = set()
    for _, faqueue_analysis in alert_uuid_and_analysis:
        analysis_details = FAQueueAnalysisDetails(**faqueue_analysis.details)
        faqueue_analysis.target.faqueue_hits = analysis_details.hits
        faqueue_analysis.target.faqueue_link = analysis_details.link
        results.add(faqueue_analysis.target)

    # Return the observables sorted by their type then value
    return sorted(results, key=lambda x: (x.type.value, x.value))


def read_summary_sandbox(uuid: UUID, db: Session) -> list[SandboxSummary]:
    def _prettify_process_tree(processes: list[SandboxProcess], text="", depth=0) -> str:
        if not text:
            pids = [proc.pid for proc in processes]
            root_pids = [proc.pid for proc in processes if proc.parent_pid not in pids]

            for process in processes:
                process.children = [proc for proc in processes if proc.parent_pid == process.pid]

            processes = [proc for proc in processes if proc.pid in root_pids]

        for process in processes:
            text += f"{'    ' * depth}{process.command}\n"

            if process.children:
                text = _prettify_process_tree(process.children, text=text, depth=depth + 1)

        return text

    # Verify the event exists
    read_by_uuid(uuid=uuid, db=db)

    alert_uuid_and_analysis = read_analysis_type_from_event(
        analysis_module_type="Sandbox Analysis", starts_with=True, uuid=uuid, db=db
    )

    # Build a list of SandboxSummary objects from the unique sandbox analyses
    results: list[SandboxSummary] = []
    lookup = set()
    for alert_uuid, sandbox_analysis in alert_uuid_and_analysis:
        # Skip this sandbox report if it is a duplicate
        details_hash = DeepHash(sandbox_analysis.details)[sandbox_analysis.details]
        if details_hash in lookup:
            continue
        else:
            lookup.add(details_hash)

        # Create the SandboxSummary object and prettyify its process tree if there are processes
        report_summary = SandboxSummary(**sandbox_analysis.details, alert_uuid=alert_uuid)
        if report_summary.processes:
            report_summary.process_tree = _prettify_process_tree(report_summary.processes).strip()

        results.append(report_summary)

    # Return the summaries by the filename
    return sorted(results, key=lambda x: x.filename)


def read_summary_url_domain(uuid: UUID, db: Session) -> URLDomainSummary:
    # Verify the event exists
    read_by_uuid(uuid=uuid, db=db)

    # Loop through the URL observables to count the domains. The key is the URL, and the value is
    # a URLDomainSummary object.
    # NOTE: This assumes the URL values are validated as they are added to the database.
    urls = read_observable_type_from_event(observable_type="url", uuid=uuid, db=db)

    return crud.helpers.read_summary_url_domain(url_observables=urls, db=db)


def read_summary_user(uuid: UUID, db: Session) -> list[UserSummary]:
    # Verify the event exists
    read_by_uuid(uuid=uuid, db=db)

    # Get the unique user analysis details
    alert_uuid_and_analysis = read_analysis_type_from_event(analysis_module_type="User Analysis", uuid=uuid, db=db)
    results: list[UserSummary] = []
    lookup = set()
    for _, user_analysis in alert_uuid_and_analysis:
        if user_analysis.details["email"] in lookup:
            continue
        else:
            lookup.add(user_analysis.details["email"])

        results.append(UserSummary(**user_analysis.details))

    # Return the analysis details sorted by the email addresses
    return sorted(results, key=lambda x: (x.email))


def update(uuid: UUID, model: EventUpdate, db: Session):
    # Update the Node attributes
    event, diffs = crud.node.update(model=model, uuid=uuid, db_table=Event, db=db)

    # Get the data that was given in the request and use it to update the database object
    update_data = model.dict(exclude_unset=True)

    if "alert_time" in update_data:
        diffs.append(crud.history.create_diff(field="alert_time", old=event.alert_time, new=update_data["alert_time"]))
        event.alert_time = update_data["alert_time"]

    if "contain_time" in update_data:
        diffs.append(
            crud.history.create_diff(field="contain_time", old=event.contain_time, new=update_data["contain_time"])
        )
        event.contain_time = update_data["contain_time"]

    if "disposition_time" in update_data:
        diffs.append(
            crud.history.create_diff(
                field="disposition_time", old=event.disposition_time, new=update_data["disposition_time"]
            )
        )
        event.disposition_time = update_data["disposition_time"]

    if "event_time" in update_data:
        diffs.append(crud.history.create_diff(field="event_time", old=event.event_time, new=update_data["event_time"]))
        event.event_time = update_data["event_time"]

    if "name" in update_data:
        diffs.append(crud.history.create_diff(field="name", old=event.name, new=update_data["name"]))
        event.name = update_data["name"]

    if "owner" in update_data:
        old = event.owner.username if event.owner else None
        diffs.append(crud.history.create_diff(field="owner", old=old, new=update_data["owner"]))

        if update_data["owner"]:
            event.owner = crud.user.read_by_username(username=update_data["owner"], db=db)
        else:
            event.owner = None

    if "ownership_time" in update_data:
        diffs.append(
            crud.history.create_diff(
                field="ownership_time", old=event.ownership_time, new=update_data["ownership_time"]
            )
        )
        event.ownership_time = update_data["ownership_time"]

    if "prevention_tools" in update_data:
        diffs.append(
            crud.history.create_diff(
                field="prevention_tools",
                old=[x.value for x in event.prevention_tools],
                new=update_data["prevention_tools"],
            )
        )

        if update_data["prevention_tools"]:
            event.prevention_tools = crud.event_prevention_tool.read_by_values(
                values=update_data["prevention_tools"], db=db
            )
        else:
            event.prevention_tools = []

    if "queue" in update_data:
        diffs.append(crud.history.create_diff(field="queue", old=event.queue.value, new=update_data["queue"]))
        event.queue = crud.queue.read_by_value(value=update_data["queue"], db=db)

    if "remediation_time" in update_data:
        diffs.append(
            crud.history.create_diff(
                field="remediation_time", old=event.remediation_time, new=update_data["remediation_time"]
            )
        )
        event.remediation_time = update_data["remediation_time"]

    if "remediations" in update_data:
        diffs.append(
            crud.history.create_diff(
                field="remediations",
                old=[x.value for x in event.remediations],
                new=update_data["remediations"],
            )
        )

        if update_data["remediations"]:
            event.remediations = crud.event_remediation.read_by_values(values=update_data["remediations"], db=db)
        else:
            event.remediations = []

    if "risk_level" in update_data:
        old = event.risk_level.value if event.risk_level else None
        diffs.append(crud.history.create_diff(field="risk_level", old=old, new=update_data["risk_level"]))

        if update_data["risk_level"]:
            event.risk_level = crud.event_risk_level.read_by_value(value=update_data["risk_level"], db=db)
        else:
            event.risk_level = None

    if "source" in update_data:
        old = event.source.value if event.source else None
        diffs.append(crud.history.create_diff(field="source", old=old, new=update_data["source"]))

        if update_data["source"]:
            event.source = crud.event_source.read_by_value(value=update_data["source"], db=db)
        else:
            event.source = None

    if "status" in update_data:
        diffs.append(crud.history.create_diff(field="status", old=event.status.value, new=update_data["status"]))

        event.status = crud.event_status.read_by_value(value=update_data["status"], db=db)

    if "type" in update_data:
        old = event.type.value if event.type else None
        diffs.append(crud.history.create_diff(field="type", old=old, new=update_data["type"]))

        if update_data["type"]:
            event.type = crud.event_type.read_by_value(value=update_data["type"], db=db)
        else:
            event.type = None

    if "vectors" in update_data:
        diffs.append(
            crud.history.create_diff(
                field="vectors",
                old=[x.value for x in event.vectors],
                new=update_data["vectors"],
            )
        )

        if update_data["vectors"]:
            event.vectors = crud.event_vector.read_by_values(values=update_data["vectors"], db=db)
        else:
            event.vectors = []

    db.flush()

    # Add an event history entry if the history username was given. This would typically only be
    # supplied by the GUI when an analyst updates an event.
    if model.history_username is not None:
        crud.history.record_node_update_history(
            record_node=event,
            action_by=crud.user.read_by_username(username=model.history_username, db=db),
            diffs=diffs,
            db=db,
        )
