
from states import state_dict, nav_dict
import time
import zmq
import json
import logging

logging.basicConfig(filename='example.log',
                    encoding='utf-8', level=logging.DEBUG)

states = ["l_dist", "r_dist", "b_dist", "l_ir",
          "c_ir", "r_ir", "speed", "mob_state", "tot_dist"]
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")


def set(statename, stateval):
    if statename in states:
        print("in")
        state_dict[statename] = stateval


def main():

    while True:
        #  Wait for next request from client
        message = socket.recv()
        message_dict = json.loads(message.decode('utf-8'))
        sender = message_dict.pop("send_module")
        logging.info("Message Received from " + sender)
        action = message_dict.pop("action")
        if action == "set":
            for i, j in message_dict.items():
                set(i, j)
            if sender!="Ultrasonic" or sender!="IR" or sender!="Wheel_Encoder_L" or sender!="Wheel_Encoder_R":
                socket.send(json.dumps(
                    {"send_module": "mother_node", "action": "received"}).encode('utf-8'))
            # Return Response Here
        elif action == "read":
            new_dict = state_dict
            new_dict["send_module"] = "mother_node"
            new_dict["action"] = "response"
            socket.send(json.dumps(new_dict).encode('utf-8'))
        elif action == "action":
            pass
        else:
            pass

        # start decoding process

        time.sleep(1)


if __name__ == "__main__":
    set("l_dist", 100)
    # print(state_dict)
    logging.info(state_dict)
