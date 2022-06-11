from ace2 import *

class TestCallback:
    def do_something(self, foo, bar=None):
        self.foo = foo
        self.bar = bar
        return 'beep'

    def test_callback(self):
        # create a callback
        callback = Callback(self.do_something)

        # verify attributes
        assert callback.method == 'do_something'
        assert callback.seconds == 0

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
        }

        # load callback from state
        callback = Callback(**state)

        # verify attributes
        assert callback.method == 'do_something'
        assert callback.seconds == 0

        # create a callback with seconds
        callback = Callback(self.do_something, seconds=1)

        # verify attributes
        assert callback.method == 'do_something'
        assert callback.seconds == 1
