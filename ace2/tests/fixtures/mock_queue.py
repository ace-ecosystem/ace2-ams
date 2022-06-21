import ace2
import json
import pytest

queues = {}
receipt_handle = 0

# monkeypatch queue with mock queue to avoid needing to connect to sqs
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
