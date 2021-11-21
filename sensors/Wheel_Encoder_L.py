# get wheel encoders status and send data to mother node
#!/usr/bin/python3
import RPi.GPIO as GPIO
from time import sleep
import time
import math

import zmq
import json

context = zmq.Context()

socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")


dist_meas = 0.00
km_per_hour = 0
rpm = 0
elapse = 0
sensor = 16
radius = 6
km_per_sec =0

pulse = 0
start_timer = time.time()


def init_GPIO():                    # initialize GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(sensor, GPIO.IN, GPIO.PUD_UP)


def calculate_elapse(channel):              # callback function
    global pulse, start_timer, elapse
    # increase pulse by 1 whenever interrupt occurred
    pulse += 1
    # elapse for every 1 complete rotation made!
    elapse = time.time() - start_timer
    start_timer = time.time()               # let current time equals to start_timer


def calculate_speed(r_cm):
    global pulse, elapse, rpm, dist_km, dist_meas, km_per_sec, km_per_hour
    if elapse != 0:                          # to avoid DivisionByZero error
        rpm = 1/elapse * 60
        # calculate wheel circumference in CM
        circ_cm = (2*math.pi)*r_cm
        dist_km = circ_cm/100000            # convert cm to km
        km_per_sec = dist_km / elapse       # calculate KM/sec
        km_per_hour = km_per_sec * 3600     # calculate KM/h
        # measure distance traverse in meter
        dist_meas = (circ_cm*pulse)/24
        return km_per_hour


def init_interrupt():
    GPIO.add_event_detect(sensor, GPIO.FALLING,
                          callback=calculate_elapse, bouncetime=20)


if __name__ == '__main__':
    init_GPIO()
    init_interrupt()
    while True:
        # call this function with wheel radius as parameter
        calculate_speed(radius)
        # send speed and distance from both wheels to mother_node
        new_dict = {}
        new_dict["send_module"] = "Wheel_Encoder_L"
        new_dict["action"] = "set"
        new_dict["l_dist"] = dist_meas
        new_dict["l_speed"] = km_per_sec*1000
        socket.send(json.dumps(new_dict).encode('utf-8'))
        socket.recv()
        #print('rpm:{0:.0f}-RPM kmh:{1:.0f}-KMH dist_meas:{2:.2f}m pulse:{3}'.format(rpm,km_per_hour,dist_meas,pulse))
        sleep(0.1)
