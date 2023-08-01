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

    start_position = [42.375801591985166, -53.92213143832757, 64.5665331874049, 78.52469979531473, 89.57366892667514, 39.43169294648077]
    intermediate_position = [2.741715199358104, -96.30411799397726, 114.95980548754238, -15.620469384363307, 93.84428568636064, 11.446130048850334]

    # Move to start position
    # robot.move_joints(intermediate_position)
    robot.move_joints(start_position)

    gripper.move_and_wait_for_pos(110, 255, 0)
    robot.move_joints([42.389926423188754, -46.782189774360155, 75.16034783539145, 60.78608380376631, 89.62782549660417, 39.58391737251285], speed=0.1)
    gripper.move_and_wait_for_pos(90, 150, 60)

    robot.move_joints(start_position, speed=0.1)
    # gripper.move_and_wait_for_pos(110, 255, 0)

    # Intermediate Position
    robot.move_joints(intermediate_position)

    # Capture Face 1
    robot.move_joints([4.845535980240268, -37.55687865866654, 90.34888537955892, -143.31614612663495, 89.9815678239083, -96.27330950335794])
    ret, frame = capture.read()
    cv2.imwrite(osp.join(save_dir, "1.JPEG"), frame)

    # Intermediate Position
    robot.move_joints(intermediate_position)

    # Capture Face 2
    robot.move_joints([5.960709503764713, -83.99731429978206, 105.1711881804303, -22.56410799648997, 97.07121538992233, -178.3092499638987])
    ret, frame = capture.read()
    cv2.imwrite(osp.join(save_dir, "2.JPEG"), frame)

    # Capture Face 3
    robot.move_joints([9.55656163006089, -82.45041433721805, 103.41618473357387, -22.342365905085508, 100.6663605916394, -90.05756415107953])
    ret, frame = capture.read()
    cv2.imwrite(osp.join(save_dir, "3.JPEG"), frame)

    # Capture Face 4
    robot.move_joints([7.759479949048945, -83.2518106778194, 104.32877996895762, -22.46601964981942, 98.86740487747394, 3.7644818129409763])
    ret, frame = capture.read()
    cv2.imwrite(osp.join(save_dir, "4.JPEG"), frame)

    # Capture Face 5
    robot.move_joints([5.769375414545146, -84.07064534514544, 105.25271331836358, -22.57325361978862, 96.88259971599243, 92.94400528205043])
    ret, frame = capture.read()
    cv2.imwrite(osp.join(save_dir, "5.JPEG"), frame)

    # Intermediate Position
    robot.move_joints(intermediate_position)

    # Drop position
    robot.move_joints([4.175595167952276, -28.395279547550807, 37.12010102662567, 82.63849541165672, 90.33209996230252, 87.00663111958505])
    gripper.move_and_wait_for_pos(110, 255, 0)

    robot.move_joints(start_position)
    capture.release()
