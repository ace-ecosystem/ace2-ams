from api_models.node_directive import NodeDirectiveCreate
from db import crud


def test_create(db):
    obj = crud.node_directive.create_or_read(
        model=NodeDirectiveCreate(description="test description", value="test value"), db=db
    )

    assert obj.description == "test description"
    assert obj.value == "test value"


def test_create_duplicate_value(db):
    obj1 = crud.node_directive.create_or_read(model=NodeDirectiveCreate(value="test"), db=db)
    assert obj1

    # Ensure that you get the same object back if you try to create a duplicate value
    obj2 = crud.node_directive.create_or_read(model=NodeDirectiveCreate(value=obj1.value), db=db)
    assert obj2.description == obj1.description
    assert obj2.uuid == obj1.uuid
    assert obj2.value == obj1.value
