from ace2.core import config

def test_config():
    assert config.load() == {
        'somedict': {
            'key': {
                'foo': 'bar',
            },
        },
        'somelist': [
            1,
            2,
            3,
        ],
    }

    # add something to the raw_config and load again to make sure that we use the cached version
    config.raw_config['tricky'] = 'hello'
    assert config.load() == {
        'somedict': {
            'key': {
                'foo': 'bar',
            },
        },
        'somelist': [
            1,
            2,
            3,
        ],
        'tricky': 'hello',
    }
