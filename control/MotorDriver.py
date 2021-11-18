# define function here
pwm1_c=0
pwm2_c=0

def init():
    import RPi.GPIO as GPIO
    m11=18
    m12=23
    m21=24
    m22=25
    pwm1=5
    pwm2=6

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(m11, GPIO.OUT)
    GPIO.setup(m12, GPIO.OUT)
    GPIO.setup(m21, GPIO.OUT)
    GPIO.setup(m22, GPIO.OUT)
    GPIO.setup(pwm1, GPIO.OUT)
    GPIO.setup(pwm2, GPIO.OUT)
    GPIO.output(m11 , 0)
    GPIO.output(m12 , 0)
    GPIO.output(m21, 0)
    GPIO.output(m22, 0)
    
    pwm1_c=GPIO.PWM(pwm1,100)
    pwm2_c=GPIO.PWM(pwm2,100)
    pwm1_c.start(0)
    pwm2_c.start(0)
    

def forward():
    GPIO.output(m11 , 1)
    GPIO.output(m12 , 0)
    GPIO.output(m21 , 1)
    GPIO.output(m22 , 0)
    return 'true'



def back():
    GPIO.output(m11 , 1)
    GPIO.output(m12 , 0)
    GPIO.output(m21 , 1)
    GPIO.output(m22 , 0)
    return 'true'

#default is full

#params should be in [0,1] 
def speedcontrol(valuel=0, valuer=0):
   
    pwm1_c.ChangeDutyCycle(valuel*100)
    pwm2_c.ChangeDutyCycle(valuer*100)
    return True
