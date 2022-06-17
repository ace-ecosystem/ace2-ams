from ace2 import queue
import json

def test_queue(mock_queue):
    # test adding to a queue
    queue.add('my_queue', {'hello': 'world'}, delay=5)
    assert mock_queue.get('my_queue') == {
        'receiptHandle': 0,
        'body': json.dumps({'hello': 'world'}),
        'delaySeconds': 5,
    }

    # test removing from a queue
    queue.remove('my_queue', 0)
    assert mock_queue.get('my_queue') == None
