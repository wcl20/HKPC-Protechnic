import numpy as np
from rtde_receive import RTDEReceiveInterface as RTDEReceive
from rtde_control import RTDEControlInterface as RTDEControl

class URRobot:

    def __init__(self, robot_ip):
        print(f"[INFO] Connecting UR robot ...")
        self.rtde_receive = RTDEReceive(robot_ip, rt_priority=90)
        self.rtde_control = RTDEControl(robot_ip, rt_priority=85)

    @staticmethod
    def degree2rad(degree):
        return degree / (180 / np.pi)

    @staticmethod
    def rad2degree(rad):
        return rad * (180 / np.pi)

    def move_joints(self, joint_degrees, speed=1):
        joint_radians = list(map(URRobot.degree2rad, joint_degrees))
        self.rtde_control.moveJ(joint_radians, speed=speed, acceleration=1)

    def get_joint_degrees(self):
        joint_radians = self.rtde_receive.getActualQ()
        joint_degrees = list(map(URRobot.rad2degree, joint_radians))
        return joint_degrees

if __name__ == '__main__':
    
    ROBOT_IP  = "172.28.60.10"

    robot = URRobot(ROBOT_IP)
    print(robot.get_joint_degrees())
