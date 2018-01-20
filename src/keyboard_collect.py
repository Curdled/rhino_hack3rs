from pynput import keyboard
from ElementCollector import ElementCollector


class KeyboardCollector(ElementCollector):

    source_name = 'keyboard'

    def __init__(self, schedule, samplePeriod,
                 total_sample_time, callback):
        self.listener = keyboard.Listener(
            on_press=self.on_press)
        self.listener.start()
        self.keyboardData = {}
        super().__init__(schedule, samplePeriod,
                         total_sample_time, callback)

    def on_press(self, key):
        key_str = str(key)
        print(key)
        if key_str in self.keyboardData.keys():
            self.keyboardData[key_str] = self.keyboardData[key_str]+1
        else:
            self.keyboardData[key_str] = 1

    def on_sample_time(self):
        self.save_sample(self.keyboardData)
        self.keyboardData = {}


#s = KeyboardCollector(1)
#s.run()
#print("here")