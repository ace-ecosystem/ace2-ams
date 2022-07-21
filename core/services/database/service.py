from ace2 import *

class Database(Service):
    ''' Client class for sending commands to the Database Service '''

    def submit_analysis(self, analysis:dict):
        ''' inserts/updates analysis in the database and starts any new analysis that needs to run

        Args:
            analysis: analysis dictionary state to insert into the database
        '''

        # TODO: add the analysis to the database and start any new analysis that needs to run
        pass
