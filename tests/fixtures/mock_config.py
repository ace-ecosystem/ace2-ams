import ace2
import pytest

@pytest.fixture(autouse=True)
def mock_config(monkeypatch, datadir):
    # reset raw_config before each test
    ace2.core.config.raw_config = None

    # patch config path to use test datadir
    monkeypatch.setattr('ace2.core.config.path', str(datadir / 'config.yml'))
