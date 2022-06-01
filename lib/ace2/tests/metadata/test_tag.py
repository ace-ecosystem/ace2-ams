from ace2 import *

def test_tag():
    # load tag from state
    state = {
        'type': 'Tag',
        'value': 'foo',
    }
    metadata = Metadata(**state)
    assert isinstance(metadata, Tag)
    assert metadata.type == 'Tag'
    assert metadata.value == 'foo'
    assert metadata.dict() == state

    # create tag
    metadata = Tag('foo')
    assert metadata.type == 'Tag'
    assert metadata.value == 'foo'
    assert metadata.dict() == state
