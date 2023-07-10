from auborobotcontrol import *

class AuboRobot:
    '''
    Wrapper for Aubo Robot Control
    '''

    JOINT_ACC = (17.308779/2.5, 17.308779/2.5, 17.308779/2.5, 17.308779/2.5, 17.308779/2.5, 17.308779/2.5)
    JOINT_VEL_FAST = (0.9,0.9,0.9,0.9,0.9,0.9)
    JOINT_VEL_SLOW = (0.5,0.5,0.5,0.5,0.5,0.5)

    def __init__(self, robot_ip, robot_port):
        print(f"[INFO] Connecting Aubo robot ...")
        Auboi5Robot.initialize()

        self.robot = Auboi5Robot()
        if self.robot.connect(robot_ip, robot_port) != RobotErrorType.RobotError_SUCC:
            raise ValueExeception(f"Cannot connect to robot {robot_ip}:{robot_port}")

        self.robot.enable_robot_event()
        self.robot.init_profile()

        self.robot.set_joint_maxacc(self.JOINT_ACC)
        self.robot.set_joint_maxvelc(self.JOINT_VEL_FAST)

    def disconnect(self):
        self.robot.disconnect()
        Auboi5Robot.uninitialize()

    def move_vertical_axis(self, position):
        assert position in ["up", "down"]
        user_di = RobotUserIoName.user_di_00 if position == "up" else RobotUserIoName.user_di_01
        user_do = RobotUserIoName.user_do_00 if position == "up" else RobotUserIoName.user_do_01
        while not self.robot.get_board_io_status(RobotIOType.User_DI, user_di):
            self.robot.set_board_io_status(RobotIOType.User_DO, user_do, 1)
            time.sleep(1)
            self.robot.set_board_io_status(RobotIOType.User_DO, user_do, 0)

    def slow(self):
        self.robot.set_joint_maxvelc(JOINT_VEL_SLOW)

    def fast(self):
        self.robot.set_joint_maxvelc(JOINT_VEL_FAST)

    def move_joint(self, radians):
        self.robot.move_joint(radians)

    def move_cartesian(self, xyz, rpy):
        self.robot.move_to_target_in_cartesian(xyz, rpy)

    def move_along_x(self, distance):
        waypoint = self.robot.get_current_waypoint()
        waypoint['pos'][0] += distance
        K = self.robot.inverse_kin(waypoint['joint'], waypoint['pos'], waypoint['ori'])
        self.robot.move_line(K['joint'])

    def move_along_y(self, distance):
        waypoint = self.robot.get_current_waypoint()
        waypoint['pos'][1] += distance
        K = self.robot.inverse_kin(waypoint['joint'], waypoint['pos'], waypoint['ori'])
        self.robot.move_line(K['joint'])

    def move_along_z(self, distance):
        waypoint = self.robot.get_current_waypoint()
        waypoint['pos'][2] += distance
        K = self.robot.inverse_kin(waypoint['joint'], waypoint['pos'], waypoint['ori'])
        self.robot.move_line(K['joint'])

    def get_current_waypoint(self):
        return self.robot.get_current_waypoint()



    @staticmethod
    def degree2rad(degree):
        return degree / (180 / np.pi)

    @staticmethod
    def rad2degree(rad):
        return rad * (180 / np.pi)


if __name__ == '__main__':

    ROBOT_IP  = "172.28.60.10"

    robot = URRobot(ROBOT_IP)
    print(robot.get_joint_degrees())
