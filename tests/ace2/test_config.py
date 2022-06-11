from ace2.config import Config

def test_config(datadir):
    # create a new config class
    class MyConfig(Config):
        foo: str

    # load the config
    config = MyConfig.load('MyConfig')
    assert config.foo == 'bar'

    # test section option
    config = MyConfig.load('MyConfig', section='hello')
    assert config.foo == 'world'
