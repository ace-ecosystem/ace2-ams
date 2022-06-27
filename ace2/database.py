from .service import Command, Service

class Database(Service):
    ''' Client class for sending commands to the Database Service '''

    def submit_analysis(self, analysis):
        ''' submits analysis to the database

        Args:
            analysis: the Analysis object to submit
        '''

        # create and send a command to submit the analysis to the database
        Command.send(self.submit_analysis, analysis.dict(exclude={'state'}))
