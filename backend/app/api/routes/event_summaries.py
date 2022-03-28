from deepdiff import DeepHash
from fastapi import Depends
from sqlalchemy import and_
from sqlalchemy.orm import Load, Session
from sqlalchemy.sql.expression import join, select
from typing import Dict, List, Tuple
from urllib.parse import urlparse
from uuid import UUID

from api.models.analysis_details import FAQueueAnalysisDetails
from api.models.event_summaries import (
    EmailHeadersBody,
    EmailSummary,
    SandboxSummary,
    URLDomainSummaryIndividual,
    UserSummary,
)
from db import crud
from db.database import get_db
from db.schemas.analysis import Analysis
from db.schemas.analysis_module_type import AnalysisModuleType
from db.schemas.event import Event
from db.schemas.node import Node
from db.schemas.node_detection_point import NodeDetectionPoint
from db.schemas.node_tree import NodeTree
from db.schemas.observable import Observable
from db.schemas.observable_type import ObservableType


def get_detection_point_summary(uuid: UUID, db: Session = Depends(get_db)):
    # Get the event from the database
    event: Event = crud.read(uuid=uuid, db_table=Event, db=db)

    # Get all the detection points (and their parent NodeTree UUIDs) performed in the event.
    # The query results are turned into a dictionary with the parent NodeTree UUID as the key.
    query = (
        select([NodeTree.root_node_uuid, NodeDetectionPoint])
        .select_from(join(NodeTree, Node, NodeTree.node_uuid == Node.uuid))
        .join(
            NodeDetectionPoint,
            onclause=and_(
                NodeDetectionPoint.node_uuid == NodeTree.node_uuid,
                NodeTree.root_node_uuid.in_(event.alert_uuids),
            ),
        )
    )

    alert_uuid_and_detection: List[Tuple[UUID, NodeDetectionPoint]] = db.execute(query).unique().fetchall()

    # Loop through the database results to count the number of times each detection point value occurred
    results: Dict[str, NodeDetectionPoint] = dict()
    for alert_uuid, detection_point in alert_uuid_and_detection:
        if detection_point.value not in results:
            results[detection_point.value] = detection_point
            results[detection_point.value].count = 1
            results[detection_point.value].alert_uuid = alert_uuid
        else:
            results[detection_point.value].count += 1

    # Return the summaries sorted by their values
    return sorted(results.values(), key=lambda x: x.value)


def get_email_headers_body_summary(uuid: UUID, db: Session = Depends(get_db)):
    # Get the event from the database
    event: Event = crud.read(uuid=uuid, db_table=Event, db=db)

    # Get all the email analyses (and their root Node UUIDs) performed in the event.
    query = (
        select([NodeTree.root_node_uuid, Analysis])
        .select_from(join(NodeTree, Node, NodeTree.node_uuid == Node.uuid))
        .join(
            Analysis,
            onclause=and_(
                Node.node_type == "analysis",
                Analysis.uuid == NodeTree.node_uuid,
                Analysis.analysis_module_type.has(AnalysisModuleType.value == "Email Analysis"),
                NodeTree.root_node_uuid.in_(event.alert_uuids),
            ),
        )
        .options(Load(Analysis).undefer("details"))
    )

    alert_uuid_and_analysis: List[Tuple[UUID, Analysis]] = db.execute(query).unique().fetchall()

    # Return the headers and body of the earliest email in the event
    if alert_uuid_and_analysis:
        sorted_alert_and_analysis = sorted(alert_uuid_and_analysis, key=lambda x: x[1].details["time"])
        return EmailHeadersBody(**sorted_alert_and_analysis[0][1].details, alert_uuid=sorted_alert_and_analysis[0][0])


def get_email_summary(uuid: UUID, db: Session = Depends(get_db)):
    # Get the event from the database
    event: Event = crud.read(uuid=uuid, db_table=Event, db=db)

    # Get all the email analyses (and their root Node UUIDs) performed in the event.
    query = (
        select([NodeTree.root_node_uuid, Analysis])
        .select_from(join(NodeTree, Node, NodeTree.node_uuid == Node.uuid))
        .join(
            Analysis,
            onclause=and_(
                Node.node_type == "analysis",
                Analysis.uuid == NodeTree.node_uuid,
                Analysis.analysis_module_type.has(AnalysisModuleType.value == "Email Analysis"),
                NodeTree.root_node_uuid.in_(event.alert_uuids),
            ),
        )
        .options(Load(Analysis).undefer("details"))
    )

    alert_uuid_and_analysis: List[Tuple[UUID, Analysis]] = db.execute(query).unique().fetchall()

    # Build a list of EmailSummary objects from the unique email analyses
    results: List[EmailSummary] = []
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


