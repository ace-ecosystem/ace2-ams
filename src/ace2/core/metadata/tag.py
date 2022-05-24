from .metadata import Metadata

class Tag(Metadata):
    ''' tag metadata class '''

    def __init__(self, value:str, **kwargs):
        ''' initializes a tag object

        Args:
            value: the tag value
            **kwargs: key word arguments to pass through
        '''

        super().__init__(self.type, value, **kwargs)
