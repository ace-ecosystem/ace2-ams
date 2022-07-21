from .service import Service

class Collector(Service):
    ''' Base class for building collectors '''

    def execute(self):
        ''' Collector entry point. Subclasses must override this function '''

        raise NotImplementedError()
