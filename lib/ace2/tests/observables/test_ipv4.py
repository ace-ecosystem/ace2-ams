from ace2 import *

def test_ipv4():
    # create an observable
    observable = IPv4('127.0.0.1')

    # verify attributes
    assert observable.type == 'IPv4'
    assert observable.value == '127.0.0.1'

    # save then load
    state = observable.dict()
    observable = Observable(**state)

    # verify class instatnce
    assert isinstance(observable, IPv4)
    assert observable.type == 'IPv4'
    assert observable.value == '127.0.0.1'
