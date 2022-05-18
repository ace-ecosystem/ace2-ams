from .metadata import Metadata

class DetectionPoint(Metadata):
    ''' detection point metadata class '''

    def __init__(self, value:str, **kwargs):
        ''' initializes a detection point object

        Args:
            value (str): the detection point value
        '''

        super().__init__(self.type, value, **kwargs)
