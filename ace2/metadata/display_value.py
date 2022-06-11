from .metadata import Metadata

class DisplayValue(Metadata):
    ''' metadata class used to override an observables displayed value '''

    def __init__(self, value:str, **kwargs):
        ''' initializes display value

        Args:
            value: the value to display in place of the actual observable value
            **kwargs: key word arguments to pass through
        '''

        super().__init__(self.type, value, **kwargs)
