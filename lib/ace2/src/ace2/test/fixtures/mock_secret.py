import ace2
import pytest

# mock secret to prevent needing to connect to aws secret manager
@pytest.fixture(autouse=True)
def mock_secret(monkeypatch):
    class MockClient():
        def get_secret_value(self, SecretId=None):
            return { 'SecretString': SecretId.upper() }

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
