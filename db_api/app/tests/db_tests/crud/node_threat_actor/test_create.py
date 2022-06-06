from api_models.node_threat_actor import NodeThreatActorCreate
from db import crud
from tests import factory


def test_create(db):
    queue = factory.queue.create_or_read(value="test_queue", db=db)

    obj = crud.node_threat_actor.create_or_read(
        model=NodeThreatActorCreate(description="test description", value="test", queues=["test_queue"]),
        db=db,
    )

    assert obj.description == "test description"
    assert obj.queues == [queue]
    assert obj.value == "test"


def test_create_duplicate(db):
    obj = crud.node_threat_actor.create_or_read(model=NodeThreatActorCreate(value="test", queues=["external"]), db=db)
    obj2 = crud.node_threat_actor.create_or_read(model=NodeThreatActorCreate(value="test", queues=["external"]), db=db)

    assert obj2.uuid == obj.uuid
