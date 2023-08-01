from mledge.endpoints.robot import URRobot

if __name__ == '__main__':

    ROBOT_IP  = "172.28.60.10"

    robot = URRobot(ROBOT_IP)
    print(robot.get_joint_degrees())
