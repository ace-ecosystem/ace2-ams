from .metadata import Metadata

class Tag(Metadata):
    ''' tag metadata class '''

    def __init__(self, value:str, **kwargs):
        ''' initializes a tag object

        Args:
            value (str): the tag value
        '''

        super().__init__(self.type, value, **kwargs)
