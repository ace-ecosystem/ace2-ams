from ace2 import *
import json

def test_submission():
    class Yarp(Submission):
        class Details(Submission.Details):
            foo: Optional[str] = Field(default=None)

    s = Yarp(
        type = 'my_submission',
        queue = 'external',
        mode = 'detect',
        detect_mode = 'detect modules',
        alert_mode = 'alert modules',
        response_mode = 'response modules',
        details = {'foo': 'bar'},
    )

    assert json.loads(s.json()) == {
        'id': None,
        'type': 'my_submission',
        'status': 'running',
        'target': None,
        'event_time': '2020-01-02T03:04:05.000006+00:00',
        'details': {
            'foo': 'bar',
        },
        'observables': [],
        'summary': None,
        'queue': 'external',
        'mode': 'detect',
        'detect_mode': 'detect modules',
        'alert_mode': 'alert modules',
        'response_mode': 'response modules',
    }

