from fastapi import Depends
from sqlalchemy import and_
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import join, select
from typing import Dict, List
from urllib.parse import urlparse
from uuid import UUID

from api.models.event_summaries import URLDomainSummary
from db import crud
from db.database import get_db
from db.schemas.analysis import Analysis
from db.schemas.analysis_module_type import AnalysisModuleType
from db.schemas.event import Event
from db.schemas.node import Node
from db.schemas.node_tree import NodeTree
from db.schemas.observable import Observable
from db.schemas.observable_type import ObservableType


#
# OBSERVABLE
#


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
            ),
        )
        .where(NodeTree.root_node_uuid.in_(event.alert_uuids))
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
        if "hits" in faqueue_analysis.details:
            node_tree_and_observables[parent_uuid].faqueue_hits = faqueue_analysis.details["hits"]

            if "link" in faqueue_analysis.details:
                node_tree_and_observables[parent_uuid].faqueue_link = faqueue_analysis.details["link"]
            else:
                node_tree_and_observables[parent_uuid].faqueue_link = ""

            results.add(node_tree_and_observables[parent_uuid])

    # Return the observables sorted by their type then value
    return sorted(results, key=lambda x: (x.type.value, x.value))


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
    domain_count: Dict[str, URLDomainSummary] = dict()
    for url in urls:
        parsed_url = urlparse(url.value)
        if parsed_url.hostname not in domain_count:
            domain_count[parsed_url.hostname] = 1
            domain_count[parsed_url.hostname] = URLDomainSummary(domain=parsed_url.hostname, count=1, total=len(urls))
        else:
            domain_count[parsed_url.hostname].count += 1

    # Return a list of the URLDomainSummary objects sorted by their count (highest first) then the domain.
    # There isn't a built-in way to do this type of sort, so first sort by the secondary value (the domain).
    # Then sort by the primary value (the count).
    sorted_results = sorted(domain_count.values(), key=lambda x: x.domain)
    return sorted(sorted_results, key=lambda x: x.count, reverse=True)


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
        # Skip this analysis if it does not have the required fields
        if "user_id" not in user_analysis.details or "email" not in user_analysis.details:
            continue

        if user_analysis.details["email"] in unique_emails:
            continue

        unique_emails.add(user_analysis.details["email"])
        results.append(user_analysis.details)

    # Return the analysis details sorted by the email addresses
    return sorted(results, key=lambda x: (x["email"]))
