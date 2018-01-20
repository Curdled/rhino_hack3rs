from mouse_collect import MouseCollector
from keyboard_collect import KeyboardCollector
import time, sched
import boto


AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''

def callback(p, data):
    s3_connection = boto.connect_s3()
    bucket = s3_connection.get_bucket('rhino-hack3rs')

schedule = sched.scheduler(time.time, time.sleep)

k = KeyboardCollector(schedule, 5, 100, callback)
m = MouseCollector(schedule, 5, 100, callback)
schedule.run()



