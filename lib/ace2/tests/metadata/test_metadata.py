from ace2 import *

def test_metadata():
    # load generic metadata from state
    state = {
        'type': 'foo',
        'value': 'bar',
    }
    metadata = Metadata(**state)
    assert isinstance(metadata, Metadata)
    assert metadata.type == 'foo'
    assert metadata.value == 'bar'
    assert metadata.dict() == state

    # create metadata from constructor
    metadata2 = Metadata('foo', 'bar')
    assert isinstance(metadata2, Metadata)
    assert metadata2.type == 'foo'
    assert metadata2.value == 'bar'
    assert metadata2.dict() == state

    # make sure the two metadata instances are considered equal
    assert metadata == metadata2
