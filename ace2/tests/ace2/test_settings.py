from ace2.settings import Settings

def test_settings(datadir):
    # create a new Settings class
    class MySettings(Settings):
        foo: str

    # load the settings
    settings = MySettings.load('MySettings')
    assert settings.foo == 'bar'

    # test section option
    settings = MySettings.load('MySettings', section='hello')
    assert settings.foo == 'world'
