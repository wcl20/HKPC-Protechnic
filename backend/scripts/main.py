import cv2
import imutils
import numpy as np
import sys
from mledge.endpoints.camera import VideoCapture
from mledge.endpoints.gripper import Gripper
from mledge.endpoints.robot import URRobot

def capture_and_save(capture, filename):
    ret, frame = capture.read()
    if not ret: raise Exception("Cannot capture image")
    cv2.imwrite(filename, frame)

if __name__ == '__main__':

    ROBOT_IP  = "192.168.8.103"
    HOST_IP   = "192.168.8.117"
    CAMERA_IP = "192.168.8.65"

    capture = VideoCapture(network_ip=HOST_IP, camera_ip=CAMERA_IP)

    gripper = Gripper()
    gripper.connect(ROBOT_IP)
    gripper.activate()

    robot = URRobot(ROBOT_IP)

    # Move to start position
    robot.move_joints([184.99378853758444, -88.16800597757384, 118.00618915830746, 62.16405831571144, 88.62304319799277, -78.73469511108584])
    # Move to position above target
    robot.move_joints([218.32448330984303, -72.90160427686823, 113.66128726120891, 48.255429920112654, 90.86826298195936, -140.39679599450386])
    gripper.move_and_wait_for_pos(110, 255, 0)
    # Move to position to insert pin
    robot.move_joints([218.32859508372337, -69.05530618918061, 115.47410142920033, 42.593667551035644, 90.86551724591301, -140.4139397693206], speed=0.1)
    gripper.move_and_wait_for_pos(90, 150, 25)
    # Move to position to pull out target
    robot.move_joints([218.32035787558434, -80.81618160026888, 106.41901911819095, 63.414010254580454, 90.87716954863706, -140.34879342501702], speed=0.1)

    # Intermediate Position
    robot.move_joints([193.8314249461773, -107.39632720823707, 124.97035931907918, -9.294429442370642, 90.86757996304236, -140.349476443934])

    # Capture Face 1
    robot.move_joints([189.3797808527298, -56.001503288965594, 124.70458299809565, -155.0288370458554, 91.8308552020676, -98.24324534301634])
    # capture_and_save(capture, "1.JPEG")

    # Capture Face 2
    robot.move_joints([191.38817065741534, -92.04006753881076, 125.14914635079343, -31.318401741833437, 101.53656767303406, -90.0])
    # capture_and_save(capture, "2.JPEG")

    # Capture Face 3
    robot.move_joints([191.38817065741534, -92.04006753881076, 125.14914635079343, -31.318401741833437, 101.53656767303406, 0.0], speed=0.5)
    # capture_and_save(capture, "3.JPEG")

    # Capture Face 4
    robot.move_joints([191.38817065741534, -92.04006753881076, 125.14914635079343, -31.318401741833437, 101.53656767303406, 90.0], speed=0.5)
    # capture_and_save(capture, "4.JPEG")

    # Capture Face 5
    robot.move_joints([191.38817065741534, -92.04006753881076, 125.14914635079343, -31.318401741833437, 101.53656767303406, 180.0], speed=0.5)
    # capture_and_save(capture, "5.JPEG")

    # Intermediate Position
    robot.move_joints([184.99378853758444, -88.16800597757384, 118.00618915830746, 62.16405831571144, 88.62304319799277, -78.73469511108584])

    # Move to position above target
    robot.move_joints([218.317612139538, -77.1963452647022, 110.56442485001176, 55.647811960709156, 90.8703256990887, -140.3741744079728])
    # Slowly descend target
    robot.move_joints([218.32310361163067, -69.87919092762422, 115.14800087746724, 43.73963668998039, 90.86689011393618, -140.4153058071546], speed=0.1)
    gripper.move_and_wait_for_pos(110, 255, 0)
    # Move to position to pull out pin
    robot.move_joints([218.32448330984303, -72.90160427686823, 113.66128726120891, 48.255429920112654, 90.86826298195936, -140.39679599450386], speed=0.1)

    # Move to starting position
    robot.move_joints([184.99378853758444, -88.16800597757384, 118.00618915830746, 62.16405831571144, 88.62304319799277, -78.73469511108584])
