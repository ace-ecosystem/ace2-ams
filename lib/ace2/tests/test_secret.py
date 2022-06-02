from ace2.secret import Secret
from pydantic import BaseModel

def test_secret(monkeypatch):
    # make a class that uses a secret
    class Something(BaseModel):
        password: Secret

    # load the class
    d = { 'password': 'my_secret_id' }
    something = Something(**d)

    # make sure the secret value is what we get out
    assert something.password == 'MY_SECRET_ID'
