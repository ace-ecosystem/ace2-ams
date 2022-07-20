from ace2 import *

def test_persistent_data(mock_now):
    # test get/set string
    assert persistent_data.get('hello') == None
    persistent_data.set('hello', 'world')
    assert persistent_data.get('hello') == 'world'

    # test get/set timestamp
    assert persistent_data.get_timestamp('foo', mock_now) == mock_now
    persistent_data.set_timestamp('foo', mock_now)
    assert persistent_data.get_timestamp('foo') == mock_now
