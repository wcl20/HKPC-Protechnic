import cv2
import numpy as np
import os
import os.path as osp
import shortuuid
import time
import torch
import zivid
from flask import abort
from flask import Blueprint
from flask import jsonify
from flask import request
from endpoints.robot import URRobot
from endpoints.turntable import Turntable
from endpoints.vimba import VideoCapture

inspection = Blueprint(name="inspection", import_name=__name__)

@inspection.route("/ur5demo", methods=["GET"])
def ur5_demo():

    ROBOT_IP  = "172.28.60.10"
    robot = URRobot(ROBOT_IP)
    print("[INFO] Connected to robot.")

    TURNTABLE_COMPORT = "/dev/ttyUSB0"
    turntable = Turntable(TURNTABLE_COMPORT)
    print("[INFO] Connected to turntable.")

    capture = VideoCapture("../settings/vimba.xml")

    turntable.move(0, speed=1000)
    current_position = turntable.get_position()
    while abs(current_position - 0) > 10:
        current_position = turntable.get_position()

    speed = 0.5
    robot.move_joints([6.512225934902086, -97.5513105364216, 129.0379728387192, -177.38458329152496, -91.85674526148762, -176.55229308293966], speed=speed)

    robot.move_joints([7.022761231019383, -65.83117755817551, 101.29098503370275, -185.15089086842298, -91.71628925139547, -176.43501873489052], speed=speed)
    frame = capture.read()
    cv2.imwrite("static/raw/1.jpeg", frame)

    turntable.move(1023, speed=1000)
    current_position = turntable.get_position()
    while abs(current_position - 1023) > 10:
        current_position = turntable.get_position()
    frame = capture.read()
    cv2.imwrite("static/raw/2.jpeg", frame)

    turntable.move(2047, speed=1000)
    current_position = turntable.get_position()
    while abs(current_position - 2047) > 10:
        current_position = turntable.get_position()
    frame = capture.read()
    cv2.imwrite("static/raw/3.jpeg", frame)

    turntable.move(3071, speed=1000)
    current_position = turntable.get_position()
    while abs(current_position - 3071) > 10:
        current_position = turntable.get_position()
    frame = capture.read()
    cv2.imwrite("static/raw/4.jpeg", frame)

    robot.move_joints([2.888498525942617, -60.48646574018132, 68.31841074000627, -135.83984838189568, -83.63549244435339, -176.4931026635923], speed=speed)
    frame = capture.read()
    cv2.imwrite("static/raw/5.jpeg", frame)

    robot.move_joints([6.512225934902086, -97.5513105364216, 129.0379728387192, -177.38458329152496, -91.85674526148762, -176.55229308293966], speed=speed)

    return jsonify({ "results": [
        { "image": "http://localhost:5000/api/static/raw/1.jpeg", "heatmap": "http://localhost:5000/api/static/prediction/1.JPEG", "error": True },
        { "image": "http://localhost:5000/api/static/raw/2.jpeg", "heatmap": "http://localhost:5000/api/static/prediction/2.JPEG", "error": False },
        { "image": "http://localhost:5000/api/static/raw/3.jpeg", "heatmap": "http://localhost:5000/api/static/prediction/3.JPEG", "error": False },
        { "image": "http://localhost:5000/api/static/raw/4.jpeg", "heatmap": "http://localhost:5000/api/static/prediction/4.JPEG", "error": False },
        { "image": "http://localhost:5000/api/static/raw/5.jpeg", "heatmap": "http://localhost:5000/api/static/prediction/5.JPEG", "error": False },
    ]})
