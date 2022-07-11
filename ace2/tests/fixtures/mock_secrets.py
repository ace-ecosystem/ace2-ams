import ace2
import pytest

# get secrets from test data file instead of connecting to Secrets Manager
@pytest.fixture(autouse=True)
def mock_secrets(monkeypatch, datadir):
    class MockClient():
        def get_secret_value(self, SecretId):
            with open(str(datadir / f'{SecretId}.json')) as f:
                return {'SecretString': f.read().strip()}

    class MockSession():
        @property
        def region_name(self):
            return 'the universe'

        def client(self, service_name=None, region_name=None):
            assert service_name == 'secretsmanager'
            assert region_name == 'the universe'
            return MockClient()

    monkeypatch.setattr('ace2.secrets.Session', MockSession)
