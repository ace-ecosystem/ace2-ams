from ace2.core.config import ConfigMap
from pydantic import BaseModel
from pydantic.error_wrappers import ValidationError
from pytest import raises

def test_config_map():
    # create a new config map class
    class MyMap(ConfigMap):
        pass

    # add new field to config map
    class HelloConfig(BaseModel):
        foo: str = 'bar'
    MyMap.add(HelloConfig)

    # test that default value works
    config = MyMap()
    assert config.Hello.foo == 'bar'

    # test that override works
    d = {
        'Hello': {
            'foo': 'world',
        },
    }
    config = MyMap(**d)
    assert config.Hello.foo == 'world'

    # add a required field to the config map
    class Required(BaseModel):
        hello: str
    MyMap.add(Required)
    
    with raises(ValidationError):
        MyMap(**d)
