from ace2.storage import upload, download
from shutil import copyfile

def test_storage(monkeypatch, datadir, tmp_path):
    # patch client with a mock client class
    class mock_client():
        def __init__(self, service):
            assert service == 's3'

        def upload_file(self, path, bucket, storage_id):
            assert path == str(datadir / 'hello.txt')
            assert bucket == 'bucket'
            assert storage_id == 'a948904f2f0f479b8f8197694b30184b0d2ed1c1cd2a1ec0fb85d299a192a447'

        def download_file(self, bucket, storage_id, path):
            assert bucket == 'bucket'
            assert storage_id == 'a948904f2f0f479b8f8197694b30184b0d2ed1c1cd2a1ec0fb85d299a192a447'
            assert path == '/tmp/a948904f2f0f479b8f8197694b30184b0d2ed1c1cd2a1ec0fb85d299a192a447'
    monkeypatch.setattr('ace2.storage.client', mock_client)

    # patch env var for bucket
    monkeypatch.setattr('os.environ', { 'FILE_STORAGE_BUCKET': 'bucket' })

    # test upload
    storage_id = upload(str(datadir / 'hello.txt'))
    assert storage_id == 'a948904f2f0f479b8f8197694b30184b0d2ed1c1cd2a1ec0fb85d299a192a447'

    # test download
    path = download('a948904f2f0f479b8f8197694b30184b0d2ed1c1cd2a1ec0fb85d299a192a447')
    assert path == '/tmp/a948904f2f0f479b8f8197694b30184b0d2ed1c1cd2a1ec0fb85d299a192a447'
