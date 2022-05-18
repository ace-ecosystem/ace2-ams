from .metadata import Metadata

class DisplayValue(Metadata):
    ''' metadata class used to override an observables displayed value '''

    def __init__(self, value:str, **kwargs):
        ''' initializes display value

        Args:
            value (str): the value to display in place of the actual observable value
        '''

        super().__init__(self.type, value, **kwargs)
