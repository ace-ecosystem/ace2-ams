from ace2 import *
import json

def test_collector(mock_queue):
    class MyCollector(Collector):
        def execute(self):
            submission = Submission(
                type = 'my_submission',
                queue = 'external',
                mode = 'detect',
                detect_mode = 'detect modules',
                alert_mode = 'alert modules',
                response_mode = 'response modules',
            )
            submission.submit()

    # send execute commadn to my collector
    Command.send(MyCollector().execute)
    message = mock_queue.get('my_collector')
    assert message['delaySeconds'] == 0
    assert json.loads(message['body']) == {
        'service': {
            'type': 'my_collector',
            'instance': None,
            'state': {},
        },
        'method': 'execute',
        'args': [],
        'kwargs': {},
    }

    # run the collector
    run({'Records': [message]}, {})
    message = mock_queue.get('database')
    assert message['delaySeconds'] == 0
    assert json.loads(message['body']) == {
        'service': {
            'type': 'database',
            'instance': None,
            'state': {},
        },
        'method': 'submit_analysis',
        'args': [
            {
                'id': None,
                'type': 'my_submission',
                'status': 'complete',
                'target': None,
                'event_time': '2020-01-02T03:04:05.000006+00:00',
                'details': {},
                'observables': [],
                'summary': None,
                'queue': 'external',
                'mode': 'detect',
                'detect_mode': 'detect modules',
                'alert_mode': 'alert modules',
                'response_mode': 'response modules',
            },
        ],
        'kwargs': {},
    }
