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
    queues = {}
    global receipt_handle
    receipt_handle = 0

    def add(queue, message, delay=0):
        global queues
        global receipt_handle

        # create queue if it doesnt exist yet
        if queue not in queues:
            queues[queue] = {}

        # add message to queue
        queues[queue][receipt_handle] = {
            'receiptHandle': receipt_handle,
            'body': json.dumps(message),
            'delaySeconds': delay,
        }

        # increment receipt handle
        receipt_handle += 1

    def remove(queue, receipt_handle):
        global queues
        del queues[queue][receipt_handle]

    def get(queue):
        global queues
        receipt_handle = sorted(queues[queue])[0]
        return {
            'Records': [
                queues[queue][receipt_handle],
            ],
        }

    monkeypatch.setattr('ace2.queue.add', add)
    monkeypatch.setattr('ace2.queue.remove', remove)
    monkeypatch.setattr('ace2.queue.get', get)
