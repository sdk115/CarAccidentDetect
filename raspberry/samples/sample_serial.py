import serial
import sys
import time

def connect():
    try:
        return serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    except serial.serialutil.SerialException as e:
        return serial.Serial('/dev/ttyACM1', 9600, timeout=1)

ser = connect()

while True:
    try:
        read_serial = ser.readline().decode()[:-2]
        print(read_serial.split('|'))
    except serial.serialutil.SerialException as e:
        time.sleep(10)
        ser = connect()