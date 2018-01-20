from pynput import mouse
import time, sched
import numpy as np
from scipy import interpolate

from ElementCollector import ElementCollector

class MouseCollector(ElementCollector):
    source_name = 'mouse'

    def get_delta(self, passed):
        c_time = time.time()
        delta = c_time - self.last_event[passed]
        self.last_event[passed] = c_time
        return delta

    def __init__(self, schedule, samplePeriod,
                 total_sample_time, callback):
        self.move_data = [[0., 0., 0., {}]]
        self.scroll_data = []

        self.last_event = {}


        self.screen_height = 1600
        self.screen_width = 2560

        self.listener = mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click,
            on_scroll=self.on_scroll)

        c_time = time.time()
        for i in ['move', 'scroll']:
            self.last_event[i] = c_time

        self.listener.start()
        super().__init__(schedule, samplePeriod,
                         total_sample_time, callback)

    def on_sample_time(self):
        obj = {'move_data': self.normalise_move_samples(),
               'scroll_data': self.scroll_data}

        self.save_sample(obj)

        #print(self.normalise_move_samples())
        #print(self.move_data)
        self.scroll_data = []

    def on_move(self, x, y):
        delta = self.get_delta('move')
        self.move_data.append([delta, x/self.screen_width, y/self.screen_height, {}])

    def on_click(self, x, y, button, _):
        delta = self.get_delta('move')
        #self.move_data.append([delta, x/self.screen_width, y/self.screen_height, {'button':str(button)}])
        self.move_data.append([delta, x/self.screen_width, y/self.screen_height, {}])


    def on_scroll(self, x, y, dx, dy):
        delta = self.get_delta('scroll')
        self.scroll_data.append(((dx,dy),delta))

    def normalise_move_samples(self):
        # append last data point
        delta = self.get_delta('move')
        [[_, x, y, o]] = self.move_data[-1:]
        self.move_data.append([delta, x, y, o])

        data = self.move_data[:]
        cum_delta = np.cumsum(list(map(lambda x: x[0], data)))
        xs = np.asarray(list(map(lambda x: x[1], data)))
        ys = np.asarray(list(map(lambda x: x[2], data)))
        interp_x = interpolate.interp1d(cum_delta, xs)
        interp_y = interpolate.interp1d(cum_delta, ys)
        t_new = np.linspace(0, self.samplingPeriod,
                           (self.samplingPeriod * 10)+1)
        smoothed = np.column_stack((t_new,
                               interp_x(t_new),
                               interp_y(t_new))).tolist()

        # append first data point of new sample period
        [[_, x, y, o]] = self.move_data[-1:]
        self.move_data = [[0., x, y, o]]

        return smoothed


#m = MouseCollector(2, 300)
