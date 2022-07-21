from ace2 import *

class Splunk(Service):
    ''' Interface for using the splunk integration service '''

    def query(self, query:str, callback:Command):
        ''' Executes a query in splunk and sends results to the callback

        Args:
            query: the query to execute
            callback: the Command to send results and query link to
        '''

        # dispatch command to service
        Command.send(self.query, query, callback)
