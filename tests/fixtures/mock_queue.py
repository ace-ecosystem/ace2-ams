import ace2
import json
import pytest

queues = {}
receipt_handle = 0

# monkeypatch queue with mock queue to avoid needing to connect to sqs
@pytest.fixture(autouse=True)
def mock_queue(monkeypatch):
    # reset queues before each test
    global queues
    global receipt_handle
    queues = {}
    receipt_handle = 0

    class mock_client():
        def __init__(self, service):
            assert service == 'sqs'

        def send_message(self, QueueUrl=None, MessageBody=None, DelaySeconds=None):
            global queues
            global receipt_handle

            # create queue if it doesnt exist yet
            if QueueUrl not in queues:
                queues[QueueUrl] = {}

            # add message to queue
            queues[QueueUrl][receipt_handle] = {
                'receiptHandle': receipt_handle,
                'body': MessageBody,
                'delaySeconds': DelaySeconds,
            }

            # increment receipt handle
            receipt_handle += 1
            
        def delete_message(self, QueueUrl=None, ReceiptHandle=None):
            global queues
            del queues[QueueUrl][ReceiptHandle]

    monkeypatch.setattr('ace2.queue.client', mock_client)
    monkeypatch.setattr('ace2.queue.environ', { 'QUEUE_BASE_URL': 'base' })

    def pop_message(queue, delete=True):
        global queues
        try:
            queue = f'base/{queue}'
            key = sorted(queues[queue])[0]
            message = queues[queue][key]
            if delete:
                del queues[queue][key]
            return message

        except IndexError:
            return None

    return pop_message
