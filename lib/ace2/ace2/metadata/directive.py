from .metadata import Metadata

class Directive(Metadata):
    ''' directive metadata class '''

    def __init__(self, value:str, **kwargs):
        ''' initializes a directive object

        Args:
            value: the directive value
            **kwargs: key word arguments to pass through
        '''

        super().__init__(self.type, value, **kwargs)
