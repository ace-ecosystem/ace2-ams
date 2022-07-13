from ace2 import *
import json
import pytest

def test_service(mock_queue):
    class MyService(Service):
        class Settings(Service.Settings):
            foo: str

        def execute_via_arg(self):
            # test adding something to the state info
            self.state['hello'] = 'world'

            # test sending from service with callback as positional argument
            Command.send(self.callback, self.end)

        def execute_via_kwarg(self):
            # test sending from service with callback as keyword argument
            Command.send(self.callback, callback=self.end)

        def callback(self, callback):
            # test sending from instruction
            Command.send(callback, self.settings.foo)

        def end(self, message:str):
            pass

    # send instruction to MyService
    Command.send(MyService().execute_via_arg)
    message = mock_queue.get('my_service')
    assert message['delaySeconds'] == 0
    assert json.loads(message['body']) == {
        'service': {
            'type': 'my_service',
            'instance': None,
            'state': {},
        },
        'method': 'execute_via_arg',
        'args': [],
        'kwargs': {},
    }

    # run the instruction to completion
    run({'Records': [message]}, {})
    message = mock_queue.get('my_service')
    run({'Records': [message]}, {})
    message = mock_queue.pop('my_service')
    assert message['delaySeconds'] == 0
    assert json.loads(message['body']) == {
        'service': {
            'type': 'my_service',
            'instance': None,
            'state': {
                'hello': 'world',
            },
        },
        'method': 'end',
        'args': [ 'bar' ],
        'kwargs': {},
    }

    # dispatch instruction to MyService in non default way
    Command.send(MyService(instance='my_instance').execute_via_kwarg, delay=5)
    message = mock_queue.get('my_service')
    assert message['delaySeconds'] == 5
    assert json.loads(message['body']) == {
        'service': {
            'type': 'my_service',
            'instance': 'my_instance',
            'state': {},
        },
        'method': 'execute_via_kwarg',
        'args': [],
        'kwargs': {},
    }

    # run the instruction to completion
    run({'Records': [message]}, {})
    message = mock_queue.get('my_service')
    run({'Records': [message]}, {})
    message = mock_queue.pop('my_service')
    assert message['delaySeconds'] == 0
    assert json.loads(message['body']) == {
        'service': {
            'type': 'my_service',
            'instance': 'my_instance',
            'state': {},
        },
        'method': 'end',
        'args': [ 'rab' ],
        'kwargs': {},
    }

    with pytest.raises(Exception):
        MyService(instance='no_settings').settings.foo

    with pytest.raises(Exception):
        MyService(instance='bad_settings').settings.foo
