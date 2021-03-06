# get ultrasonic status and send data to mother node
# Libraries
import RPi.GPIO as GPIO
import time
# import requests
import zmq
import json

# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

# set GPIO Pins
GPIO_TRIGGER = 21
GPIO_ECHO = 26

# set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)


context = zmq.Context()

socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")


def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return distance


if __name__ == '__main__':
    # URL = "https://api.thingspeak.com/update"

    try:
        while True:
            dist = distance()

            print("Measured Distance = %.1f cm" % dist)
            new_dict = {}
            new_dict["send_module"] = "Ultrasonic"
            new_dict["action"] = "set"
            new_dict["b_dist"] = dist

            socket.send(json.dumps(new_dict).encode('utf-8'))
            socket.recv()

            time.sleep(0.1)
            # PARAMS = {'api_key':'2FW6VH3PCNKWQ1MU','field1':dist}
            # r = requests.get(url = URL, params = PARAMS)
            # data=r.json()
            # print(data)

        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
