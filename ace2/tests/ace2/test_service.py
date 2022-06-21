from ace2 import *
import json

def test_service(mock_queue):
    class MyService(Service):
        class Settings(Service.Settings):
            foo: str

        def execute_via_arg(self):
            # test dispatching from service with callback as positional argument
            self.dispatch('callback', self.end)

        def execute_via_kwarg(self):
            # test dispatching from service with callback as keyword argument
            self.dispatch('callback', callback=self.end)

        def callback(self, callback:Instruction):
            # test dispatching from instruction
            callback.dispatch(self.settings.foo)

        def end(self, message:str):
            pass

    # dispatch instruction to MyService
    Service('my_service').dispatch('execute_via_arg')
    message = mock_queue.get('my_service')
    assert message['delaySeconds'] == 0
    assert json.loads(message['body']) == {
        'service': {
            'type': 'my_service',
            'instance': None,
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
        },
        'method': 'end',
        'args': [ 'bar' ],
        'kwargs': {},
    }

    # dispatch instruction to MyService in non default way
    Service('my_service', instance='my_instance').dispatch('execute_via_kwarg', delay=5)
    message = mock_queue.get('my_service')
    assert message['delaySeconds'] == 5
    assert json.loads(message['body']) == {
        'service': {
            'type': 'my_service',
            'instance': 'my_instance',
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
        },
        'method': 'end',
        'args': [ 'rab' ],
        'kwargs': {},
    }
