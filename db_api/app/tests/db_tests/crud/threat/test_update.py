from api_models.threat import ThreatUpdate
from db import crud
from tests import factory


def test_update(db):
    queue = factory.queue.create_or_read(value="queue", db=db)
    obj = factory.threat.create_or_read(description="description", value="value", queues=["queue"], db=db)

    assert obj.description == "description"
    assert obj.queues == [queue]
    assert obj.value == "value"

    queue2 = factory.queue.create_or_read(value="queue2", db=db)
    new_threat_type = factory.threat_type.create_or_read(value="new_threat_type", db=db)
    result = crud.threat.update(
        uuid=obj.uuid,
        model=ThreatUpdate(
            description="updated description",
            queues=["queue2"],
            types=["new_threat_type"],
            value="updated value",
        ),
        db=db,
    )
    assert result is True
    assert obj.description == "updated description"
    assert obj.queues == [queue2]
    assert obj.types == [new_threat_type]
    assert obj.value == "updated value"


def test_update_conflicting_value(db):
    factory.threat.create_or_read(value="value", db=db)
    obj2 = factory.threat.create_or_read(value="value2", db=db)

    result = crud.threat.update(uuid=obj2.uuid, model=ThreatUpdate(value="value"), db=db)
    assert result is False
    assert obj2.value == "value2"
