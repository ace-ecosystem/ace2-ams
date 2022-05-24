from ace2.core.metadata import *

def test_directive():
    # load directive from state
    state = {
        'type': 'Directive',
        'value': 'foo',
    }
    metadata = Metadata(**state)
    assert isinstance(metadata, Directive)
    assert metadata.type == 'Directive'
    assert metadata.value == 'foo'
    assert metadata.dict() == state

    # create directive
    metadata = Directive('foo')
    assert metadata.type == 'Directive'
    assert metadata.value == 'foo'
    assert metadata.dict() == state
