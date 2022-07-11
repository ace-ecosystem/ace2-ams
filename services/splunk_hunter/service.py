from ace2 import *
from splunk import Splunk

class SplunkHunter(Collector):
    name: str = Field(description='the name of the hunt')
    query: str = Field(description='the query to run')
    observable_map: dict = Field(default_factory=dict, description='fields to map to observables')

    def execute(self):
        # build the query from settings
        self.build_query()

        # run the query
        Splunk(instance=self.instance).query(self.query, callback=self.process)

    def build_query(self):
        # TODO: set next_run_time
        self.query = self.query

    def process(self, results, link):
        for result in results:
            # make the submission
            submission = Submission(
                type = 'splunk_hunter_' + self.name,
                event_time = 
                summary = self.name + ': ' + result[self.group_by] if self.group_by else self.name,
                details = {
                    'query': self.query,
                    'link': link,
                    'result': result,
                }
                queue = self.queue,
            )

            # add observables
            for field, observable_info in self.observable_map.items():
                if field in result:
                    observable = submission.add(Observable, result[field], type=observable_info['type'])
                    # TODO: add observable metadata

            # submit the submission
            submission.submit()
