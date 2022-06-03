import pytest

from api_models.alert_disposition import AlertDispositionUpdate
from db import crud
from tests import factory


def test_update(db):
    obj = factory.alert_disposition.create_or_read(value="test", rank=1, db=db)

    assert obj.description is None
    assert obj.rank == 1
    assert obj.value == "test"

    crud.alert_disposition.update(
        uuid=obj.uuid,
        model=AlertDispositionUpdate(description="test description", rank=2, value="new value"),
        db=db,
    )

    assert obj.description == "test description"
    assert obj.rank == 2
    assert obj.value == "new value"


@pytest.mark.parametrize(
    "key",
    [
        ("rank"),
        ("value"),
    ],
)
def test_update_duplicate_unique_fields(db, key):
    # Create some objects
    obj1 = factory.alert_disposition.create_or_read(value="test", rank=1, db=db)
    obj2 = factory.alert_disposition.create_or_read(value="test2", rank=2, db=db)

    # Ensure you cannot update a unique field to a value that already exists
    update_model = AlertDispositionUpdate()
    setattr(update_model, key, getattr(obj1, key))
    result = crud.alert_disposition.update(uuid=obj2.uuid, model=update_model, db=db)
    assert result is False
