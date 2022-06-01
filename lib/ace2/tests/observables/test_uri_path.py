from ace2 import *

def test_uri_path():
    # create an observable
    observable = UriPath('/yada/yada/yada')

    # verify attributes
    assert observable.type == 'UriPath'
    assert observable.value == '/yada/yada/yada'

    # save then load
    state = observable.dict()
    observable = Observable(**state)

    # verify class instatnce
    assert isinstance(observable, UriPath)
    assert observable.type == 'UriPath'
    assert observable.value == '/yada/yada/yada'
