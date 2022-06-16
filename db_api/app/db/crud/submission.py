import json

from datetime import datetime
from api_models.summaries import URLDomainSummary
from fastapi.encoders import jsonable_encoder
from sqlalchemy import and_, func, or_, select
from sqlalchemy.orm import Session
from sqlalchemy.sql.selectable import Select
from typing import Optional
from uuid import UUID

from api_models.analysis import AnalysisSubmissionTreeRead
from api_models.observable import ObservableSubmissionTreeRead
from api_models.submission import SubmissionCreate, SubmissionUpdate
from db import crud
from db.schemas.alert_disposition import AlertDisposition
from db.schemas.analysis_child_observable_mapping import analysis_child_observable_mapping
from db.schemas.analysis_metadata import AnalysisMetadata
from db.schemas.event import Event
from db.schemas.metadata_tag import MetadataTag
from db.schemas.node import Node
from db.schemas.node_threat import NodeThreat
from db.schemas.node_threat_actor import NodeThreatActor
from db.schemas.observable import Observable
from db.schemas.observable_type import ObservableType
from db.schemas.queue import Queue
from db.schemas.submission import Submission, SubmissionHistory
from db.schemas.submission_analysis_mapping import submission_analysis_mapping
from db.schemas.submission_tool import SubmissionTool
from db.schemas.submission_tool_instance import SubmissionToolInstance
from db.schemas.submission_type import SubmissionType
from db.schemas.user import User


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
    observable: Optional[list[str]] = None,  # Example: type|value
    observable_types: Optional[list[str]] = None,
    observable_value: Optional[list[str]] = None,
    owner: Optional[list[str]] = None,
    queue: Optional[list[str]] = None,
    sort: Optional[str] = None,  # Example: event_time|desc
    submission_type: Optional[list[str]] = None,
    tags: Optional[list[str]] = None,
    threat_actors: Optional[list[str]] = None,
    threats: Optional[list[str]] = None,
    tool: Optional[list[str]] = None,
    tool_instance: Optional[list[str]] = None,
) -> Select:
    def _join_as_subquery(query: Select, subquery: Select):
        s = subquery.subquery()
        return query.join(s, Submission.uuid == s.c.uuid).group_by(Submission.uuid, Node.uuid)

    def _replace_none(values: list):
        return [None if v.lower() == "none" else v for v in values]

    query = select(Submission)

    if alert:
        alert_query = select(Submission).where(Submission.alert == True)

        query = _join_as_subquery(query, alert_query)

    if disposition:
        disposition_query = (
            select(Submission).join(AlertDisposition).where(AlertDisposition.value.in_(_replace_none(disposition)))
        )

        query = _join_as_subquery(query, disposition_query)

    if disposition_user:
        disposition_user_query = select(Submission).where(
            Submission.history.any(
                and_(
                    SubmissionHistory.field == "disposition",
                    SubmissionHistory.action_by.has(User.username.in_(disposition_user)),
                )
            )
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
        event_uuid_query = (
            select(Submission)
            .join(Event, onclause=Submission.event_uuid == Event.uuid)
            .where(Event.uuid.in_(event_uuid))
        )
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
            .group_by(Submission.uuid, Node.uuid)
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
        owner_query = (
            select(Submission)
            .join(User, onclause=Submission.owner_uuid == User.uuid)
            .where(User.username.in_(_replace_none(owner)))
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
                            Submission.child_permanent_tags.any(MetadataTag.value == tag),
                        )
                    )

                tag_filters.append(and_(*tag_sub_filters))

        tags_query = select(Submission).where(or_(*tag_filters))

        query = _join_as_subquery(query, tags_query)

    if threat_actors:
        threat_actor_filters = []
        for t in threat_actors:
            if t:
                threat_actor_sub_filters = []
                for threat_actor in t.split(","):
                    threat_actor_sub_filters.append(
                        or_(
                            Submission.threat_actors.any(NodeThreatActor.value == threat_actor),
                            Submission.child_threat_actors.any(NodeThreatActor.value == threat_actor),
                        )
                    )

                threat_actor_filters.append(and_(*threat_actor_sub_filters))

        threat_actor_query = select(Submission).where(and_(*threat_actor_filters))

        query = _join_as_subquery(query, threat_actor_query)

    if threats:
        threat_filters = []
        for t in threats:
            if t:
                threat_sub_filters = []
                for threat in t.split(","):
                    threat_sub_filters.append(
                        or_(
                            Submission.threats.any(NodeThreat.value == threat),
                            Submission.child_threats.any(NodeThreat.value == threat),
                        )
                    )

                threat_filters.append(and_(*threat_sub_filters))

        threats_query = select(Submission).where(or_(*threat_filters))

        query = _join_as_subquery(query, threats_query)

    if tool:
        tool_query = select(Submission).join(SubmissionTool).where(SubmissionTool.value.in_(tool))
        query = _join_as_subquery(query, tool_query)

    if tool_instance:
        tool_instance_query = (
            select(Submission).join(SubmissionToolInstance).where(SubmissionToolInstance.value.in_(tool_instance))
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
                Submission.uuid, Node.uuid, User.username
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
                Submission.uuid, Node.uuid, User.username
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
    # Create the new submission Node using the data from the request
    obj: Submission = crud.node.create(
        model=model, db_node_type=Submission, db=db, exclude={"history_username", "observables"}
    )

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
    obj.root_analysis = crud.analysis.create_root(db=db)
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
        crud.history.record_node_create_history(
            record_node=obj,
            action_by=crud.user.read_by_username(username=model.history_username, db=db),
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
    observable: Optional[list[str]] = None,  # Example: type|value
    observable_types: Optional[list[str]] = None,
    observable_value: Optional[list[str]] = None,
    owner: Optional[list[str]] = None,
    queue: Optional[list[str]] = None,
    sort: Optional[str] = None,  # Example: event_time|desc
    submission_type: Optional[list[str]] = None,
    tags: Optional[list[str]] = None,
    threat_actors: Optional[list[str]] = None,
    threats: Optional[list[str]] = None,
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
                observable=observable,  # Example: type|value
                observable_types=observable_types,
                observable_value=observable_value,
                owner=owner,
                queue=queue,
                sort=sort,  # Example: event_time|desc
                submission_type=submission_type,
                tags=tags,
                threat_actors=threat_actors,
                threats=threats,
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
            onclause=submission_analysis_mapping.c.analysis_uuid == analysis_child_observable_mapping.c.analysis_uuid,
        )
        .join(ObservableType, onclause=ObservableType.uuid == Observable.type_uuid)
        .join(
            Submission,
            onclause=and_(Submission.uuid == submission_analysis_mapping.c.submission_uuid, Submission.uuid.in_(uuids)),
        )
    )

    # Organize the observables into a dictionary with their UUIDs as the key
    observables_by_uuid: dict[UUID, Observable] = {o.uuid: o for o in db.execute(query).unique().scalars().all()}

    # Get a list of the analysis metadata added to the observables inside of the given submission UUIDs
    query = select(AnalysisMetadata).join(
        submission_analysis_mapping,
        onclause=and_(
            submission_analysis_mapping.c.analysis_uuid == AnalysisMetadata.analysis_uuid,
            submission_analysis_mapping.c.submission_uuid.in_(uuids),
        ),
    )
    analysis_metadata: list[AnalysisMetadata] = db.execute(query).scalars().all()

    # There are certain types of analysis metadata that we want to inject into the observables.
    # Loop through all of the analysis metadata inject the metadata into the observables.
    metadata_tags_by_observable_uuid: dict[UUID, list[MetadataTag]] = {}

    for metadata in analysis_metadata:
        # Only set the display type if it hasn't been set already
        if (
            not observables_by_uuid[metadata.observable_uuid].display_type
            and metadata.metadata_object.metadata_type == "display_type"
        ):
            observables_by_uuid[metadata.observable_uuid].display_type = metadata.metadata_object

        # Only set the display value if it hasn't been set already
        elif (
            not observables_by_uuid[metadata.observable_uuid].display_value
            and metadata.metadata_object.metadata_type == "display_value"
        ):
            observables_by_uuid[metadata.observable_uuid].display_value = metadata.metadata_object

        elif metadata.metadata_object.metadata_type == "tag":
            if metadata.observable_uuid not in metadata_tags_by_observable_uuid:
                metadata_tags_by_observable_uuid[metadata.observable_uuid] = []

            metadata_tags_by_observable_uuid[metadata.observable_uuid].append(metadata.metadata_object)

    # Inject the analysis tags into the observables
    for observable_uuid in metadata_tags_by_observable_uuid:
        observables_by_uuid[observable_uuid].analysis_tags = sorted(
            set(metadata_tags_by_observable_uuid[observable_uuid]), key=lambda t: t.value
        )

    # Return the list of observables sorted by their type then value
    return sorted(observables_by_uuid.values(), key=lambda o: (o.type.value, o.value))


