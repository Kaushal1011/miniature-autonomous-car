# get ir sensor status and send data to mother node
import RPi.GPIO as GPIO
import time
# import requests
import zmq
import json

context = zmq.Context()

socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

sensor1 = 2
sensor2 = 3
sensor3 = 4


GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor1, GPIO.IN)
GPIO.setup(sensor2, GPIO.IN)
GPIO.setup(sensor3, GPIO.IN)

print("IR Sensor Ready.....")
print(" ")

try:
    while True:
        obstacle1 = not bool(GPIO.input(sensor1))
        obstacle2 = not bool(GPIO.input(sensor2))
        obstacle3 = not bool(GPIO.input(sensor3))
        new_dict = {}
        new_dict["send_module"] = "Ultrasonic"
        new_dict["action"] = "set"
        new_dict["l_ir"] = obstacle1
        new_dict["c_ir"] = obstacle2
        new_dict['r_ir'] = obstacle3

        socket.send(json.dumps(new_dict).encode('utf-8'))
        socket.recv()
        time.sleep(0.1)

except KeyboardInterrupt:
    GPIO.cleanup()
