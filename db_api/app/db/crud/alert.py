import json

from fastapi.encoders import jsonable_encoder
from sqlalchemy import insert, select
from sqlalchemy.orm import Session
from uuid import UUID

from api_models.alert import AlertTreeRead
from api_models.analysis import AnalysisNodeTreeRead
from api_models.observable import ObservableNodeTreeRead
from db.schemas.alert import Alert
from db.schemas.alert_root_observable_mapping import alert_root_observable_mapping


def add_root_observable_to_root_analysis(observable_uuid: UUID, root_analysis_uuid: UUID, db: Session):
    existing = (
        db.execute(
            select(alert_root_observable_mapping).where(
                alert_root_observable_mapping.c.alert_uuid == root_analysis_uuid,
                alert_root_observable_mapping.c.observable_uuid == observable_uuid,
            )
        )
        .scalars()
        .one_or_none()
    )

    if existing is None:
        db.execute(
            insert(alert_root_observable_mapping).values(alert_uuid=root_analysis_uuid, observable_uuid=observable_uuid)
        )


def read_alert_by_uuid(uuid: UUID, db: Session) -> Alert:
    return db.execute(select(Alert).where(Alert.uuid == uuid)).scalars().one()


def read_tree(uuid: UUID, db: Session) -> dict:
    # The Alert db object has "analyses" list and "root_observables" list. Each observable in root_observables will
    # be a top-level key in the returned dictionary. The "analyses" list is every unique analysis object in the alert.
    db_alert = read_alert_by_uuid(uuid=uuid, db=db)

    # Organize the root observables in a dictionary where their UUID is the key
    root_observables: dict[UUID, ObservableNodeTreeRead] = {
        o.uuid: o.serialize_for_node_tree() for o in db_alert.root_observables
    }

    # Organize the child observables in a dictionary where their UUID is the key
    db_child_observables = {co for a in db_alert.analyses for co in a.child_observables}
    child_observables: dict[UUID, ObservableNodeTreeRead] = {
        o.uuid: o.serialize_for_node_tree() for o in db_child_observables
    }

    # Organize the analyses in a dictionary where their parent_observable_uuid is the key as well as
    # a dictionary where their own UUID is the key. Both forms of lookup are required to build the tree.
    analyses_by_parent_observable: dict[UUID, list[AnalysisNodeTreeRead]] = {}
    analyses_by_uuid: dict[UUID, AnalysisNodeTreeRead] = {}
    for db_analysis in db_alert.analyses:
        if db_analysis.parent_observable_uuid not in analyses_by_parent_observable:
            analyses_by_parent_observable[db_analysis.parent_observable_uuid] = []

        analysis = db_analysis.serialize_for_node_tree()
        analyses_by_parent_observable[db_analysis.parent_observable_uuid].append(analysis)
        analyses_by_uuid[db_analysis.uuid] = analysis

        # If this analysis has child observables, add the serialized observable as a child to the serialized analysis.
        for db_child_observable in db_analysis.child_observables:
            analyses_by_uuid[db_analysis.uuid].children.append(child_observables[db_child_observable.uuid])

    # Loop over each overvable and add its analysis as a child
    for observable_uuid, observable in list(root_observables.items()) + list(child_observables.items()):

        if observable_uuid in analyses_by_parent_observable:
            observable.children = analyses_by_parent_observable[observable_uuid]

    # Create the AlertTree object and add the root observables as its children
    alert_tree = AlertTreeRead(**db_alert.__dict__)
    alert_tree.children = list(root_observables.values())

    # Now that the tree structure is built, we need to walk it to mark which of the leaves have
    # already appeared in the tree. This is useful for when you might not want to display or
    # process a leaf in the tree if it is a duplicate (ex: the GUI auto-collapses duplicate leaves).
    #
    # But before the tree can be traversed, it needs to be serialized into JSON. If an observable or analysis
    # is repeated in the tree, it is just a reference to the same object, so updating its "first_appearance"
    # property would change the value for every instance of the object (which we do not want).
    #
    # Adapted from: https://www.geeksforgeeks.org/preorder-traversal-of-n-ary-tree-without-recursion/
    alert_tree_json: dict = json.loads(alert_tree.json(encoder=jsonable_encoder))
    unique_uuids: set[UUID] = set()
    unvisited = [alert_tree_json]
    while unvisited:
        current = unvisited.pop(0)

        if current["uuid"] in unique_uuids:
            current["first_appearance"] = False
        else:
            current["first_appearance"] = True
            unique_uuids.add(current["uuid"])

        for idx in range(len(current["children"]) - 1, -1, -1):
            unvisited.insert(0, current["children"][idx])

    return alert_tree_json
