from fastapi import Depends
from sqlalchemy import and_
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import join, select
from typing import Dict
from uuid import UUID

from db import crud
from db.database import get_db
from db.schemas.analysis import Analysis
from db.schemas.analysis_module_type import AnalysisModuleType
from db.schemas.event import Event
from db.schemas.node import Node
from db.schemas.node_tree import NodeTree
from db.schemas.observable import Observable


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
        node_tree_and_observables[parent_uuid].faqueue_hits = faqueue_analysis.details["hits"]
        node_tree_and_observables[parent_uuid].faqueue_link = faqueue_analysis.details["link"]
        results.add(node_tree_and_observables[parent_uuid])

    # Return the observables sorted by their type then value
    return sorted(results, key=lambda x: (x.type.value, x.value))
