from ace2 import *

def test_persistent_data():
    assert persistent_data.get('hello') == None
    persistent_data.set('hello', 'world')
    assert persistent_data.get('hello') == 'world'
