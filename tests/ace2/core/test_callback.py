import datetime
from ace2.core import Callback

class TestCallback:
    def do_something(self, foo, bar=None):
        self.foo = foo
        self.bar = bar
        return 'beep'

    def test_callback(self, mock_datetime):
        # create a callback
        callback = Callback(self.do_something)

        # verify attributes
        assert callback.method == 'do_something'
        assert callback.timestamp == mock_datetime.utcnow()

        # run the callback
        result = callback.execute(self, 'hello', bar='world')
        assert result == 'beep'
        assert self.foo == 'hello'
        assert self.bar == 'world'

        # save the state
        state = callback.dict()

        # verify state
        assert state == {
            'method': 'do_something',
            'timestamp': mock_datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
        }

        # load callback from state
        callback = Callback(**state)

        # verify attributes
        assert callback.method == 'do_something'
        assert callback.timestamp == mock_datetime.utcnow().replace(microsecond=0)

        # create a callback with kwargs
        kwargs = {
            'weeks': 1,
            'days': 1,
            'hours': 1,
            'minutes': 1,
            'seconds': 1,
        }
        callback = Callback(self.do_something, **kwargs)

        # verify attributes
        assert callback.method == 'do_something'
        assert callback.timestamp == mock_datetime.utcnow() + datetime.timedelta(**kwargs)
