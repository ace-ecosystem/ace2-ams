import json

from datetime import datetime
from sqlalchemy.orm import Session
from typing import Optional, Union
from uuid import UUID, uuid4

from api_models.analysis import AnalysisCreateInObservable
from api_models.observable import ObservableCreate, ObservableCreateInSubmission
from api_models.submission import SubmissionCreate
from api_models.alert_disposition import AlertDispositionCreate
from db import crud
from db.schemas.event import Event
from db.schemas.submission import Submission
from tests import factory


def create(
    db: Session,
    alert: bool = False,
    alert_queue: str = "external",
    submission_type: str = "test_type",
    submission_uuid: Optional[Union[str, UUID]] = None,
    disposition: Optional[str] = None,
    event: Optional[Event] = None,
    event_time: datetime = None,
    history_username: Optional[str] = None,
    insert_time: datetime = None,
    name: str = "Test Alert",
    observables: Optional[list[ObservableCreateInSubmission]] = None,
    owner: Optional[str] = None,
    tags: Optional[list[str]] = None,
    threat_actors: Optional[list[str]] = None,
    threats: Optional[list[str]] = None,
    tool: str = "test_tool",
    tool_instance: str = "test_tool_instance",
    update_time: Optional[datetime] = None,
    updated_by_user: str = "analyst",
):
    diffs = []

    # Set default values
    if submission_uuid is None:
        submission_uuid = uuid4()

    if event_time is None:
        event_time = crud.helpers.utcnow()

    if insert_time is None:
        insert_time = crud.helpers.utcnow()

    if observables is None:
        observables = []

    # Create the alert queue
    factory.queue.create_or_read(value=alert_queue, db=db)

    # Create the submission type
    factory.submission_type.create_or_read(value=submission_type, db=db)

    # Create the tool and tool instance
    factory.submission_tool.create_or_read(value=tool, db=db)
    factory.submission_tool_instance.create_or_read(value=tool_instance, db=db)

    # Create the history user if one was given
    if history_username is not None:
        factory.user.create_or_read(username=history_username, db=db)

    # Create the owner user if one was given
    if owner is not None:
        factory.user.create_or_read(username=owner, alert_queue=alert_queue, db=db)

    # Create the actual submission
    submission = crud.submission.create_or_read(
        model=SubmissionCreate(
            alert=alert,
            event_time=event_time,
            insert_time=insert_time,
            history_username=history_username,
            name=name,
            owner=owner,
            queue=alert_queue,
            tool=tool,
            tool_instance=tool_instance,
            type=submission_type,
            uuid=submission_uuid,
        ),
        db=db,
    )

    if update_time is None:
        update_time = crud.helpers.utcnow()

    if owner is not None:
        diffs.append(crud.history.create_diff(field="owner", old=None, new=owner))

    # Add the observables to the submission
    for observable in observables:
        factory.observable_type.create_or_read(value=observable.type, db=db)
        submission.root_analysis.child_observables.append(
            crud.observable.create_or_read(
                model=ObservableCreate(
                    analyses=observable.analyses,
                    context=observable.context,
                    detection_points=observable.detection_points,
                    expires_on=observable.expires_on,
                    for_detction=observable.for_detection,
                    history_username=observable.history_username,
                    observable_relationships=observable.observable_relationships,
                    parent_analysis_uuid=submission.root_analysis_uuid,
                    tags=observable.tags,
                    threat_actors=observable.threat_actors,
                    threats=observable.threats,
                    type=observable.type,
                    value=observable.value,
                ),
                db=db,
            )
        )

    if disposition:
        existing_dispositions = crud.alert_disposition.read_all(db=db)
        submission.disposition = crud.alert_disposition.create_or_read(
            model=AlertDispositionCreate(value=disposition, rank=len(existing_dispositions) + 1), db=db
        )
        submission.disposition_time = update_time
        submission.disposition_user = factory.user.create_or_read(
            username=updated_by_user, display_name=updated_by_user, db=db
        )
        diffs.append(crud.history.create_diff(field="disposition", old=None, new=disposition))

    if event:
        submission.event = event
        diffs.append(crud.history.create_diff(field="event_uuid", old=None, new=event.uuid))

    if tags:
        submission.tags = [factory.metadata_tag.create_or_read(value=t, db=db) for t in tags]

    if threat_actors:
        submission.threat_actors = [factory.node_threat_actor.create_or_read(value=t, db=db) for t in threat_actors]

    if threats:
        submission.threats = [factory.node_threat.create_or_read(value=threat, db=db) for threat in threats]

    if history_username and diffs and updated_by_user:
        crud.history.record_node_update_history(
            record_node=submission,
            action_by=factory.user.create_or_read(username=updated_by_user, db=db),
            action_time=update_time,
            diffs=diffs,
            db=db,
        )

    db.commit()
    return submission


