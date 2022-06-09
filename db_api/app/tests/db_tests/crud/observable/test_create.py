import pytest

from uuid import uuid4

from api_models.analysis import AnalysisCreateInObservable
from api_models.observable import ObservableCreate, ObservableRelationshipCreate
from db import crud
from exceptions.db import UuidNotFoundInDatabase, ValueNotFoundInDatabase
from tests import factory


#
# INVALID TESTS
#


def test_create_nonexistent_analysis_module_type(db):
    submission = factory.submission.create(db=db)
    factory.observable_type.create_or_read(value="test", db=db)

    with pytest.raises(UuidNotFoundInDatabase):
        crud.observable.create_or_read(
            model=ObservableCreate(
                type="test",
                value="test",
                parent_analysis_uuid=submission.root_analysis_uuid,
                analyses=[
                    AnalysisCreateInObservable(analysis_module_type_uuid=uuid4(), submission_uuid=submission.uuid)
                ],
            ),
            db=db,
        )


def test_create_nonexistent_history_username(db):
    submission = factory.submission.create(db=db)
    factory.observable_type.create_or_read(value="test", db=db)

    with pytest.raises(ValueNotFoundInDatabase):
        crud.observable.create_or_read(
            model=ObservableCreate(
                type="test", value="test", parent_analysis_uuid=submission.root_analysis_uuid, history_username="asdf"
            ),
            db=db,
        )


def test_create_nonexistent_node_directive(db):
    submission = factory.submission.create(db=db)
    factory.observable_type.create_or_read(value="test", db=db)

    with pytest.raises(ValueNotFoundInDatabase):
        crud.observable.create_or_read(
            model=ObservableCreate(
                type="test", value="test", parent_analysis_uuid=submission.root_analysis_uuid, directives=["asdf"]
            ),
            db=db,
        )


def test_create_nonexistent_tag(db):
    submission = factory.submission.create(db=db)
    factory.observable_type.create_or_read(value="test", db=db)

    with pytest.raises(ValueNotFoundInDatabase):
        crud.observable.create_or_read(
            model=ObservableCreate(
                type="test", value="test", parent_analysis_uuid=submission.root_analysis_uuid, permanent_tags=["asdf"]
            ),
            db=db,
        )


def test_create_nonexistent_node_threat_actors(db):
    submission = factory.submission.create(db=db)
    factory.observable_type.create_or_read(value="test", db=db)

    with pytest.raises(ValueNotFoundInDatabase):
        crud.observable.create_or_read(
            model=ObservableCreate(
                type="test", value="test", parent_analysis_uuid=submission.root_analysis_uuid, threat_actors=["asdf"]
            ),
            db=db,
        )


def test_create_nonexistent_node_threats(db):
    submission = factory.submission.create(db=db)
    factory.observable_type.create_or_read(value="test", db=db)

    with pytest.raises(ValueNotFoundInDatabase):
        crud.observable.create_or_read(
            model=ObservableCreate(
                type="test", value="test", parent_analysis_uuid=submission.root_analysis_uuid, threats=["asdf"]
            ),
            db=db,
        )


def test_create_nonexistent_observable_type(db):
    submission = factory.submission.create(db=db)

    with pytest.raises(ValueNotFoundInDatabase):
        crud.observable.create_or_read(
            model=ObservableCreate(type="test", value="test", parent_analysis_uuid=submission.root_analysis_uuid), db=db
        )


def test_create_nonexistent_parent_analysis_uuid(db):
    factory.observable_type.create_or_read(value="test", db=db)

    with pytest.raises(UuidNotFoundInDatabase):
        crud.observable.create_or_read(
            model=ObservableCreate(type="test", value="test", parent_analysis_uuid=uuid4()),
            db=db,
        )


def test_create_nonexistent_relationship_observable(db):
    submission = factory.submission.create(db=db)
    factory.observable_type.create_or_read(value="test", db=db)
    factory.node_relationship_type.create_or_read(value="asdf", db=db)

    with pytest.raises(ValueNotFoundInDatabase):
        crud.observable.create_or_read(
            model=ObservableCreate(
                type="test",
                value="test2",
                parent_analysis_uuid=submission.root_analysis_uuid,
                observable_relationships=[
                    ObservableRelationshipCreate(relationship_type="asdf", type="test", value="test")
                ],
            ),
            db=db,
        )


