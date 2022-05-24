from .observable import Observable

class FQDN(Observable):
    ''' Observable that represents a fully qualified domain name '''

    def __init__(self, value:str, **kwargs):
        ''' Initializes a fqdn observable

        Args:
            value: the fqdn
            **kawrgs: key word arguments to pass through
        '''

        # call super class constructor with our type and given value
        super().__init__(self.type, value, **kwargs)
