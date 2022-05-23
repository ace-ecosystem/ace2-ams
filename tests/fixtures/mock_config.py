import ace2
import pytest

@pytest.fixture(autouse=True)
def mock_config(monkeypatch, datadir):
    # reset config before each test
    ace2.core.config._config = None

    # patch config path to use test datadir
    monkeypatch.setattr('ace2.core.config._config_path', str(datadir / 'config.yml'))
