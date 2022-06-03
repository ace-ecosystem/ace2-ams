from db import crud
from tests import factory


def test_delete(db):
    obj = factory.alert_disposition.create_or_read(value="test", rank=1, db=db)
    assert crud.alert_disposition.delete(uuid=obj.uuid, db=db) is True


def test_unable_to_delete(db):
    # Create an alert disposition and assign it to an alert/submission object
    obj = factory.alert_disposition.create_or_read(value="test", rank=1, db=db)
    factory.submission.create(alert=True, disposition="test", db=db)

    # You should not be able to delete the alert disposition now that it is in use
    assert crud.alert_disposition.delete(uuid=obj.uuid, db=db) is False
