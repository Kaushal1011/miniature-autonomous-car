from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

from physics import PID_Mod, SmoothSignal
from control import MotorDriver
from vision import Camera
from mobility import LaneFollow

K = 5  # Change this based on what happens irl

default_speed = 0.3
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
rawCapture = PiRGBArray(camera)

# allow the camera to warmup
time.sleep(0.1)

MotorDriver.init()
pid = PID_Mod.PID(P=2, I=0.9, D=1)

count = 0

while True:
    count += 1
    # grab an image from the camera
    camera.capture(rawCapture, format="bgr")
    image = rawCapture.array
    angle = LaneFollow.find_steering_angle(image)
    pidval = pid.update(angle-90)
    pwmdiff = pidval*K
    pwmdiff = abs(pwmdiff)
    if pwmdiff > 0.5:
        pwmdiff = 0.5
    # Do lane follow
    if pwmdiff < 0:
        MotorDriver.speedcontrol(default_speed, default_speed+pwmdiff)
    if pwmdiff > 0:
        MotorDriver.speedcontrol(default_speed+pwmdiff, default_speed)

    if count == 100:
        LaneFollow.save_videos()

    time.sleep(0.02)
