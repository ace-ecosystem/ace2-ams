import pytest

@pytest.fixture(autouse=True)
def mock_settings(monkeypatch, datadir):
    monkeypatch.setattr('ace2.settings.environ', {'ACE2': str(datadir)})