def test_create_nonexistent_relationship_type(db):
    submission = factory.submission.create(db=db)
    factory.observable_type.create_or_read(value="test", db=db)
    factory.observable.create_or_read(type="test", value="test", parent_analysis=submission.root_analysis, db=db)

    with pytest.raises(ValueNotFoundInDatabase):
        crud.observable.create_or_read(
            model=ObservableCreate(
                type="test",
                value="test2",
                parent_analysis_uuid=submission.root_analysis_uuid,
                observable_relationships=[
                    ObservableRelationshipCreate(relationship_type="asdf", type="test", value="test")
                ],
            ),
            db=db,
        )


#
# VALID TESTS
#


def test_create(db):
    analysis_module_type = factory.analysis_module_type.create_or_read(value="module", db=db)
    now = crud.helpers.utcnow()
    submission = factory.submission.create(db=db)
    initial_submission_version = submission.version
    factory.node_directive.create_or_read(value="directive", db=db)
    factory.node_relationship_type.create_or_read(value="relationship_type", db=db)
    factory.tag.create_or_read(value="tag", db=db)
    factory.node_threat_actor.create_or_read(value="threat_actor", db=db)
    factory.node_threat.create_or_read(value="threat", db=db)
    factory.observable.create_or_read(type="type2", value="value2", parent_analysis=submission.root_analysis, db=db)
    factory.observable_type.create_or_read(value="type1", db=db)
    factory.observable_type.create_or_read(value="type3", db=db)

    observable = crud.observable.create_or_read(
        model=ObservableCreate(
            analyses=[
                AnalysisCreateInObservable(
                    analysis_module_type_uuid=analysis_module_type.uuid, submission_uuid=submission.uuid
                )
            ],
            context="context",
            detection_points=["detection_point"],
            directives=["directive"],
            expires_on=now,
            for_detection=True,
            history_username="analyst",
            observable_relationships=[
                ObservableRelationshipCreate(relationship_type="relationship_type", type="type2", value="value2")
            ],
            redirection=ObservableCreate(
                type="type3", value="value3", parent_analysis_uuid=submission.root_analysis_uuid
            ),
            permanent_tags=["tag"],
            threat_actors=["threat_actor"],
            threats=["threat"],
            time=now,
            type="type1",
            value="test",
            parent_analysis_uuid=submission.root_analysis_uuid,
        ),
        db=db,
    )

    assert observable.context == "context"
    assert len(observable.detection_points) == 1
    assert observable.detection_points[0].value == "detection_point"
    assert len(observable.directives) == 1
    assert observable.directives[0].value == "directive"
    assert observable.expires_on == now
    assert observable.for_detection is True
    # There should be three history records: one for creating the observable, one for updating the detection points,
    # and one for updating the observable relationships.
    assert len(observable.history) == 3
    assert len(observable.observable_relationships) == 1
    assert observable.observable_relationships[0].related_node.type.value == "type2"
    assert observable.observable_relationships[0].related_node.value == "value2"
    assert observable.redirection.type.value == "type3"
    assert observable.redirection.value == "value3"
    assert len(observable.tags) == 1
    assert observable.tags[0].value == "tag"
    assert len(observable.threat_actors) == 1
    assert observable.threat_actors[0].value == "threat_actor"
    assert len(observable.threats) == 1
    assert observable.threats[0].value == "threat"
    assert observable.time == now
    assert observable.type.value == "type1"
    assert observable.value == "test"
    assert submission.version != initial_submission_version


def test_create_duplicate(db):
    submission = factory.submission.create(db=db)
    factory.observable_type.create_or_read(value="type", db=db)

    observable = crud.observable.create_or_read(
        model=ObservableCreate(type="type", value="test", parent_analysis_uuid=submission.root_analysis_uuid),
        db=db,
    )

    observable2 = crud.observable.create_or_read(
        model=ObservableCreate(type="type", value="test", parent_analysis_uuid=submission.root_analysis_uuid),
        db=db,
    )

    assert observable2.uuid == observable.uuid
