import RPi.GPIO as GPIO
import serial
import sys
import time
import pyglet

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

def connect():
    try:
        return serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    except serial.serialutil.SerialException as e:
        return serial.Serial('/dev/ttyACM1', 9600, timeout=1)

ser = connect()
f = open('sensor.csv', 'w')


GPIO.setmode(GPIO.BCM)

GPIO.setup(19, GPIO.OUT)
GPIO.setup(20, GPIO.IN)

gogo = 0
GPIO.output(19, GPIO.LOW)

cnt = 0

try:
    while True:
        pressed = not GPIO.input(20)
        if pressed and not cnt:
            print('pressed!')
            gogo = 1
            GPIO.output(19, GPIO.HIGH)
            cnt = 3
            play_sound('test.wav')


        read_serial = ser.readline().decode()[:-2]
        read_serial = read_serial.replace('|', ',')
        read_serial = str(int(time.time() *100)) + ',' + read_serial + ',' + str(gogo) + '\n'
        f.write(read_serial)

        if gogo == 1:
            gogo = 0

        GPIO.output(19, GPIO.LOW)
        if cnt:
            cnt -= 1

except serial.serialutil.SerialException as e:
    time.sleep(10)
    ser = connect()

except KeyboardInterrupt:
    GPIO.cleanup()
