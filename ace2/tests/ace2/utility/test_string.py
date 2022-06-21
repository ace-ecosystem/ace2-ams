from ace2.utility import camel_to_snake
import pytest

@pytest.mark.parametrize('value, expected', [
    ('Hello', 'hello'),
    ('HelloWorld', 'hello_world'),
    ('HElloWorld', 'hello_world'),
])
def test_camel_to_snake(value, expected):
    assert camel_to_snake(value) == expected
