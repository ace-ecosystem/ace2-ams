from ace2.core.metadata import *

def test_tag():
    # load tag from state
    state = {
        'type': 'tag',
        'value': 'foo',
    }
    metadata = Metadata(**state)
    assert isinstance(metadata, Tag)
    assert metadata.type == 'tag'
    assert metadata.value == 'foo'
    assert metadata.dict() == state

    # create tag
    metadata = Tag('foo')
    assert metadata.type == 'tag'
    assert metadata.value == 'foo'
    assert metadata.dict() == state
