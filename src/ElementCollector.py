import json


class ElementCollector(object):
    source_name = 'base'

    def save_sample(self, data):
        obj = {'sampleNumber': self.sampleNumber,
               'data': data, 'source':self.source_name}
        self.sampleNumber += 1
        self.samples.append(obj)
        self.render_values()
        return obj

    def on_sample_time(self):
        pass

    def render_values(self):
        return json.dumps(self.samples)

    def __init__(self, schedule, sampling_period,
                 total_sample_points, sampleCallback):
        self.samples = []
        self.samplingPeriod = sampling_period
        self.totalSamplesPoints = total_sample_points
        self.dataPoint = 0
        self.sampleNumber = 0
        self.sampleCallback = sampleCallback
        self.schedule = schedule
        self.schedule.enter(self.samplingPeriod, 1,
                            self.do_something, (self.schedule,))

    def do_something(self, sc):
        self.on_sample_time()
        if self.sampleNumber > 0 and self.sampleNumber % self.totalSamplesPoints == 0:
            self.dataPoint += 1
            self.sampleCallback(self.dataPoint,
                                self.source_name, self.render_values())
            self.samples = []
        self.schedule.enter(self.samplingPeriod, 1,
                            self.do_something, (sc,))

