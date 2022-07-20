import json

from uuid import uuid4
from api_models.analysis import AnalysisCreateInObservable
from api_models.observable import ObservableCreate

from api_models.analysis_metadata import AnalysisMetadataCreate
from api_models.submission import SubmissionCreate
from db import crud
from tests import factory


def test_create(db):
    # Create the various objects to link to the submission
    analysis_module_type = factory.analysis_module_type.create_or_read(value="module", db=db)
    factory.metadata_tag.create_or_read(value="tag", db=db)
    factory.metadata_tag.create_or_read(value="o_analysis_tag", db=db)
    factory.metadata_tag.create_or_read(value="o_tag", db=db)
    factory.observable_type.create_or_read(value="type", db=db)
    factory.queue.create_or_read(value="queue", db=db)
    factory.submission_tool.create_or_read(value="tool", db=db)
    factory.submission_tool_instance.create_or_read(value="tool_instance", db=db)
    factory.submission_type.create_or_read(value="type", db=db)

    # Create the submission
    now = crud.helpers.utcnow()
    submission_uuid = uuid4()
    submission = crud.submission.create_or_read(
        model=SubmissionCreate(
            alert=True,
            description="description",
            details=json.dumps({"foo": "bar"}),
            event_time=now,
            history_username="analyst",
            insert_time=now,
            instructions="instructions",
            name="name",
            observables=[
                ObservableCreate(
                    type="type",
                    value="value",
                    analyses=[
                        AnalysisCreateInObservable(
                            analysis_module_type_uuid=analysis_module_type.uuid, submission_uuid=submission_uuid
                        )
                    ],
                    analysis_metadata=[
                        AnalysisMetadataCreate(type="critical_point", value="o_critical_point"),
                        AnalysisMetadataCreate(type="detection_point", value="o_detection_point"),
                        AnalysisMetadataCreate(type="directive", value="o_analysis_directive"),
                        AnalysisMetadataCreate(type="tag", value="o_analysis_tag"),
                    ],
                    detection_points=["detection_point"],
                    tags=["o_tag"],
                )
            ],
            owner="analyst",
            queue="queue",
            tags=["tag"],
            tool="tool",
            tool_instance="tool_instance",
            type="type",
            uuid=submission_uuid,
        ),
        db=db,
    )

    assert submission.alert is True
    assert len(submission.analyses) == 2
    assert any(a.analysis_module_type_uuid is None for a in submission.analyses)
    assert any(a.analysis_module_type_uuid == analysis_module_type.uuid for a in submission.analyses)
    assert len(submission.child_detection_points) == 1
    assert submission.child_detection_points[0].value == "o_detection_point"
    assert len(submission.child_analysis_tags) == 1
    assert submission.child_analysis_tags[0].value == "o_analysis_tag"
    assert len(submission.child_tags) == 1
    assert submission.child_tags[0].value == "o_tag"
    assert submission.description == "description"
    assert submission.event_time == now
    assert len(submission.history) == 1
    assert submission.history[0].action == "CREATE"
    assert submission.insert_time == now
    assert submission.instructions == "instructions"
    assert submission.name == "name"
    assert submission.owner.username == "analyst"
    assert submission.queue.value == "queue"
    assert submission.root_analysis.details == {"foo": "bar"}
    assert len(submission.tags) == 1
    assert submission.tags[0].value == "tag"
    assert submission.tool.value == "tool"
    assert submission.tool_instance.value == "tool_instance"
    assert submission.type.value == "type"
    assert submission.uuid == submission_uuid


def test_create_duplicate_uuid(db):
    factory.queue.create_or_read(value="queue", db=db)
    factory.submission_type.create_or_read(value="type", db=db)

    submission1 = crud.submission.create_or_read(model=SubmissionCreate(queue="queue", type="type", name="name"), db=db)
    submission2 = crud.submission.create_or_read(
        model=SubmissionCreate(queue="queue", type="type", name="name2", uuid=submission1.uuid), db=db
    )
    assert submission2 == submission1
