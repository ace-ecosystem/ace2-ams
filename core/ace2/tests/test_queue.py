from ace2 import queue

def test_queue(mock_queue):
    # test adding to a queue
    queue.add('my_queue', 'hello', delay=5)
    assert mock_queue.get('my_queue') == {
        'receiptHandle': 0,
        'body': 'hello',
        'delaySeconds': 5,
    }

    # test removing from a queue
    queue.remove('my_queue', 0)
    assert mock_queue.get('my_queue') == None
