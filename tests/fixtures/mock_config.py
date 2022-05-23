import ace2
import pytest

@pytest.fixture(autouse=True)
def mock_config(monkeypatch, datadir):
    monkeypatch.setattr('ace2.core.config._config_path', str(datadir / 'config.yml'))
