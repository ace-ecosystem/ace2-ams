from ace2.queue import add, remove, get

def test_queue(monkeypatch):
    # patch client with a mock client class
    class mock_client():
        def __init__(self, service):
            assert service == 'sqs'

        def send_message(self, QueueUrl=None, MessageBody=None, DelaySeconds=None):
            assert QueueUrl == 'SomeQueue'
            assert MessageBody == {'hello':'world'}
            assert DelaySeconds == 5
            
        def delete_message(self, QueueUrl=None, ReceiptHandle=None):
            assert QueueUrl == 'SomeQueue'
            assert ReceiptHandle == 'abc'

        def receive_message(self, QueueUrl=None, VisibilityTimeout=None):
            assert VisibilityTimeout == 15 * 60
            if QueueUrl == 'SomeQueue':
                return [{
                    'ReceiptHandle': 'abc',
                    'Body': {'hello':'world'},
                }]
            return []
    monkeypatch.setattr('ace2.queue.client', mock_client)

    # test
    add('SomeQueue', {'hello':'world'}, delay=5)
    assert get('SomeQueue') == {
        'ReceiptHandle': 'abc',
        'Body': {'hello':'world'},
    }
    assert get('EmptyQueue') == None
    remove('SomeQueue', 'abc')

