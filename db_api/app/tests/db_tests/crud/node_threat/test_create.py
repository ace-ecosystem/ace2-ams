from api_models.node_threat import NodeThreatCreate
from db import crud
from tests import factory


def test_create(db):
    queue = factory.queue.create_or_read(value="test_queue", db=db)
    threat_type = factory.node_threat_type.create_or_read(value="test_threat_type", db=db)

    obj = crud.node_threat.create_or_read(
        model=NodeThreatCreate(
            description="test description", types=["test_threat_type"], value="test", queues=["test_queue"]
        ),
        db=db,
    )

    assert obj.description == "test description"
    assert obj.queues == [queue]
    assert obj.types == [threat_type]
    assert obj.value == "test"


def test_create_duplicate(db):
    factory.node_threat_type.create_or_read(value="test_threat_type", db=db)

    obj = crud.node_threat.create_or_read(
        model=NodeThreatCreate(types=["test_threat_type"], value="test", queues=["external"]), db=db
    )
    obj2 = crud.node_threat.create_or_read(
        model=NodeThreatCreate(types=["test_threat_type"], value="test", queues=["external"]), db=db
    )

    assert obj2.uuid == obj.uuid
