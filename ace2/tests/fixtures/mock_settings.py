import pytest

@pytest.fixture(autouse=True)
def mock_settings(monkeypatch, datadir):
    class MockOpen():
        def __init__(self, path):
            self.path = str(datadir / path)

        def __enter__(self):
            self.file_handle = open(self.path)
            return self.file_handle

        def __exit__(self, *args):
            self.file_handle.close()

    monkeypatch.setattr('ace2.settings.open', MockOpen)
