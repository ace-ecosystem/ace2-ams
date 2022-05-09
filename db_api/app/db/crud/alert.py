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
        root_analysis=crud.analysis.create_root(db=db),
        tool=crud.alert_tool.read_by_value(value=model.tool, db=db),
        tool_instance=crud.alert_tool_instance.read_by_value(value=model.tool_instance, db=db),
        type=crud.alert_type.read_by_value(value=model.type, db=db),
        uuid=model.uuid,
    )

    if model.owner is not None:
        obj.owner = crud.user.read_by_username(username=model.owner, db=db)

    db.add(obj)
    db.flush()

    # Associate the root analysis with the submission
    crud.alert_analysis_mapping.create(analysis_uuid=obj.root_analysis_uuid, submission_uuid=obj.uuid, db=db)

    # Associate the root analysis with its observables
    obj.root_analysis.child_observables = [crud.observable.create(model=o, db=db) for o in model.observables]

    # Add an alert history entry if the history username was given. This would typically only be
    # supplied by the GUI when an analyst creates a manual alert.
    if model.history_username is not None:
        crud.history.record_node_create_history(
            record_node=obj,
            action_by=crud.user.read_by_username(username=model.history_username, db=db),
            db=db,
        )

    return obj


def read_by_uuid(uuid: UUID, db: Session) -> Optional[Alert]:
    return db.execute(select(Alert).where(Alert.uuid == uuid)).scalars().one_or_none()


def read_tree(uuid: UUID, db: Session) -> Optional[dict]:
    # The Alert db object has an "analyses" list that contains every analysis object regardless
    # of where it appears in the tree structure.
    db_alert = read_by_uuid(uuid=uuid, db=db)

    if db_alert is not None:
        # The analyses and observables need to be organized in a few dictionaries so that the tree
        # structure can be easily built:
        #
        # Dictionary of analysis objects where their UUID is the key
        # Dictionary of analysis objects where their target observable UUID is the key
        # Dictionary of observables where their UUID is the key
        analyses_by_target: dict[UUID, list[AnalysisNodeTreeRead]] = {}
        analyses_by_uuid: dict[UUID, AnalysisNodeTreeRead] = {}
        child_observables: dict[UUID, ObservableNodeTreeRead] = {}
        for db_analysis in db_alert.analyses:
            # Create an empty list if this target observable UUID has not been seen yet.
            if db_analysis.target_uuid not in analyses_by_target:
                analyses_by_target[db_analysis.target_uuid] = []

            # Add the analysis model to the two analysis dictionaries
            analysis = db_analysis.convert_to_pydantic()
            analyses_by_target[db_analysis.target_uuid].append(analysis)
            analyses_by_uuid[db_analysis.uuid] = analysis

            for db_child_observable in db_analysis.child_observables:
                # Add the observable model to the dictionary if it has not been seen yet.
                if db_child_observable.uuid not in child_observables:
                    child_observables[db_child_observable.uuid] = db_child_observable.convert_to_pydantic()

                # Add the observable as a child to the analysis model.
                analyses_by_uuid[db_analysis.uuid].children.append(child_observables[db_child_observable.uuid])

        # Loop over each overvable and add its analysis as a child
        for observable_uuid, observable in child_observables.items():

            if observable_uuid in analyses_by_target:
                observable.children = analyses_by_target[observable_uuid]

        # Create the AlertTree object and set its children to be the root analysis children.
        alert_tree = AlertTreeRead(**db_alert.__dict__)
        alert_tree.children = analyses_by_uuid[db_alert.root_analysis_uuid].children

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

    return None
