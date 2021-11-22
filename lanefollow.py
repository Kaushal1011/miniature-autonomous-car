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
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(800, 600))

# allow the camera to warmup
time.sleep(0.1)


K =0.00333   # Change this based on what happens irl
pwmdiffval=0.8
default_speed = 0.6
tdiff=0.15


MotorDriver.init()
pid = PID_Mod.PID(P=4, I=0.8, D=4,Integrator_max=0.8, Integrator_min=-0.8)
MotorDriver.forward()

count = 0
try:
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        count += 1
        # grab an image from the camera
        image  = frame.array
        #imagenew = cv2.rotate(image, cv2.ROTATE_180)
        
        #MotorDriver.speedcontrol(default_speed-tdiff, default_speed)
        angle = LaneFollow.find_steering_angle(image,roi=[[0, 600], [0, 350], [800, 350], [800, 600]])
        pidval = pid.update(angle-90)
        pwmdiff = pidval*K
        pwmdiff = abs(pwmdiff)
        if pwmdiff > pwmdiffval:
            pwmdiff = pwmdiffval
        # Do lane follow
        print(angle)
        angle=SmoothSignal.smooth_angle(LaneFollow.angle_arr,angle,WINDOW_SIZE=2)
        print(angle)
        print(pwmdiff)
        
        if abs(angle-90>6):
            if angle-90 < 6:
                MotorDriver.speedcontrol(0 , pwmdiff )
                
            if angle-90 > 6:
                MotorDriver.speedcontrol(pwmdiff  , 0)
                
            time.sleep(0.2)
            MotorDriver.speedcontrol(0, 0)

        else :
            MotorDriver.speedcontrol(default_speed-tdiff, default_speed)
            time.sleep(0.2)
            MotorDriver.speedcontrol((default_speed-tdiff)/2, (default_speed)/2)
            time.sleep(0.2)
            MotorDriver.speedcontrol(0, 0)
        rawCapture.truncate(0)
        
except KeyboardInterrupt or Exception as e:
    print(count)
    print("video out")
    MotorDriver.stop()
    LaneFollow.save_videos()


    #time.sleep(0.02)
