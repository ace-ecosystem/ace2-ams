import ace2
from ace2.timestamp import Timestamp
from ace2.storage import get_storage_id
from datetime import datetime, timezone
import os
import pytest
from shutil import copyfile


# make sure we return a constant value from datetime.now functions
_mock_now = datetime(2020, 1, 2, 3, 4, 5, 6)
@pytest.fixture(autouse=True)
def mock_now(monkeypatch):
    class mock_datetime(datetime):
        def utcnow(*args, **kwargs):
            return _mock_now

    # patch datetime so it produces fixed values
    monkeypatch.setattr('ace2.timestamp.datetime', mock_datetime)

    # return mock now so tests can make assertions with it
    return Timestamp.from_datetime(_mock_now)


# monkeypatch queue with mock queue to avoid needing to connect to sqs
queues = {}
receipt_handle = 0
@pytest.fixture(autouse=True)
def mock_queue(monkeypatch):
    class MockQueues():
        def __init__(self):
            self.queues = {}
            self.receipt_handle = 0

        def send_message(self, QueueUrl=None, MessageBody=None, DelaySeconds=None):
            # create queue if it doesnt exist yet
            if QueueUrl not in self.queues:
                self.queues[QueueUrl] = {}

            # add message to queue
            self.queues[QueueUrl][self.receipt_handle] = {
                'receiptHandle': self.receipt_handle,
                'body': MessageBody,
                'delaySeconds': DelaySeconds,
            }

            # increment receipt handle
            self.receipt_handle += 1
            
        def delete_message(self, QueueUrl=None, ReceiptHandle=None):
            del self.queues[QueueUrl][ReceiptHandle]

        def get(self, queue):
            try:
                queue = f'base/{queue}'
                key = sorted(self.queues[queue])[0]
                return self.queues[queue][key]

            except IndexError:
                return None

        def pop(self, queue):
            try:
                queue = f'base/{queue}'
                key = sorted(self.queues[queue])[0]
                message = self.queues[queue][key]
                del self.queues[queue][key]
                return message

            except IndexError:
                return None

    mock_queues = MockQueues()
    def mock_client(service):
        assert service == 'sqs'
        return mock_queues

    monkeypatch.setattr('ace2.queue.client', mock_client)
    monkeypatch.setattr('ace2.queue.environ', { 'QUEUE_BASE_URL': 'base' })

    return mock_queues


# get secrets from test data file instead of connecting to Secrets Manager
@pytest.fixture(autouse=True)
def mock_secrets(monkeypatch, datadir):
    class MockClient():
        def get_secret_value(self, SecretId):
            with open(str(datadir / f'{SecretId}.json')) as f:
                return {'SecretString': f.read().strip()}

    class MockSession():
        @property
        def region_name(self):
            return 'the universe'

        def client(self, service_name=None, region_name=None):
            assert service_name == 'secretsmanager'
            assert region_name == 'the universe'
            return MockClient()

    monkeypatch.setattr('ace2.secrets.Session', MockSession)


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
