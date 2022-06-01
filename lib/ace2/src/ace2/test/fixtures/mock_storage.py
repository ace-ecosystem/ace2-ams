import os
import pytest
from shutil import copyfile
from ace2.storage import get_storage_id

# monkeypatch storage upload/download for all tests so that it does not call out
@pytest.fixture(autouse=True)
def mock_storage(monkeypatch, tmp_path, datadir):
    def upload(path):
        storage_id = get_storage_id(path)
        copyfile(path, str(tmp_path / storage_id))
        return storage_id

    def download(storage_id):
        for directory in [tmp_path, datadir]:
            if os.path.exists(str(directory / storage_id)):
                return str(directory / storage_id)
        raise FileNotFoundError(storage_id)

    monkeypatch.setattr('ace2.storage.upload', upload)
    monkeypatch.setattr('ace2.storage.download', download)
