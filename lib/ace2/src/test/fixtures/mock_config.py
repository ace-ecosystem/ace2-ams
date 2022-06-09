import pytest

@pytest.fixture(autouse=True)
def mock_config(monkeypatch, datadir):
    monkeypatch.setattr('ace2.config.DIR', str(datadir))
