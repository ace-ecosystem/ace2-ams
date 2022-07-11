from ace2 import *
from ace2.analysis import Analysis
import json

def test_analysis(mock_queue):
    class MyAnalysis(Analysis):
        class Details(Analysis.Details):
            hello: str = Field(default='world')

    # test ignore
    analysis = Analysis(type='my_analysis')
    analysis.ignore()
    assert analysis.status == 'ignore'
    message = mock_queue.pop('database')
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
                'type': 'my_analysis',
                'status': 'ignore',
                'target': None,
                'details': {
                    'hello': 'world',
                },
                'observables': [],
                'summary': None,
            },
        ],
        'kwargs': {},
    }

    # test submit
    analysis.submit()
    assert analysis.status == 'complete'
    message = mock_queue.pop('database')
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
                'type': 'my_analysis',
                'status': 'complete',
                'target': None,
                'details': {
                    'hello': 'world',
                },
                'observables': [],
                'summary': None,
            },
        ],
        'kwargs': {},
    }

    # test making some changes
    analysis.details.hello = 'everybody'
    analysis.add(Observable, 'bar', type='foo')
    observable = analysis.add(Observable, 'bar', type='foo')
    assert isinstance(observable, Observable)
    assert observable.type == 'foo'
    assert observable.value == 'bar'
    analysis.summary = 'this is my analysis'
    assert analysis.dict() == {
        'id': None,
        'type': 'my_analysis',
        'target': None,
        'status': 'complete',
        'summary': 'this is my analysis',
        'details': {
            'hello': 'everybody',
        },
        'observables': [
            {
                'type': 'foo',
                'value': 'bar',
                'metadata': [],
            },
        ],
    }
