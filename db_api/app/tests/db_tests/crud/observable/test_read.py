from db import crud
from tests import factory


def test_read_all(db):
    submission = factory.submission.create(db=db)
    obs1 = factory.observable.create_or_read(
        type="type", value="value", parent_analysis=submission.root_analysis, db=db
    )
    obs2 = factory.observable.create_or_read(
        type="type2", value="value2", parent_analysis=submission.root_analysis, db=db
    )
    assert crud.observable.read_all(db=db) == [obs1, obs2]


def test_read_all_history(db):
    submission = factory.submission.create(db=db)
    observable = factory.observable.create_or_read(
        type="type", value="value", parent_analysis=submission.root_analysis, history_username="analyst", db=db
    )
    result = crud.observable.read_all_history(uuid=observable.uuid, db=db)
    assert len(result) == 1
    assert result[0].action == "CREATE"
