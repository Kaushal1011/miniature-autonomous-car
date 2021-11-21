
from states import state_dict, state_dict_store, nav_dict
import time
import zmq
import json
import logging

logging.basicConfig(filename='example.log', level=logging.DEBUG)

states = state_dict.keys()
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")


def set(statename, stateval):
    if statename in states:
        print("in")
        state_dict[statename] = stateval
        state_dict_store[statename].append(stateval)


def main():

    while True:
        #  Wait for next request from client
        message = socket.recv()
        message_dict = json.loads(message.decode('utf-8'))
        sender = message_dict.pop("send_module")
        logging.info("Message Received from " + sender)
        action = message_dict.pop("action")
        if action == "set":
            logging.info(str(message_dict))
            for i, j in message_dict.items():
                set(i, j)
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
    main()
