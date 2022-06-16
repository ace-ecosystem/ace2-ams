from ace2 import *
import json
from pydantic import Field
from typing import Optional

def test_analysis(monkeypatch):
    class MyAnalysis(Analysis):
        class Settings(Analysis.Settings):
            foo: str

        class Details(Analysis.Details):
            result: str = Field(default=None, description='some details field')

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

    # run analysis
    analysis = {
        'id': 1,
        'type': 'my_analysis',
        'target': {
            'type': 'ipv4',
            'value': '127.0.0.1',
        },
    }
    module = MyAnalysis(**analysis)
    module.execute()

    # verify analysis
    assert isinstance(module, Service)
    assert module.summary == 'hello world'
    assert module.details.result == 'bar'
    assert len(module.observables) == 1
    observable = module.observables[0]
    assert isinstance(observable, IPv4)
    assert observable.value == '127.0.0.1'
