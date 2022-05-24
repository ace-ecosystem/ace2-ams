from .observable import Observable

class UriPath(Observable):
    ''' Observable that represents a uri path '''

    def __init__(self, value:str, **kwargs):
        ''' Initializes a uri path observable

        Args:
            value: the uri path
            **kwargs: key word arguments to pass through
        '''

        # call super class constructor with our type and given value
        super().__init__(self.type, value, **kwargs)
