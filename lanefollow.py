from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
from physics import PID_Mod, SmoothSignal
from control import MotorDriver
from vision import Camera
from mobility import LaneFollow


# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (800, 600)
camera.framerate = 20
rawCapture = PiRGBArray(camera, size=(800, 600))

# allow the camera to warmup
time.sleep(0.1)


K =0.03333   # Change this based on what happens irl

default_speed = 0.45
tdiff=0.15


MotorDriver.init()
pid = PID_Mod.PID(P=1, I=0.03, D=0.5)
MotorDriver.forward()

count = 0
try:
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        count += 1
        # grab an image from the camera
        image  = frame.array
        #imagenew = cv2.rotate(image, cv2.ROTATE_180)
        
        #MotorDriver.speedcontrol(default_speed-tdiff, default_speed)
        angle = LaneFollow.find_steering_angle(image)
        pidval = pid.update(angle-90)
        pwmdiff = pidval*K
        pwmdiff = abs(pwmdiff)
        if pwmdiff > 0.3:
            pwmdiff = 0.3
        # Do lane follow
        print(angle)
        angle=SmoothSignal.smooth_angle(LaneFollow.angle_arr,angle)
        print(pwmdiff)
        
        if abs(angle-90>5):
            if angle-90 < 10:
                MotorDriver.speedcontrol(0, pwmdiff/2.5)
            if angle-90 > 10:
                MotorDriver.speedcontrol(pwmdiff/2.5, 0)
            if angle-90 < 10:
                MotorDriver.speedcontrol(0, pwmdiff/2)
            if angle-90 > 10:
                MotorDriver.speedcontrol(pwmdiff/2, 0)
            if angle-90 < 20:
                MotorDriver.speedcontrol(0, pwmdiff)
            if angle-90 > 20:
                MotorDriver.speedcontrol(pwmdiff-tdiff, 0)

        else :
            MotorDriver.speedcontrol(default_speed-tdiff, default_speed)
        rawCapture.truncate(0)
except KeyboardInterrupt:
    print(count)
    print("video out")
    MotorDriver.stop()
    LaneFollow.save_videos()

    #time.sleep(0.02)
