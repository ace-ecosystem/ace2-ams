from ace2.core.polymorphism import TypedModel

class Foo(TypedModel):
    pass

class BarBar(Foo):
    pass

def test_typed_model():
    # load Foo from state
    state = {
        'type': 'bar_bar'
    }
    foo = Foo(**state)

    # ensure foo is loaded as instance of BarBar
    assert isinstance(foo, BarBar)

    # ensure that BarBar class has a set type
    assert BarBar.type == 'bar_bar'
