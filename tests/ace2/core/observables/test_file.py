from ace2.core.observables import *

def test_file(datadir):
    # create an observable
    observable = File(str(datadir / 'hello.txt'))

    # verify attributes
    assert observable.type == 'File'
    assert observable.value == 'a948904f2f0f479b8f8197694b30184b0d2ed1c1cd2a1ec0fb85d299a192a447'
    assert observable.display_value == 'hello.txt'
    assert observable.path == str(datadir / 'hello.txt')
    assert observable.extension == 'txt'

    # save then load
    state = observable.dict()
    assert state == {
        'type': 'File',
        'value': 'a948904f2f0f479b8f8197694b30184b0d2ed1c1cd2a1ec0fb85d299a192a447',
        'metadata': [
            {
                'type': 'DisplayValue',
                'value': 'hello.txt'
            },
        ],
    }
    observable = Observable(**state)

    # verify attributes
    assert isinstance(observable, File)
    assert observable.type == 'File'
    assert observable.value == 'a948904f2f0f479b8f8197694b30184b0d2ed1c1cd2a1ec0fb85d299a192a447'
    assert observable.display_value == 'hello.txt'
    assert observable.extension == 'txt'
    with open(observable.path) as f:
        assert f.read() == 'hello world\n'

    # test uppercase extension
    state = {
        'type': 'File',
        'value': 'a948904f2f0f479b8f8197694b30184b0d2ed1c1cd2a1ec0fb85d299a192a447',
        'metadata': [
            {
                'type': 'DisplayValue',
                'value': 'hello.TXT'
            },
        ],
    }
    assert Observable(**state).extension == 'txt'

    # test empty extension
    state = {
        'type': 'File',
        'value': 'a948904f2f0f479b8f8197694b30184b0d2ed1c1cd2a1ec0fb85d299a192a447',
        'metadata': [
            {
                'type': 'DisplayValue',
                'value': 'hello.'
            },
        ],
    }
    assert Observable(**state).extension == None

    # test missing extension
    state = {
        'type': 'File',
        'value': 'a948904f2f0f479b8f8197694b30184b0d2ed1c1cd2a1ec0fb85d299a192a447',
        'metadata': [
            {
                'type': 'DisplayValue',
                'value': 'hello'
            },
        ],
    }
    assert Observable(**state).extension == None
