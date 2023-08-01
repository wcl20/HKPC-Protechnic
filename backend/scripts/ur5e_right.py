import argparse
import cv2
import imutils
import numpy as np
import os
import os.path as osp
import sys
from mledge.endpoints.gripper import Gripper
from mledge.endpoints.robot import URRobot
from mledge.endpoints.camera import VideoCapture


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    args = parser.parse_args()

    save_dir = osp.join("images", args.name)
    if osp.exists(save_dir):
        raise Exception(f"{save_dir} already exists")
    else:
        os.makedirs(save_dir)

    ROBOT_IP  = "172.28.60.10"
    HOST_IP   = "172.28.60.2"
    CAMERA_IP = "172.28.60.65"

    gripper = Gripper()
    gripper.connect(ROBOT_IP)
    gripper.activate()

    robot = URRobot(ROBOT_IP)
    capture = VideoCapture(network_ip=HOST_IP, camera_ip=CAMERA_IP)

    start_position = [42.40183144291208, -54.00913780306978, 60.06194146751146, 84.22439703504199, 89.80239830160053, 41.84679661057851]
    intermediate_position = [2.741715199358104, -96.30411799397726, 114.95980548754238, -15.620469384363307, 93.84428568636064, 11.446130048850334]

    # Move to start position
    robot.move_joints(start_position)

    gripper.move_and_wait_for_pos(110, 255, 0)
    robot.move_joints([42.42323384067632, -46.06827108155374, 74.35107970177165, 61.99058766389806, 89.86492185326283, 42.0388546998501], speed=0.1)
    gripper.move_and_wait_for_pos(89, 150, 25)

    robot.move_joints(start_position, speed=0.1)

    # Intermediate Position
    robot.move_joints(intermediate_position)

    # Capture Face 1
    robot.move_joints([2.371952449912297, -38.48160772511081, 92.62407603360353, -144.6692885634845, 89.98843216402416, -93.80304864661777])
    ret, frame = capture.read()
    cv2.imwrite(osp.join(save_dir, "1.JPEG"), frame)

    # Intermediate Position
    robot.move_joints(intermediate_position)

    # Capture Face 2
    robot.move_joints([5.833500218680987, -83.28185411865735, 102.93348160455074, -21.038605735935132, 96.93123066288291, -178.29811675555158])
    ret, frame = capture.read()
    cv2.imwrite(osp.join(save_dir, "2.JPEG"), frame)

    # Capture Face 3
    robot.move_joints([5.013732376759594, -84.23460275551113, 104.2885364943679, -21.441334179966596, 96.11774147235606, -87.86704052198641])
    ret, frame = capture.read()
    cv2.imwrite(osp.join(save_dir, "3.JPEG"), frame)

    # Capture Face 4
    robot.move_joints([8.077467943595352, -83.59011378939154, 104.49803205659053, -22.288373259696556, 99.18415490023328, -1.0195459798734743])
    ret, frame = capture.read()
    cv2.imwrite(osp.join(save_dir, "4.JPEG"), frame)

    # Capture Face 5
    robot.move_joints([8.081151976878926, -84.21630126363007, 103.155817922413, -20.31815055209302, 99.17224305032077, 90.05870115020525])
    ret, frame = capture.read()
    cv2.imwrite(osp.join(save_dir, "5.JPEG"), frame)

    # Intermediate Position
    robot.move_joints(intermediate_position)

    # Drop position
    robot.move_joints([4.175595167952276, -28.395279547550807, 37.12010102662567, 82.63849541165672, 90.33209996230252, 87.00663111958505])
    gripper.move_and_wait_for_pos(110, 255, 0)

    robot.move_joints(start_position)
    capture.release()