def read_tree(uuid: UUID, db: Session) -> dict:
    # The Submission db object has an "analyses" list that contains every analysis object regardless
    # of where it appears in the tree structure.
    db_submission = read_by_uuid(uuid=uuid, db=db)

    # The analyses and observables need to be organized in a few dictionaries so that the tree
    # structure can be easily built:
    #
    # Dictionary of analysis objects where their UUID is the key
    # Dictionary of analysis objects where their target observable UUID is the key
    # Dictionary of observables where their UUID is the key
    analyses_by_target: dict[UUID, list[AnalysisSubmissionTreeRead]] = {}
    analyses_by_uuid: dict[UUID, AnalysisSubmissionTreeRead] = {}
    child_observables: dict[UUID, ObservableSubmissionTreeRead] = {}
    for db_analysis in db_submission.analyses:
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

            #
            # METADATA
            #
            # Inject metadata objects added by analysis into the observable model. We could simply add a list
            # of metadata objects to the observable model, but this would require the GUI to perform extra
            # work to display certain kinds of metadata (such as tags).

            # Add any tags added by the analysis to the observable model.
            child_observables[db_child_observable.uuid].analysis_tags += [
                m.metadata_object.convert_to_pydantic()
                for m in db_analysis.analysis_metadata
                if m.metadata_object.metadata_type == "tag" and m.observable_uuid == db_child_observable.uuid
            ]

            # Only set the observable's display type if it hasn't been set already.
            if child_observables[db_child_observable.uuid].display_type is None:
                for m in db_analysis.analysis_metadata:
                    if (
                        m.metadata_object.metadata_type == "display_type"
                        and m.observable_uuid == db_child_observable.uuid
                    ):
                        child_observables[
                            db_child_observable.uuid
                        ].display_type = m.metadata_object.convert_to_pydantic()
                        break

            # Only set the observable's display value if it hasn't been set already.
            if child_observables[db_child_observable.uuid].display_value is None:
                for m in db_analysis.analysis_metadata:
                    if (
                        m.metadata_object.metadata_type == "display_value"
                        and m.observable_uuid == db_child_observable.uuid
                    ):
                        child_observables[
                            db_child_observable.uuid
                        ].display_value = m.metadata_object.convert_to_pydantic()
                        break

            # Add the observable as a child to the analysis model.
            analyses_by_uuid[db_analysis.uuid].children.append(child_observables[db_child_observable.uuid])

    # Loop over each overvable in the submission
    for observable_uuid, observable in child_observables.items():

        #
        # METADATA
        #
        # Dedup the various types of metadata lists that were injected into the observable model.

        observable.analysis_tags = sorted(set(observable.analysis_tags), key=lambda m: m.value)

        # Add its analysis as a child to the observable model.
        if observable_uuid in analyses_by_target:
            observable.children = analyses_by_target[observable_uuid]

    # Create the Submission object to SubmissionTree and set its children to be the root analysis children.
    # The actual root analysis is not included in the tree structure.
    tree = db_submission.convert_to_pydantic()
    tree.children = analyses_by_uuid[db_submission.root_analysis_uuid].children

    # Now that the tree structure is built, we need to walk it to mark which of the leaves have
    # already appeared in the tree. This is useful for when you might not want to display or
    # process a leaf in the tree if it is a duplicate (ex: the GUI auto-collapses duplicate leaves).
    #
    # But before the tree can be traversed, it needs to be serialized into JSON. If an observable or analysis
    # is repeated in the tree, it is just a reference to the same object, so updating its "first_appearance"
    # property would change the value for every instance of the object (which we do not want).
    #
    # Adapted from: https://www.geeksforgeeks.org/preorder-traversal-of-n-ary-tree-without-recursion/
    tree_json: dict = json.loads(tree.json(encoder=jsonable_encoder))
    unique_uuids: set[UUID] = set()
    unvisited = [tree_json]
    while unvisited:
        current = unvisited.pop(0)

        if current["uuid"] in unique_uuids:
            current["first_appearance"] = False
        else:
            current["first_appearance"] = True
            unique_uuids.add(current["uuid"])

        for idx in range(len(current["children"]) - 1, -1, -1):
            unvisited.insert(0, current["children"][idx])

    return tree_json


def read_summary_url_domain(uuid: UUID, db: Session) -> URLDomainSummary:
    # Verify the submission exists
    read_by_uuid(uuid=uuid, db=db)

    observables = read_observables(uuids=[uuid], db=db)
    urls = [observable for observable in observables if observable.type.value == "url"]

    return crud.helpers.read_summary_url_domain(url_observables=urls, db=db)


def update(model: SubmissionUpdate, db: Session):
    # Update the Node attributes
    submission, diffs = crud.node.update(model=model, uuid=model.uuid, db_table=Submission, db=db)

    # Get the data that was given in the request and use it to update the database object
    update_data = model.dict(exclude_unset=True)

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
            crud.node.update_version(node=submission.event, db=db)
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
        crud.history.record_node_update_history(
            record_node=submission,
            action_by=crud.user.read_by_username(username=model.history_username, db=db),
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
        crud.node.update_version(node=submission, db=db)

    db.flush()
