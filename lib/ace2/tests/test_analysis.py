from ace2 import *
import json
from pydantic import Field
from typing import Optional

def test_analysis(monkeypatch, mock_datetime):
    class MyAnalysis(Analysis):
        class Config(Analysis.Config):
            foo: str

        class Details(Analysis.Details):
            result: str = Field(default=None, description='some details field')

        def execute(self, observable):
            # verify observable is passed correctly
            assert isinstance(observable, IPv4)
            assert observable.type == 'IPv4'
            assert observable.value == '127.0.0.1'

            # verify config property works
            assert self.config.foo == 'bar'

            # pretend that we submitted something to a sandbox or whatever
            self.state['submission_id'] = '123'

            # check back later
            return Callback(self.get_results, seconds=5)

        def get_results(self, observable):
            # verify observable is passed correctly
            assert isinstance(observable, IPv4)
            assert observable.type == 'IPv4'
            assert observable.value == '127.0.0.1'

            # make sure the state was kept
            assert self.state['submission_id'] == '123'

            # add some details
            self.details.result = 'its malz bro'

            # add a generic child observable
            observable = self.add(Observable, 'foo', 'bar')
            assert len(self.observables) == 1
            assert isinstance(observable, Observable)
            assert observable.type == 'foo'
            assert observable.value == 'bar'

            # ensure duplicate observables are not added
            observable = self.add(Observable, 'foo', 'bar')
            assert len(self.observables) == 1

            # add a typed child observble
            observable = self.add(IPv4, '127.0.0.1')
            assert len(self.observables) == 2
            assert isinstance(observable, IPv4)
            assert observable.type == 'IPv4'
            assert observable.value == '127.0.0.1'

            # set the summary
            self.summary = f'hey, {self.details.result}'

    # add analysis to the queue
    analysis = {
        'id': 1,
        'type': 'MyAnalysis',
        'target': {
            'type': 'IPv4',
            'value': '127.0.0.1',
        },
    }
    queue.add('MyAnalysis', analysis)

    # get a message from the queue
    message = queue.get('MyAnalysis')

    # run the analysis with the lambda handler function
    run(message, None)

    # make sure message was requeued
    message = queue.get('MyAnalysis')

    # verify result
    assert message['Records'][0]['delaySeconds'] == 5
    assert json.loads(message['Records'][0]['body']) == {
        'id': 1,
        'type': 'MyAnalysis',
        'target': {
            'type': 'IPv4',
            'value': '127.0.0.1',
            'metadata': [],
        },
        'summary': None,
        'details': {
            'result': None
        },
        'observables': [],
        'callback': {
            'method': 'get_results',
        },
        'state': {
            'submission_id': '123',
        },
    }

    # run again to test the callback
    run(message, None)

    # make sure message was submitted
    message = queue.get('Submission')

    # verify result
    assert json.loads(message['Records'][0]['body']) == {
        'id': 1,
        'type': 'MyAnalysis',
        'target': {
            'type': 'IPv4',
            'value': '127.0.0.1',
            'metadata': [],
        },
        'summary': 'hey, its malz bro',
        'details': {
            'result': 'its malz bro',
        },
        'observables': [
            {
                'type': 'foo',
                'value': 'bar',
                'metadata': [],
            },
            {
                'type': 'IPv4',
                'value': '127.0.0.1',
                'metadata': [],
            },
        ],
    }
