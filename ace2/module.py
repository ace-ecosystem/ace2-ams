from .analysis import Analysis
from .service import Service

class Module(Service, Analysis):
    ''' Base class for building analysis modules '''

    def start(self):
        ''' This is the entry point for running analysis '''

        # ignore analysis if it should not run
        if not self.should_run():
            self.ignore()
            return

        # execute the analysis
        self.execute()

    def should_run(self) -> bool:
        ''' Subclasses must override this function to determine when analysis will run

        Returns:
            True if analysis should run
        '''

        raise NotImplementedError()

    def execute(self):
        ''' Subclasses must override this function to perform their analysis '''

        raise NotImplementedError()
