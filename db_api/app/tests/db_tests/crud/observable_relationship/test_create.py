from api_models.observable_relationship import ObservableRelationshipCreate
from db import crud
from tests import factory


def test_create(db):
    submission = factory.submission.create(db=db)
    observable = factory.observable.create_or_read(
        type="type", value="value", parent_analysis=submission.root_analysis, db=db
    )
    observable2 = factory.observable.create_or_read(
        type="type", value="value2", parent_analysis=submission.root_analysis, db=db
    )
    factory.observable_relationship_type.create_or_read(value="test", db=db)

    obj = crud.observable_relationship.create_or_read(
        model=ObservableRelationshipCreate(
            observable_uuid=observable.uuid,
            history_username="analyst",
            related_observable_uuid=observable2.uuid,
            type="test",
        ),
        db=db,
    )

    assert obj.observable == observable
    assert obj.related_observable == observable2
    assert obj.type.value == "test"


def test_create_duplicate(db):
    submission = factory.submission.create(db=db)
    observable = factory.observable.create_or_read(
        type="type", value="value", parent_analysis=submission.root_analysis, db=db
    )
    observable2 = factory.observable.create_or_read(
        type="type", value="value2", parent_analysis=submission.root_analysis, db=db
    )
    factory.observable_relationship_type.create_or_read(value="test", db=db)

    obj = crud.observable_relationship.create_or_read(
        model=ObservableRelationshipCreate(
            observable_uuid=observable.uuid,
            history_username="analyst",
            related_observable_uuid=observable2.uuid,
            type="test",
        ),
        db=db,
    )

    obj2 = crud.observable_relationship.create_or_read(
        model=ObservableRelationshipCreate(
            observable_uuid=observable.uuid,
            history_username="analyst",
            related_observable_uuid=observable2.uuid,
            type="test",
        ),
        db=db,
    )

    assert obj2.uuid == obj.uuid
