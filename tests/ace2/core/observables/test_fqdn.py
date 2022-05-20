from ace2.core.observables import *

def test_fqdn():
    # create an observable
    observable = FQDN('www.google.com')

    # verify attributes
    assert observable.type == 'FQDN'
    assert observable.value == 'www.google.com'

    # save then load
    state = observable.dict()
    observable = Observable(**state)

    # verify class instatnce
    assert isinstance(observable, FQDN)
    assert observable.type == 'FQDN'
    assert observable.value == 'www.google.com'
