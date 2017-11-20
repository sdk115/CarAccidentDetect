import tensorflow as tf
import time
import os
import pyglet

def load_tensor_model():
    print("load model")

def load_sensor_value():
    print("load sensor value")
    return []

def insert_value_to_DB(sensor_value):
    print("insert value to DB")

def make_feature(sensor_value):
    print("make_feature")
    feature = []
    return feature

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

    time.sleep(wating)

    print("cancel btn not pushed")
    return False

def report_accident():
    print("accident reported")

load_tensor_model()
# play_sound("alert_200m.wav", 7)

while True:
    time.sleep(1)
    sensor_value = load_sensor_value()
    insert_value_to_DB(sensor_value)
    feature = make_feature(sensor_value)

    if detect_accident(feature):
        play_sound("detect_accident.wav")

        # true : cancel / false : not canceld
        if wait_cancel_btn():
            play_sound("cancel.wav")
            continue
        else:
            report_accident()
            play_sound("register_accident.wav")

    shortest_distance = get_shortest_distance()
