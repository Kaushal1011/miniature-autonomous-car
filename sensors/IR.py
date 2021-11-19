# get ir sensor status and send data to mother node
import RPi.GPIO as GPIO
import time
import requests

sensor1 = 2
sensor2 = 3
sensor3 = 4


GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor1,GPIO.IN)
GPIO.setup(sensor2,GPIO.IN)
GPIO.setup(sensor3,GPIO.IN)

print("IR Sensor Ready.....")
print(" ")

try: 
   while True:
        obstacle1=not bool(GPIO.input(sensor1))
        obstacle2=not bool(GPIO.input(sensor2))
        obstacle3=not bool(GPIO.input(sensor3))
          
except KeyboardInterrupt:
    GPIO.cleanup()
