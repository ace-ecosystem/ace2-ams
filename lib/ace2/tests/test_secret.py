from ace2.secret import Secret
from pydantic import BaseModel

def test_secret(monkeypatch):
    class MockClient():
        def get_secret_value(self, SecretId=None):
            assert SecretId == 'my_secret_id'
            return { 'SecretString': 'hello world!' }

    class MockSession():
        @property
        def region_name(self):
            return 'the universe'

        def client(self, service_name=None, region_name=None):
            assert service_name == 'secretsmanager'
            assert region_name == 'the universe'
            return MockClient()

    # mock Session
    monkeypatch.setattr('ace2.secret.Session', MockSession)

    # make a class that uses a secret
    class Something(BaseModel):
        password: Secret

    # load the class
    d = { 'password': 'my_secret_id' }
    something = Something(**d)

    # make sure the secret value is what we get out
    assert something.password == 'hello world!'
