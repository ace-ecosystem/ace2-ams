from ace2 import *
import json

def test_analysis(mock_queue):
    class MyAnalysis(Analysis):
        class Settings(Analysis.Settings):
            foo: str

        class Details(Analysis.Details):
            result: str = Field(default=None, description='some details field')

        def should_run(self):
            return isinstance(self.target, IPv4)

        def execute(self):
            # test adding observable
            observable = self.add(IPv4, '127.0.0.1')
            assert isinstance(observable, IPv4)
            assert observable.value == '127.0.0.1'

            # test adding same observable twice
            self.add(IPv4, '127.0.0.1')

            # test details and settings
            self.details.result = self.settings.foo

            # test summary
            self.summary = 'hello world'

            # submit analysis
            self.submit()

    # test analysis that should not run
    analysis = {
        'id': 1,
        'type': 'my_analysis',
        'target': {
            'type': 'fqdn',
            'value': '127.0.0.1',
        },
    }
    analysis = Analysis(**analysis)
    analysis.start()

    # verify database message
    message = mock_queue.pop('database')
    assert message['delaySeconds'] == 0
    assert json.loads(message['body']) == {
        'service': {
            'type': 'database',
            'instance': None,
        },
        'method': 'submit_analysis',
        'args': [
            {
                'id': 1,
                'type': 'my_analysis',
                'instance': None,
                'status': 'ignored',
                'target': {
                    'type': 'fqdn',
                    'value': '127.0.0.1',
                    'metadata': [],
                },
                'details': {
                    'result': None,
                },
                'observables': [],
                'summary': None,
            },
        ],
        'kwargs': {},
    }

    # test analysis that should run
    analysis = {
        'id': 1,
        'type': 'my_analysis',
        'target': {
            'type': 'ipv4',
            'value': '127.0.0.1',
        },
    }
    analysis = Analysis(**analysis)
    analysis.start()

    # verify first database message
    message = mock_queue.pop('database')
    assert message['delaySeconds'] == 0
    assert json.loads(message['body']) == {
        'service': {
            'type': 'database',
            'instance': None,
        },
        'method': 'submit_analysis',
        'args': [
            {
                'id': 1,
                'type': 'my_analysis',
                'instance': None,
                'status': 'running',
                'target': {
                    'type': 'ipv4',
                    'value': '127.0.0.1',
                    'metadata': [],
                },
                'details': {
                    'result': None,
                },
                'observables': [],
                'summary': None,
            },
        ],
        'kwargs': {},
    }

    # verify seconds database message
    message = mock_queue.pop('database')
    assert message['delaySeconds'] == 0
    assert json.loads(message['body']) == {
        'service': {
            'type': 'database',
            'instance': None,
        },
        'method': 'submit_analysis',
        'args': [
            {
                'id': 1,
                'type': 'my_analysis',
                'instance': None,
                'status': 'complete',
                'target': {
                    'type': 'ipv4',
                    'value': '127.0.0.1',
                    'metadata': [],
                },
                'details': {
                    'result': 'bar',
                },
                'observables': [
                    {
                        'type': 'ipv4',
                        'value': '127.0.0.1',
                        'metadata': [],
                    },
                ],
                'summary': 'hello world',
            },
        ],
        'kwargs': {},
    }
