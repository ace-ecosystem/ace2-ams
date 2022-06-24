from db import crud
from tests import factory


def test_delete(db):
    submission = factory.submission.create(db=db)
    observable = factory.observable.create_or_read(
        type="type", value="value", parent_analysis=submission.root_analysis, db=db
    )
    observable2 = factory.observable.create_or_read(
        type="type", value="value2", parent_analysis=submission.root_analysis, db=db
    )
    obj = factory.observable_relationship.create_or_read(
        observable=observable, related_observable=observable2, type="test", db=db
    )

    result = crud.observable_relationship.delete(uuid=obj.uuid, history_username="analyst", db=db)
    assert result is True
