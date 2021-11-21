# define function here
import RPi.GPIO as GPIO
import time
pwm1_c = 0
pwm2_c = 0

m11 = 18
m12 = 23
m21 = 24
m22 = 25
pwm1 = 5
pwm2 = 6


def init():

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(m11, GPIO.OUT)
    GPIO.setup(m12, GPIO.OUT)
    GPIO.setup(m21, GPIO.OUT)
    GPIO.setup(m22, GPIO.OUT)
    GPIO.setup(pwm1, GPIO.OUT)
    GPIO.setup(pwm2, GPIO.OUT)
    GPIO.output(m11, 0)
    GPIO.output(m12, 0)
    GPIO.output(m21, 0)
    GPIO.output(m22, 0)
    global pwm1_c,pwm2_c

    pwm1_c = GPIO.PWM(pwm1, 100)
    pwm2_c = GPIO.PWM(pwm2, 100)
    pwm1_c.start(0)
    pwm2_c.start(0)


def forward():
    GPIO.output(m11, 1)
    GPIO.output(m12, 0)
    GPIO.output(m21, 1)
    GPIO.output(m22, 0)
    return 'true'


def back():
    GPIO.output(m11, 0)
    GPIO.output(m12, 1)
    GPIO.output(m21, 0)
    GPIO.output(m22, 1)
    return 'true'


def stop():
    GPIO.output(m11, 0)
    GPIO.output(m12, 0)
    GPIO.output(m21, 0)
    GPIO.output(m22, 0)
    return 'true'


#default is full

# params should be in [0,1]
def speedcontrol(valuel=0, valuer=0):
    global pwm1_c,pwm2_c
    pwm1_c.ChangeDutyCycle(valuel*100)
    pwm2_c.ChangeDutyCycle(valuer*100)
    return True

if __name__=="__main__":
 init()
 stop()
 forward()
 speedcontrol(0.4,0.5)
 time.sleep(3)
 stop()
#time.sleep(0.4)
#speedcontrol(0.8,0.1)
#time.sleep(1)
#speedcontrol(0.5,0.5)
#time.sleep(0.5)
#speedcontrol(0,0)