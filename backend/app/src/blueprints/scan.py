import zivid
from ..app import socketio
from flask import Blueprint
from flask import jsonify
from flask import request
from endpoints.robot import URRobot
from endpoints.turntable import Turntable

scan = Blueprint(name="scan", import_name=__name__)

@socketio.on("scan")
def scan():
    ROBOT_IP  = "172.28.60.10"
    robot = URRobot(ROBOT_IP)
    print("[INFO] Connected to robot.")

    TURNTABLE_COMPORT = "/dev/ttyUSB0"
    turntable = Turntable(TURNTABLE_COMPORT)
    print("[INFO] Connected to turntable.")

    turntable.move(0, speed=1000)
    current_position = turntable.get_position()
    while abs(current_position - 0) > 10:
        current_position = turntable.get_position()

    app = zivid.Application()
    camera = app.connect_camera()
    settings = zivid.Settings(acquisitions=[zivid.Settings.Acquisition()])
    print("[INFO] Connected to zivid.")

    socketio.emit('scan/scanning')

    speed = 0.5
    robot.move_joints([6.512225934902086, -97.5513105364216, 129.0379728387192, -177.38458329152496, -91.85674526148762, -176.55229308293966], speed=speed)
    frame = camera.capture(settings)

    robot.move_joints([6.5204550321914825, -70.54741122723827, 108.9834446052946, -178.69617085746415, -91.99501561104535, -176.53669293087535], speed=speed)
    frame = camera.capture(settings)

    turntable.move(1023, speed=1000)
    current_position = turntable.get_position()
    while abs(current_position - 1023) > 10:
        current_position = turntable.get_position()
    frame = camera.capture(settings)

    turntable.move(2047, speed=1000)
    current_position = turntable.get_position()
    while abs(current_position - 2047) > 10:
        current_position = turntable.get_position()
    frame = camera.capture(settings)

    turntable.move(3071, speed=1000)
    current_position = turntable.get_position()
    while abs(current_position - 3071) > 10:
        current_position = turntable.get_position()
    frame = camera.capture(settings)

    socketio.emit('scan/done')

    robot.move_joints([6.512225934902086, -97.5513105364216, 129.0379728387192, -177.38458329152496, -91.85674526148762, -176.55229308293966], speed=speed)
