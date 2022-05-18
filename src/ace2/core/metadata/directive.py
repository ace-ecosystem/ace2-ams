from .metadata import Metadata

class Directive(Metadata):
    ''' directive metadata class '''

    def __init__(self, value:str, **kwargs):
        ''' initializes a directive object

        Args:
            value (str): the directive value
        '''

        super().__init__(self.type, value, **kwargs)
