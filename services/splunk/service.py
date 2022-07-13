from ace2 import *

class Splunk(Service):
    ''' Splunk integration service '''

    def query(self, query, callback):
        ''' Executes a query in splunk and sends results to the callback

        Args:
            query: the query to execute
            callback: the Command to send results and query link to
        '''

        # TODO: start query in splunk and get search id (sid)

        # get the results
        self.get_results(sid, callback)

    def get_results(self, sid, callback):
        ''' Gets the results of a splunk search by sid and sends the results and link to the callback.
        If the search is not complete then delay and try again.

        Args:
            sid: the search to get results for
            callback: the Command to send results and query link to
        '''

        # TODO: check if query is complete
        
        # if query is not complete then check again later
        if not compelte:
            Command.send(self.get_results, sid, callback, delay='10')
            return

        # TODO: download results

        # TODO: generate gui link for this query

        # pass results and link to callback
        Command.send(callback, results, link)