def get_observable_summary(uuid: UUID, db: Session = Depends(get_db)):
    # Get the event from the database
    event: Event = crud.read(uuid=uuid, db_table=Event, db=db)

    # Get all the FA Queue analyses (and their parent NodeTree UUIDs) performed in the event.
    # The query results are turned into a dictionary with the parent NodeTree UUID as the key.
    query = (
        select([NodeTree.parent_tree_uuid, Analysis])
        .select_from(join(NodeTree, Node, NodeTree.node_uuid == Node.uuid))
        .join(
            Analysis,
            onclause=and_(
                Node.node_type == "analysis",
                Analysis.uuid == NodeTree.node_uuid,
                Analysis.analysis_module_type.has(AnalysisModuleType.value.startswith("FA Queue")),
                NodeTree.root_node_uuid.in_(event.alert_uuids),
            ),
        )
    )

    node_tree_and_faqueue: Dict[UUID, Analysis] = dict(db.execute(query).unique().fetchall())

    # Get all the observables (and their NodeTree UUIDs) that go with the FA Queue analyses.
    # The query results are turned into a dictionary with the NodeTree UUID as the key.
    query = (
        select([NodeTree.uuid, Observable])
        .select_from(join(NodeTree, Node, NodeTree.node_uuid == Node.uuid))
        .where(Node.node_type == "observable", NodeTree.uuid.in_(node_tree_and_faqueue.keys()))
    )

    node_tree_and_observables: Dict[UUID, Observable] = dict(db.execute(query).unique().fetchall())

    # Loop over the FA Queue analyses and inject their results into the observables.
    results = set()
    for parent_uuid, faqueue_analysis in node_tree_and_faqueue.items():
        analysis_details = FAQueueAnalysisDetails(**faqueue_analysis.details)
        node_tree_and_observables[parent_uuid].faqueue_hits = analysis_details.hits
        node_tree_and_observables[parent_uuid].faqueue_link = analysis_details.link
        results.add(node_tree_and_observables[parent_uuid])

    # Return the observables sorted by their type then value
    return sorted(results, key=lambda x: (x.type.value, x.value))


def get_sandbox_summary(uuid: UUID, db: Session = Depends(get_db)):
    # Get the event from the database
    event: Event = crud.read(uuid=uuid, db_table=Event, db=db)

    # Get all the sandbox analyses (and their root Node UUIDs) performed in the event.
    query = (
        select([NodeTree.root_node_uuid, Analysis])
        .select_from(join(NodeTree, Node, NodeTree.node_uuid == Node.uuid))
        .join(
            Analysis,
            onclause=and_(
                Node.node_type == "analysis",
                Analysis.uuid == NodeTree.node_uuid,
                Analysis.analysis_module_type.has(AnalysisModuleType.value.startswith("Sandbox Analysis")),
                NodeTree.root_node_uuid.in_(event.alert_uuids),
            ),
        )
        .options(Load(Analysis).undefer("details"))
    )

    alert_uuid_and_analysis: List[Tuple[UUID, Analysis]] = db.execute(query).unique().fetchall()

    # Build a list of SandboxSummary objects from the unique email analyses
    results: List[SandboxSummary] = []
    unique = []
    for alert_uuid, analysis in alert_uuid_and_analysis:
        # Skip this sandbox report if it is a duplicate
        details_hash = DeepHash(analysis.details)[analysis.details]
        if details_hash in unique:
            continue
        else:
            unique.append(details_hash)

        results.append(SandboxSummary(**analysis.details, alert_uuid=alert_uuid))

    # Return the summaries by the filename
    return sorted(results, key=lambda x: x.filename)


def get_url_domain_summary(uuid: UUID, db: Session = Depends(get_db)):
    # Get the event from the database
    event: Event = crud.read(uuid=uuid, db_table=Event, db=db)

    # Get all the URL observables in the event.
    query = select(Observable).join(
        NodeTree,
        onclause=and_(
            NodeTree.node_uuid == Observable.uuid,
            NodeTree.root_node_uuid.in_(event.alert_uuids),
            Observable.type.has(ObservableType.value == "url"),
        ),
    )

    urls: List[Observable] = db.execute(query).unique().scalars().all()

    # Loop through the URL observables to count the domains. The key is the URL, and the value is
    # a URLDomainSummary object.
    # NOTE: This assumes the URL values are validated as they are added to the database.
    domain_count: Dict[str, URLDomainSummaryIndividual] = dict()
    for url in urls:
        parsed_url = urlparse(url.value)
        if parsed_url.hostname not in domain_count:
            domain_count[parsed_url.hostname] = 1
            domain_count[parsed_url.hostname] = URLDomainSummaryIndividual(domain=parsed_url.hostname, count=1)
        else:
            domain_count[parsed_url.hostname].count += 1

    # Return a list of the URLDomainSummary objects sorted by their count (highest first) then the domain.
    # There isn't a built-in way to do this type of sort, so first sort by the secondary value (the domain).
    # Then sort by the primary value (the count).
    sorted_results = sorted(domain_count.values(), key=lambda x: x.domain)
    sorted_results = sorted(sorted_results, key=lambda x: x.count, reverse=True)

    return {"domains": sorted_results, "total": len(urls)}


def get_user_summary(uuid: UUID, db: Session = Depends(get_db)):
    # Get the event from the database
    event: Event = crud.read(uuid=uuid, db_table=Event, db=db)

    # Get all the user analyses performed in the event.
    query = select(Analysis).join(
        NodeTree,
        onclause=and_(
            NodeTree.node_uuid == Analysis.uuid,
            NodeTree.root_node_uuid.in_(event.alert_uuids),
            Analysis.analysis_module_type.has(AnalysisModuleType.value == "User Analysis"),
        ),
    )

    user_analyses: List[Analysis] = db.execute(query).scalars().all()

    # Get the unique user analysis details
    unique_emails = set()
    results = []
    for user_analysis in user_analyses:
        if user_analysis.details["email"] in unique_emails:
            continue
        else:
            unique_emails.add(user_analysis.details["email"])

        results.append(UserSummary(**user_analysis.details))

    # Return the analysis details sorted by the email addresses
    return sorted(results, key=lambda x: (x.email))
