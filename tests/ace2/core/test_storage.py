from ace2.core.storage import upload, download
from shutil import copyfile

def test_storage(monkeypatch, datadir, tmp_path):
    # patch client with a mock client class
    class mock_client():
        def __init__(self, service):
            assert service == 's3'

        def upload_file(self, path, bucket, storage_id):
            assert bucket == 'bucket'
            copyfile(path, tmp_path / storage_id)

        def download_file(self, bucket, storage_id, path):
            assert bucket == 'bucket'
            copyfile(datadir / storage_id, tmp_path / path)
    monkeypatch.setattr('ace2.storage.client', mock_client)
    monkeypatch.setattr('os.environ', { 'FILE_STORAGE_BUCKET': 'bucket' })

    # test upload
    storage_id = upload(datadir / 'hello.txt')
    assert storage_id == 'a948904f2f0f479b8f8197694b30184b0d2ed1c1cd2a1ec0fb85d299a192a447'
    with open(tmp_path / storage_id) as f:
        assert f.read() == 'hello world\n'

    # test download
    path = download('hello.txt')
    assert path == 'hello.txt'
    with open(tmp_path / storage_id) as f:
        assert f.read() == 'hello world\n'
