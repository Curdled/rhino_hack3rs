from mouse_collect import MouseCollector
from keyboard_collect import KeyboardCollector
import time, sched
from time import gmtime, strftime

import boto3

import os
import pwd

os.environ["AWS_SHARED_CREDENTIALS_FILE"] = "/Users/josi2/.aws/credentials"

BUCKET = 'rhino-hack3rs'

s3 = boto3.resource('s3')

f_str = strftime("%Y-%b-%d-%H:%M:%S", gmtime())

def get_username():
    return pwd.getpwuid( os.getuid() )[ 0 ]

def change_f_name(p, input_type, data):
    global f_str
    save_to_s3(p, input_type, data)
    f_str = strftime("%Y-%b-%d-%H:%M:%S", gmtime())


def save_to_s3(p, input_type, data):
    key = f_str + '/' + get_username() + '-sample-' + input_type + "-" + str(p)
    s3.Bucket(BUCKET).put_object(Body=data, Key=key,
                                 ContentType='text/json')


schedule = sched.scheduler(time.time, time.sleep)

bin_size = 1
total_bins = 360

k = KeyboardCollector(schedule, bin_size,  total_bins, save_to_s3)
m = MouseCollector(schedule, bin_size,     total_bins, change_f_name)
schedule.run()



