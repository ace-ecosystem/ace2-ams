import pytest

from api_models.alert_disposition import AlertDispositionUpdate
from db import crud
from db.schemas.alert_disposition import AlertDisposition
from tests import factory


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
    result = crud.helpers.update(uuid=obj2.uuid, update_model=update_model, db_table=AlertDisposition, db=db)
    assert result is False
