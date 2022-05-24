from ace2.core.models import TypedModel, PrivateModel

def test_typed_model():
    class Foo(TypedModel):
        pass

    class Bar(Foo):
        pass

    # load Foo from state
    state = {
        'type': 'Bar'
    }
    foo = Foo(**state)

    # ensure foo is loaded as instance of Bar
    assert isinstance(foo, Bar)

    # ensure foo is subclass of PrivateModel
    assert isinstance(foo, Bar)

    # ensure that Bar class has a set type
    assert Bar.type == 'Bar'

def test_private_model():
    # init a private model
    foo = PrivateModel()

    # ensure that getting missing attributes returns None
    assert foo.private.bar is None

    # make sure we can set attributes
    foo.private.bar = 'test'
    assert foo.private.bar == 'test'

    # make sure our private attribute doesnt show up in the dict
    assert foo.dict() == {}
