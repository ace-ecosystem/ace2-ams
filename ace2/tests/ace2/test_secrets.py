from ace2.secrets import get_secret

def test_get_secret():
    assert get_secret('hello') == 'world'
