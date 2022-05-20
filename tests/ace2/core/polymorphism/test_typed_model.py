from ace2.core.polymorphism import TypedModel

class Foo(TypedModel):
    pass

class Bar(Foo):
    pass

def test_typed_model():
    # load Foo from state
    state = {
        'type': 'Bar'
    }
    foo = Foo(**state)

    # ensure foo is loaded as instance of Bar
    assert isinstance(foo, Bar)

    # ensure that Bar class has a set type
    assert Bar.type == 'Bar'
