import tensorflow as tf
import time
import os
import pyglet
import sys
import time
import csv
import queue
import feature_extration
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.IN)

def connect():
    try:
        return serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    except serial.serialutil.SerialException as e:
        return serial.Serial('/dev/ttyACM1', 9600, timeout=1)

def load_tensor_model():
    print("load tensor model")


# load dummy data
index = 0
dummy = []
with open('../data/sensor.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        dummy.append( [float(i) for i in row[0].split(",")])

def load_sensor_value():
    global index

    len_dummy = len(dummy)
    temp_index = (index) % len_dummy
    index += 1

    ret = dummy[temp_index][1:]

    return ret

def insert_value_to_DB(sensor_value):
    print("insert value to DB")

def make_feature(sensor_values):
    print("feature_extration !!")
    return feature_extration.average_pooling(sensor_values,3,1)

#return true or false
def detect_accident(feature):
    print("dectect_acctident")
    return True

def play_sound(file_name):
    print("play", file_name, "!!")

    player = pyglet.media.Player()

    file_path = '../sound/'
    sound = pyglet.media.load(file_path+file_name, streaming=False)
    player.queue(sound)
    player.play()

    time.sleep(sound.duration)

    # mixer.init()
    # mixer.music.load('../sound'+file_name)
    # mixer.music.play()

def get_shortest_distance():
    return 101

# if (cancel btn pushed ) return true
def wait_cancel_btn(wating=5):
    print("now wating cancel button")
    timeout = time.time() + wating
    while True:
        if time.time() > timeout:
            break
        time.sleep(0.05)

        pressed = not GPIO.input(20)
        if pressed :
            return True

    print("cancel btn not pushed")
    return False

def report_accident():
    print("accident reported")


model = load_tensor_model()
# play_sound("alert_200m.wav", 7)

sensor_value_queue = queue.Queue()
window_size = 32

flag500 = False
flag200 = False
flag100 = False

while True:

    time.sleep(0.05)

    # load sensor data
    try:
        sensor_value = load_sensor_value()
        sensor_value_queue.put(sensor_value)

        if sensor_value_queue.qsize() > window_size:
            sensor_value_queue.get()
        else:
            continue
    except Exception as ex:
        print("load sensor data failed")
        print(ex)
        continue

    sensor_value_list = list(sensor_value_queue.queue)

    # not yet
    insert_value_to_DB(sensor_value)
    feature = make_feature(sensor_value_list)

    if sensor_value_list[-1][-1] == 1:
    # if detect_accident(feature):
        play_sound("detect_accident.wav")

        # true : cancel / false : not canceld
        if wait_cancel_btn():
            play_sound("cancel.wav")
            continue
        else:
            report_accident()
            play_sound("register_accident.wav")

    shortest_distance = get_shortest_distance()

    if shortest_distance > 500:
        flag500 = False
        flag200 = False
        flag100 = False
    elif (not flag500) and shortest_distance <500 and shortest_distance >200 :
        play_sound("alert_500m")
        flag500 = True
    elif (not flag200) and shortest_distance < 200 and shortest_distance >100 :
        play_sound("alert_200m")
        flag200 = True
    elif (not flag100) and shortest_distance < 100:
        play_sound("alert_100m")
        flag100 = True