def create_from_json_file(db: Session, json_path: str, submission_name: str) -> Submission:
    def _build_observable_model(o: dict, submission_uuid: UUID) -> ObservableCreate:
        """Helper function used to construct an ObservableCreate model with child AnalysisCreate models.

        Args:
            o: The observable dictionary from the submission JSON file.
            submission_uuid: The UUID of the submission (alert) containing the observable.

        Returns:
            An ObservableCreate model
        """
        # Make sure the observable type exists
        factory.observable_type.create_or_read(value=o["type"], db=db)

        # Make sure that any relationships the observable has exist
        if "observable_relationships" in o:
            for relationship in o["observable_relationships"]:
                factory.node_relationship_type.create_or_read(value=relationship["type"], db=db)

        # Make sure that any permanent tags the observable has exist
        if "tags" in o:
            for tag in o["tags"]:
                factory.metadata_tag.create_or_read(value=tag, db=db)

        # Build the ObservableCreate model
        observable_model = ObservableCreate(
            analysis_metadata=o.get("metadata", []),
            detection_points=o.get("detection_points", []),
            for_detection=o.get("for_detection", False),
            observable_relationships=o.get("observable_relationships", []),
            tags=o.get("tags", []),
            type=o["type"],
            value=o["value"],
        )

        # If the observable in the JSON file has any child analyses, build AnalysisCreate models
        # and add them to the ObservableCreate model. This is what creates the recursive tree structure.
        if "analyses" in o:
            for a in o["analyses"]:
                # Create the analysis module type object
                analysis_module_type = factory.analysis_module_type.create_or_read(
                    value=a["type"],
                    observable_types=a.get("observable_types", None),
                    required_directives=a.get("required_directives", None),
                    required_tags=a.get("required_tags", None),
                    db=db,
                )

                # Build the AnalysisCreate model and add it to the ObservableCreate model's list of analyses
                observable_model.analyses.append(
                    AnalysisCreateInObservable(
                        analysis_module_type_uuid=analysis_module_type.uuid,
                        child_observables=[
                            _build_observable_model(o=co, submission_uuid=submission_uuid) for co in a["observables"]
                        ]
                        if "observables" in a
                        else [],
                        details=json.dumps(a["details"]) if "details" in a else None,
                        submission_uuid=submission_uuid,
                    )
                )

        return observable_model

    def _replace_tokens(text: str, token: str, base_replacement_string: str) -> str:
        for i in range(text.count(token)):
            text = text.replace(token, f"{base_replacement_string}{i}", 1)

        return text

    with open(json_path) as f:
        text = f.read()

        text = text.replace("<ALERT_NAME>", submission_name)
        text = _replace_tokens(text, "<A_TYPE>", "a_type")
        text = _replace_tokens(text, "<O_TYPE>", "o_type")
        text = _replace_tokens(text, "<O_VALUE>", "o_value")
        text = _replace_tokens(text, "<TAG>", "tag")

        data: dict = json.loads(text)

    # Create the submission object
    submission = create(
        db=db,
        alert=True,
        submission_uuid=data.get("submission_uuid", uuid4()),
        name=data.get("name", "Test Alert"),
        owner=data.get("owner", None),
        updated_by_user=data.get("disposition_user", None) or data.get("owner", None) or "analyst",
    )

    # Build all of the ObservableCreate models
    observable_create_models = [
        _build_observable_model(o=o, submission_uuid=submission.uuid) for o in data["observables"]
    ]

    # Create all of the observables using the submission's root analysis as the parent analysis
    for model in observable_create_models:
        crud.observable.create_or_read(model=model, parent_analysis=submission.root_analysis, db=db)

    db.commit()

    return submission


def stringify_submission_tree(submission_tree: dict):
    def _stringify_children(children: list[dict], depth=0, string=""):
        for child in children:
            duplicate = "" if child["first_appearance"] else " (Duplicate)"
            if child["node_type"] == "observable":
                string += f"{' '*depth}{child['type']['value']}: {child['value']}{duplicate}\n"
                if child["children"]:
                    string = _stringify_children(children=child["children"], depth=depth + 2, string=string)
            if child["node_type"] == "analysis":
                string += f"{' '*depth}{child['analysis_module_type']['value']}{duplicate}\n"
                if child["children"]:
                    string = _stringify_children(children=child["children"], depth=depth + 2, string=string)

        return string

    return _stringify_children(children=submission_tree["children"])
