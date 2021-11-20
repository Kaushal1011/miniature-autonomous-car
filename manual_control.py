import time
import RPi.GPIO as GPIO
from flask import render_template, request
from flask import Flask
from control import MotorDriver

MotorDriver.init()


app = Flask(__name__)

print("DOne")


@app.route("/")
def index():
    return "hello"


@app.route('/left_side')
def left_side():
    data1 = "LEFT"

    MotorDriver.forward()
    MotorDriver.speedcontrol(0.5, 0)

    return 'true'


@app.route('/right_side')
def right_side():
    data1 = "RIGHT"
    MotorDriver.forward()
    MotorDriver.speedcontrol(0, 0.5)

    return 'true'


@app.route('/up_side')
def up_side():
    data1 = "FORWARD"
    MotorDriver.forward()
    MotorDriver.speedcontrol(0.5, 0.5)
    return 'true'


@app.route('/down_side')
def down_side():
    data1 = "BACK"
    MotorDriver.back()
    MotorDriver.speedcontrol(0.5, 0.5)

    return 'true'


@app.route('/tt')
def tt():
    data1 = "BACK"
    MotorDriver.forward()
    MotorDriver.speedcontrol(0, 0.5)
    time.sleep(0.5)
    MotorDriver.back()

    return 'true'


@app.route('/stop')
def stop():
    MotorDriver.stop()

    return 'true'


if __name__ == "__main__":
    print("Start")
    app.run(host='0.0.0.0', port=5010)
