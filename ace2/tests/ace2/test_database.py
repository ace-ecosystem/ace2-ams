from ace2 import *
from ace2.database import Database
import json

def test_database(mock_queue):
    # submit some analysis to the database
    analysis = Module(
        type = 'analysis',
        id = 123,
        target = Observable('bar', type='foo'),
        state = { 'hello': 'world' },
    )
    Database().submit_analysis(analysis)

    # verify message on database queue
    message = mock_queue.pop('database')
    assert json.loads(message['body']) == {
        'service': {
            'type': 'database',
            'instance': None,
            'state': {},
        },
        'method': 'submit_analysis',
        'args': [{
            'type': 'analysis',
            'id': 123,
            'instance': None,
            'target': {
                'type': 'foo',
                'value': 'bar',
                'metadata': [],
            },
            'summary': None,
            'observables': [],
            'details': {},
            'status': 'running',
        }],
        'kwargs': {},
    }
