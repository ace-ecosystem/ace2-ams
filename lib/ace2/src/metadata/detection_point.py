from .metadata import Metadata

class DetectionPoint(Metadata):
    ''' detection point metadata class '''

    def __init__(self, value:str, **kwargs):
        ''' initializes a detection point object

        Args:
            value: the detection point value
            **kwargs: key word arguments to pass through
        '''

        super().__init__(self.type, value, **kwargs)
