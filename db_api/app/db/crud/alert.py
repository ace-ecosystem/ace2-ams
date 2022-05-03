import json

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from api_models.alert import AlertCreate, AlertTreeRead
from api_models.analysis import AnalysisNodeTreeRead
from api_models.observable import ObservableNodeTreeRead
from db import crud
from db.schemas.alert import Alert


def create(model: AlertCreate, db: Session) -> Alert:
    obj = Alert(
        description=model.description,
        event_time=model.event_time,
        insert_time=model.insert_time,
        instructions=model.instructions,
        name=model.name,
        queue=crud.queue.read_by_value(value=model.queue, db=db),
        tool=crud.alert_tool.read_by_value(value=model.tool, db=db),
        tool_instance=crud.alert_tool_instance.read_by_value(value=model.tool_instance, db=db),
        type=crud.alert_type.read_by_value(value=model.type, db=db),
        uuid=model.uuid,
    )

    if model.owner is not None:
        obj.owner = crud.user.read_by_username(username=model.owner, db=db)

    db.add(obj)
    db.flush()

    # Associate the observables with the alert after the alert is flushed to the database. This is because
    # the alert UUID is required if the observables also go on to create analyses since an analysis object
    # gets linked to an existing alert.
    obj.root_observables = [crud.observable.create(model=o, db=db) for o in model.root_observables]

    return obj


def read_by_uuid(uuid: UUID, db: Session) -> Optional[Alert]:
    return db.execute(select(Alert).where(Alert.uuid == uuid)).scalars().one_or_none()


def read_tree(uuid: UUID, db: Session) -> dict:
    # The Alert db object has "analyses" list and "root_observables" list. Each observable in root_observables will
    # be a top-level key in the returned dictionary. The "analyses" list is every unique analysis object in the alert.
    db_alert = read_by_uuid(uuid=uuid, db=db)

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
