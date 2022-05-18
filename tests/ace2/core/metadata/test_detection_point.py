from ace2.core.metadata import *

def test_detection_point():
    # load detectionpoint from state
    state = {
        'type': 'detection_point',
        'value': 'foo',
    }
    metadata = Metadata(**state)
    assert isinstance(metadata, DetectionPoint)
    assert metadata.type == 'detection_point'
    assert metadata.value == 'foo'
    assert metadata.dict() == state

    # create detectionpoint
    metadata = DetectionPoint('foo')
    assert metadata.type == 'detection_point'
    assert metadata.value == 'foo'
    assert metadata.dict() == state
