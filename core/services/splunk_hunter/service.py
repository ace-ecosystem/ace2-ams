from ace2 import *
from splunk import Splunk

class SplunkHunter(Collector):
    name: str = Field(description='the name of the hunt')
    query: str = Field(description='the query to run')
    observable_map: dict = Field(default_factory=dict, description='fields to map to observables')
    max_time_range: str = Field(default='48:00:00', description='max query timespan')
    offset: str = Field(default='5:00', description='timespan offset from now to query up to')
    use_index_time: bool = Field(default=True, description='if we should use index time instead of event time')

    def execute(self):
        # build the query from settings
        self.build_query()

        # run the query
        Splunk(instance=self.instance).query(self.query, callback=self.process)

    def build_query(self):
        # create end time
        end = now() - timespan(self.offset)

        # get start time from last end time
        key = f'splunk_hunter.{self.name}.last_end_time'
        max_time_range = timespan(self.max_time_range)
        min_start = end - max_time_range
        start = persistent_data.get_timestamp(key, min_start)
        if start < min_start:
            start = min_start

        # set last end time to current end time
        persistent_data.set_timestamp(key, end)

        # format start and end times
        start = 'earliest = ' + start.strftime('%m/%d/%Y:%H:%M:%S')
        end = 'latest = ' + end.strftime('%m/%d/%Y:%H:%M:%S')

        # apply timespec to index time if specified
        if self.use_index_time:
            start = '_index_' + start
            end = '_index_' + end

        # replace timespec with start and end
        self.query = self.query.replace('{time_spec}', f'{start} {end}')

    def process(self, results, link):
        for result in results:
            # make the submission
            submission = Submission(
                type = 'splunk_hunter_' + self.name,
                event_time = strptime(result['_time'], '%Y-%m-%dT%H:%M:%S') if '_time' in result else now(),
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
