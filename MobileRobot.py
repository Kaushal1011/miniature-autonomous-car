# Main event loop for Mobile Robot

#import format

# Not implemented functions

# def turn_left():

# def turn_right():

# def straight():

# LaneFollow.stabilise()

# Camera.check_node_reach(img)

# Get Camera Image

# denoising angle input

from Navigation import find_path, get_turn_dir, cur_node, found_path, indexnode
from physics import PID_Mod, SmoothSignal
from control import MotorDriver
import zmq
import json
from vision import Camera
from mobility import LaneFollow

context = zmq.Context()

#  Socket to talk to server
# print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

pid = None

# Theta_new=Theta + PIDdiff * K

K = 5  # Change this based on what happens irl

default_speed = 0.3


def start_rob(path):
    found_path = find_path(path)
    cur_node = found_path[0]
    MotorDriver.init()
    pid = PID_Mod.PID(P=2, I=0.9, D=1)


def turn_left():
    return None


def turn_right():
    return None


def straight():
    return None


def obj_avoid(obs1, obs2, obs3):
    if obs1 == 1 or obs2 == 1 or obs3 == 1:
        MotorDriver.speedcontrol(0, 0)
        return True


def rev_avoid(ob1):
    return None


def function_loop():

    try:
        global indexnode, found_path, cur_node
        # define the functionloop here
        # Read Sensor Values

        while True:
            new_dict = {}
            new_dict["send_module"] = "MobileRobot"
            new_dict["action"] = "read"
            socket.send(json.dumps(new_dict).encode('utf-8'))
            #  Get the reply.
            message = socket.recv()
            message_dict = json.loads(message.decode('utf-8'))

            # Check Actions on Sensor Values
            if obj_avoid(message_dict['l_ir'], message_dict['c_ir'], message_dict['r_ir']):
                continue
            if rev_avoid(message_dict['b_dist']):
                continue

            # Get Camera Image
            img = []
            # Check Node Reach if yes turn and update node info , start turn and use stablise lane if last node reach stop
            if Camera.check_node_reach(img):
                turn_dir = get_turn_dir(cur_node, found_path[indexnode+1])
                indexnode += 1
                cur_node = found_path[indexnode]
                if turn_dir == "l":

                    turn_left()
                    LaneFollow.stabilise()
                    continue
                if turn_dir == 'r':
                    turn_right()
                    LaneFollow.stabilise()
                    continue
                if turn_dir == 's':
                    straight()
                    LaneFollow.stabilise()
                    continue

            # Get steering angle, smooth steering angle, get PWM control with PID, send signal.
            angle = LaneFollow.find_steering_angle(img)
            smooth_angle = SmoothSignal.smooth_angle(
                LaneFollow.angle_arr, angle)
            # write some logic to select either one here
            pidval = pid.update(angle-90)
            pwmdiff = pidval*K
            pwmdiff = pidval*K
            pwmdiff = abs(pwmdiff)
            if pwmdiff > 0.5:
                pwmdiff = 0.5
            # Do lane follow
            if pwmdiff < 0:
                MotorDriver.speedcontrol(default_speed, default_speed+pwmdiff)
            if pwmdiff > 0:
                MotorDriver.speedcontrol(default_speed+pwmdiff, default_speed)

    except Exception as e:
        print(e)
        print("Exception occured or keyboard interrupt")
