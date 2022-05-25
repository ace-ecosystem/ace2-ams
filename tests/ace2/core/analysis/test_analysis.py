from ace2.core import *

def test_analysis(monkeypatch, mock_datetime):
    class MyAnalysis(Analysis):
        class Config(Analysis.Config):
            foo: str

        @property
        def valid_observables(self):
            return [ IPv4, 'FQDN' ]

        @property
        def required_directives(self):
            return [ 'do_it', 'no_really' ]

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
            return Callback(self.get_results)

        def get_results(self, observable):
            # verify observable is passed correctly
            assert isinstance(observable, IPv4)
            assert observable.type == 'IPv4'
            assert observable.value == '127.0.0.1'

            # make sure the state was kept
            assert self.state['submission_id'] == '123'

            # add some details
            self.details['result'] = 'its malz bro'

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
            self.summary = f'hey, {self.details["result"]}'

    # create analysis to run
    analysis = {
        'id': 1,
        'type': 'MyAnalysis',
        'target': {
            'type': 'IPv4',
            'value': '127.0.0.1',
        },
    }

    # run the analysis with the lambda handler function
    analysis = Analysis(**analysis).run()

    # verify result
    assert analysis == {
        'id': 1,
        'type': 'MyAnalysis',
        'target': {
            'type': 'IPv4',
            'value': '127.0.0.1',
            'metadata': [],
        },
        'summary': None,
        'details': {},
        'observables': [],
        'callback': {
            'method': 'get_results',
            'timestamp': mock_datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
        },
        'state': {
            'submission_id': '123',
        },
    }

    # run again to test the callback
    analysis = Analysis(**analysis).run()

    # verify result
    assert analysis == {
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
        'callback': None,
        'state': {
            'submission_id': '123',
        },
    }

    # test should run with type
    analysis = {
        'id': 1,
        'type': 'MyAnalysis',
        'target': {
            'type': 'IPv4',
            'value': '127.0.0.1',
            'metadata' : [
                {
                    'type': 'Directive',
                    'value': 'do_it',
                },
                {
                    'type': 'Directive',
                    'value': 'no_really',
                },
            ],
        },
    }
    assert Analysis(**analysis).should_run()

    # test should run with string
    analysis = {
        'id': 1,
        'type': 'MyAnalysis',
        'target': {
            'type': 'FQDN',
            'value': '127.0.0.1',
            'metadata' : [
                {
                    'type': 'Directive',
                    'value': 'do_it',
                },
                {
                    'type': 'Directive',
                    'value': 'no_really',
                },
            ],
        },
    }
    assert Analysis(**analysis).should_run()

    # make sure not to run if missing directive
    analysis = {
        'id': 1,
        'type': 'MyAnalysis',
        'target': {
            'type': 'IPv4',
            'value': '127.0.0.1',
            'metadata' : [
                {
                    'type': 'Directive',
                    'value': 'do_it',
                },
            ],
        },
    }
    assert not Analysis(**analysis).should_run()

    # make sure not to run if wrong observable type
    analysis = {
        'id': 1,
        'type': 'MyAnalysis',
        'target': {
            'type': 'nope',
            'value': '127.0.0.1',
            'metadata' : [
                {
                    'type': 'Directive',
                    'value': 'do_it',
                },
                {
                    'type': 'Directive',
                    'value': 'no_really',
                },
            ],
        },
    }
    assert not Analysis(**analysis).should_run()
