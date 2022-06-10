from api_models.submission_tool_instance import SubmissionToolInstanceUpdate
from db import crud
from tests import factory


def test_update(db):
    obj = factory.submission_tool_instance.create_or_read(value="test", db=db)

    assert obj.description is None
    assert obj.value == "test"

    crud.submission_tool_instance.update(
        uuid=obj.uuid,
        model=SubmissionToolInstanceUpdate(description="test description", value="new value"),
        db=db,
    )

    assert obj.description == "test description"
    assert obj.value == "new value"


def test_update_duplicate_value(db):
    obj1 = factory.submission_tool_instance.create_or_read(value="test", db=db)
    obj2 = factory.submission_tool_instance.create_or_read(value="test2", db=db)

    result = crud.submission_tool_instance.update(
        uuid=obj2.uuid, model=SubmissionToolInstanceUpdate(value=obj1.value), db=db
    )
    assert result is False
