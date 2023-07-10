from robotcontrol import *
from camera import VideoCapture

import serial
import time
import binascii
import numpy as np

def test_jim():
    # 初始化logger
    logger_init()

    # 启动测试
    logger.info("{0} test beginning...".format(Auboi5Robot.get_local_time()))

    # 系统初始化
    Auboi5Robot.initialize()

    # 创建机械臂控制类
    robot = Auboi5Robot()

    # 创建上下文
    handle = robot.create_context()

    # 打印上下文
    logger.info("robot.rshd={0}".format(handle))

    try:

        # time.sleep(0.2)
        # process_get_robot_current_status = GetRobotWaypointProcess()
        # process_get_robot_current_status.daemon = True
        # process_get_robot_current_status.start()
        # time.sleep(0.2)

        queue = Queue()

        p = Process(target=runWaypoint, args=(queue,))
        p.start()
        time.sleep(5)
        print("process started.")

        # 链接服务器
        #ip = 'localhost'
        # ip = '192.168.109.129'
        ip = '169.254.88.2'

        port = 8899
        result = robot.connect(ip, port)

        if result != RobotErrorType.RobotError_SUCC:
            logger.info("connect server{0}:{1} failed.".format(ip, port))
        else:
            robot.enable_robot_event()
            robot.init_profile()
            joint_maxvelc = (2.596177, 2.596177, 2.596177, 3.110177, 3.110177, 3.110177)
            joint_maxacc = (17.308779/2.5, 17.308779/2.5, 17.308779/2.5, 17.308779/2.5, 17.308779/2.5, 17.308779/2.5)
            robot.set_joint_maxacc(joint_maxacc)
            robot.set_joint_maxvelc(joint_maxvelc)
            robot.set_arrival_ahead_blend(0.05)
            while True:
                time.sleep(1)

                # joint_radian = (0.541678, 0.225068, -0.948709, 0.397018, -1.570800, 0.541673)
                # robot.move_joint(joint_radian, True)
                

                # joint_radian = (55.5/180.0*pi, -20.5/180.0*pi, -72.5/180.0*pi, 38.5/180.0*pi, -90.5/180.0*pi, 55.5/180.0*pi)
                # robot.move_joint(joint_radian, True)

                joint_radian = (0, 0, -pi/2, -pi/4, -pi/2, 0)
                robot.move_joint(joint_radian, True)
                time.sleep(1)
                # robot.move_to_target_in_cartesian(pos, rpy_xyz):
                robot.move_to_target_in_cartesian((-0.3,-0.3,0.3),(0,-180,90))

                
                # # 坐标系默认使用基座坐标系（默认填写下面的值就可以了）
                # user_coord = {'coord_type': RobotCoordType.Robot_Base_Coordinate,
                #             'calibrate_method': 0,
                #             'calibrate_points':
                #                 {"point1": (0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
                #                 "point2": (0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
                #                 "point3": (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)},
                #             'tool_desc':
                #                 {"pos": (0.0, 0.0, 0.0),
                #                 "ori": (1.0, 0.0, 0.0, 0.0)}
                #             }

                # rotate_axis = (1,0,0)
                # # 调用转轴旋转接口，最后一个参数为旋转角度（弧度）
                # robot.move_rotate(user_coord, rotate_axis, 0.1)

                # robot.move_rotate(user_coord, rotate_axis, rotate_angle):
                current_pos = robot.get_current_waypoint()
                initial_pos = -2*pi*170/360
                current_pos['joint'][5] = initial_pos
                robot.move_joint(current_pos['joint'], True)
                
                for i in range(3):
                    # current_pos = robot.get_current_waypoint()
                    initial_pos += pi/2
                    current_pos['joint'][5] = initial_pos

                    robot.move_joint(current_pos['joint'], True)
                    time.sleep(1)
                print("-----------------------------")

                queue.put(joint_radian)

                # time.sleep(5)

                # process_get_robot_current_status.test()

                # print("-----------------------------")

                # 断开服务器链接
            robot.disconnect()

    except KeyboardInterrupt:
        robot.move_stop()

    except RobotError as e:
        logger.error("robot Event:{0}".format(e))



    finally:
        # 断开服务器链接
        if robot.connected:
            # 断开机械臂链接
            robot.disconnect()
        # 释放库资源
        Auboi5Robot.uninitialize()
        print("run end-------------------------")

def test_jim_VM():
    # 系统初始化
    Auboi5Robot.initialize()

    # 创建机械臂控制类
    robot = Auboi5Robot()
    
    # 创建上下文
    handle = robot.create_context()

    # 打印上下文
    print("robot.rshd={0}".format(handle))


    try:
        # 链接服务器
        #ip = 'localhost'
        # ip = '192.168.109.129'

        ip = '169.254.88.2'
        port = 8899
        result = robot.connect(ip, port)

        if result != RobotErrorType.RobotError_SUCC:
            print("connect server{0}:{1} failed.".format(ip, port))
        else:
            robot.enable_robot_event()
            robot.init_profile()
            joint_maxvelc = (1,1,1,1,1,1)

            # joint_maxvelc = (2.596177, 2.596177, 2.596177, 3.110177, 3.110177, 3.110177)
            joint_maxacc = (17.308779/2.5, 17.308779/2.5, 17.308779/2.5, 17.308779/2.5, 17.308779/2.5, 17.308779/2.5)
            robot.set_joint_maxacc(joint_maxacc)
            robot.set_joint_maxvelc(joint_maxvelc)
            robot.set_arrival_ahead_blend(0.05)
            while True:
                time.sleep(1)

                # joint_radian = (0.541678, 0.225068, -0.948709, 0.397018, -1.570800, 0.541673)
                # robot.move_joint(joint_radian, True)
                

                # joint_radian = (55.5/180.0*pi, -20.5/180.0*pi, -72.5/180.0*pi, 38.5/180.0*pi, -90.5/180.0*pi, 55.5/180.0*pi)
                # robot.move_joint(joint_radian, True)

                joint_radian = (0.01, 0.01, -pi/2, 0.01, -pi/2, 0.01)
                robot.move_joint(joint_radian, True)
                print("move to home")
                time.sleep(1)
                # robot.move_to_target_in_cartesian(pos, rpy_xyz):
                robot.move_to_target_in_cartesian((-0.4,-0.4,0.1),(0.01,-180,90))
                print("move to pick pos")
                time.sleep(1)
                robot.move_to_target_in_cartesian((-0.4,-0.2,0.4),(0.01,-90,0.01))
                print("move to ready pos")
                time.sleep(1)
                
                # # 坐标系默认使用基座坐标系（默认填写下面的值就可以了）
                # user_coord = {'coord_type': RobotCoordType.Robot_Base_Coordinate,
                #             'calibrate_method': 0,
                #             'calibrate_points':
                #                 {"point1": (0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
                #                 "point2": (0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
                #                 "point3": (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)},
                #             'tool_desc':
                #                 {"pos": (0.0, 0.0, 0.0),
                #                 "ori": (1.0, 0.0, 0.0, 0.0)}
                #             }

                # rotate_axis = (1,0,0)
                # # 调用转轴旋转接口，最后一个参数为旋转角度（弧度）
                # robot.move_rotate(user_coord, rotate_axis, 1.5)

                # robot.move_rotate(user_coord, rotate_axis, rotate_angle):

                current_pos = robot.get_current_waypoint()
                # initial_pos = -2*pi*160/360
                initial_pos = -2*pi*160/360
                print("initial yaw radians", initial_pos)

                next_pos = current_pos['joint']
                next_pos[5] = initial_pos
                print(next_pos)
                robot.move_joint(next_pos, True)
                print("move to initial pos")
                print("initial yaw radians", initial_pos)
                time.sleep(1)
                for i in range(3):
                    # current_pos = robot.get_current_waypoint()
                    initial_pos += pi/2
                    print("next yaw radians", initial_pos)

                    next_pos[5] = initial_pos

                    robot.move_joint(next_pos, True)
                    print("move to next pos")
                    time.sleep(1)
                print("-----------------------------")

                print("home radians",joint_radian)

                # time.sleep(5)

                # process_get_robot_current_status.test()

                # print("-----------------------------")

                # 断开服务器链接
            robot.disconnect()

    except KeyboardInterrupt:
        robot.move_stop()

    except RobotError as e:
        print("robot Event:{0}".format(e))
        robot.move_stop()
        robot.disconnect()


    finally:
        # 断开服务器链接
        if robot.connected:
            # 断开机械臂链接
            robot.disconnect()
        # 释放库资源
        Auboi5Robot.uninitialize()
        print("run end-------------------------")


def test_get_joints_real():
    Auboi5Robot.initialize()
    robot = Auboi5Robot()
    handle = robot.create_context()
    print("robot.rshd={0}".format(handle))

    try: 
        ip = '192.168.56.10'
        port = 8899
        result = robot.connect(ip, port)

        if result != RobotErrorType.RobotError_SUCC:
            print("connect server{0}:{1} failed.".format(ip, port))
        else:
            robot.enable_robot_event()
            robot.init_profile()
            joint_maxvelc = (1,1,1,1,1,1)

            # joint_maxvelc = (2.596177, 2.596177, 2.596177, 3.110177, 3.110177, 3.110177)
            joint_maxacc = (17.308779/2.5, 17.308779/2.5, 17.308779/2.5, 17.308779/2.5, 17.308779/2.5, 17.308779/2.5)
            robot.set_joint_maxacc(joint_maxacc)
            robot.set_joint_maxvelc(joint_maxvelc)
            robot.set_arrival_ahead_blend(0.05)
           
                
              
            current_pos = robot.get_current_waypoint()
            print(current_pos['joint'])
                
            robot.disconnect()

    except KeyboardInterrupt:
        robot.move_stop()

    except RobotError as e:
        print("robot Event:{0}".format(e))
        robot.move_stop()
        robot.disconnect()


    finally:
        # 断开服务器链接
        if robot.connected:
            # 断开机械臂链接
            robot.disconnect()
        # 释放库资源
        Auboi5Robot.uninitialize()
        print("run end-------------------------")
    # robot.move_joint(joint_radian)

def test_move_capture():
    Auboi5Robot.initialize()
    robot = Auboi5Robot()
    handle = robot.create_context()
    print("robot.rshd={0}".format(handle))

    # HOST_IP   = "169.254.88.158"
    HOST_IP   = "192.168.56.10"

    # CAMERA_IP = "169.254.208.10"


    capture = VideoCapture(network_ip=HOST_IP, camera_ip=CAMERA_IP)

    try: 
        ip = '169.25\4.88.2'
        port = 8899
        result = robot.connect(ip, port)

        if result != RobotErrorType.RobotError_SUCC:
            print("connect server{0}:{1} failed.".format(ip, port))
        else:
            robot.enable_robot_event()
            robot.init_profile()
            # joint_maxvelc = (1,1,1,1,1,1)
            joint_maxvelc = (0.5,0.5,0.5,0.5,0.5,0.5)

            # joint_maxvelc = (2.596177, 2.596177, 2.596177, 3.110177, 3.110177, 3.110177)
            joint_maxacc = (17.308779/2.5, 17.308779/2.5, 17.308779/2.5, 17.308779/2.5, 17.308779/2.5, 17.308779/2.5)
            robot.set_joint_maxacc(joint_maxacc)
            robot.set_joint_maxvelc(joint_maxvelc)
            robot.set_arrival_ahead_blend(0.05)

            poses = []
            poses.append([0.4701825976371765, 0.4680332541465759, -1.946478247642517, 0.7528040409088135, 1.3659590482711792, 1.5136961936950684])
            poses.append([0.5791407823562622, 0.46387845277786255, -1.9532997608184814, 0.7498549222946167, 1.464654564857483, 3.052569627761841])
            poses.append([0.6016201376914978, 0.3626787066459656, -1.9789847135543823, 0.8253172636032104, 1.4871323108673096, -1.57709801197052])
            poses.append([0.5623961687088013, 0.3780516982078552, -1.9562666416168213, 0.8327670693397522, 1.4479210376739502, -0.029479941353201866])
            poses.append([0.5590343475341797, 0.4678281247615814, -2.018132209777832, -0.8115365505218506, 1.4826499223709106, -1.5345818996429443])
            for i in poses:
            
                robot.move_joint(i)
                time.sleep(2)
                ret, frame = capture.read()
                time.sleep(2)
            robot.disconnect()

    except KeyboardInterrupt:
        robot.move_stop()

    except RobotError as e:
        print("robot Event:{0}".format(e))
        robot.move_stop()
        robot.disconnect()


    finally:
        # 断开服务器链接
        if robot.connected:
            # 断开机械臂链接
            robot.disconnect()
        # 释放库资源
        Auboi5Robot.uninitialize()
        print("run end-------------------------")
    # robot.move_joint(joint_radian)



def test_move_real():
    #robotiq hande gripper modbus
    # ser = serial.Serial(port='COM4',baudrate=115200,timeout=1, parity=serial.PARITY_NONE,
    # stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS)


    # print("Close gripper")
    # ser.write(b"\x09\x10\x03\xE8\x00\x03\x06\x09\x00\x00\xFF\xFF\xFF\x42\x29")
    # data_raw = ser.readline()
    # print(data_raw)
    # data = binascii.hexlify(data_raw)
    # print("Response 3 "), data
    # time.sleep(2)

    # print("Open gripper")
    # ser.write(b"\x09\x10\x03\xE8\x00\x03\x06\x09\x00\x00\x00\xFF\xFF\x72\x19")
    # data_raw = ser.readline()
    # print(data_raw)
    # data = binascii.hexlify(data_raw)
    # print("Response 4 "), data
    # time.sleep(2)

    gripper = Gripper()
    gripper.open()
    gripper.close()
    gripper.open()

    time.sleep(2)

    Auboi5Robot.initialize()
    robot = Auboi5Robot()
    handle = robot.create_context()
    print("robot.rshd={0}".format(handle))

    # HOST_IP   = "192.168.56.10"
    try: 
        ip = '192.168.56.10'
        port = 8899
        result = robot.connect(ip, port)

        if result != RobotErrorType.RobotError_SUCC:
            print("connect server{0}:{1} failed.".format(ip, port))
            # raise Exception()
        else:
            robot.enable_robot_event()
            robot.init_profile()
            # joint_maxvelc = (1,1,1,1,1,1)
            joint_maxvelc = (0.5,0.5,0.5,0.5,0.5,0.5)

            # joint_maxvelc = (2.596177, 2.596177, 2.596177, 3.110177, 3.110177, 3.110177)
            joint_maxacc = (17.308779/2.5, 17.308779/2.5, 17.308779/2.5, 17.308779/2.5, 17.308779/2.5, 17.308779/2.5)
            robot.set_joint_maxacc(joint_maxacc)
            robot.set_joint_maxvelc(joint_maxvelc)
            robot.set_arrival_ahead_blend(0.05)

            
            gripper.open()
            
            robot.move_joint([0.04077628254890442, -0.32949554920196533, 1.8527307510375977, 0.6082250475883484, 1.4683446884155273, -1.3047101497650146])
            
            time.sleep(1)
            gripper.close()

            poses = []
            poses.append([0.04078241065144539, 0.7611889839172363, 1.8028794527053833, -0.4972745478153229, 1.5640031099319458, -1.3048202991485596])
            
            # poses.append([0.6016201376914978, 0.3626787066459656, -1.9789847135543823, 0.8253172636032104, 1.4871323108673096, -1.57709801197052])
            # poses.append([0.5623961687088013, 0.3780516982078552, -1.9562666416168213, 0.8327670693397522, 1.4479210376739502, -0.029479941353201866])
            # poses.append([0.5590343475341797, 0.4678281247615814, -2.018132209777832, -0.8115365505218506, 1.4826499223709106, -1.5345818996429443])
            for i in poses:
            
                robot.move_joint(i)
                time.sleep(2)

            robot.disconnect()

    except KeyboardInterrupt:
        robot.move_stop()

    except RobotError as e:
        print("robot Event:{0}".format(e))
        robot.move_stop()
        robot.disconnect()


    finally:
        # 断开服务器链接
        if robot.connected:
            # 断开机械臂链接
            robot.disconnect()
        # 释放库资源
        Auboi5Robot.uninitialize()
        print("run end-------------------------")
    # robot.move_joint(joint_radian)



class Gripper:

    def __init__(self, port="COM4", baudrate=115200):
        self.ser = serial.Serial(
            port='COM4',
            baudrate=baudrate,
            timeout=1, 
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS)
    
    def close(self):
        print("Close gripper")
        self.ser.write(b"\x09\x10\x03\xE8\x00\x03\x06\x09\x00\x00\xFF\xFF\xFF\x42\x29")
        data = binascii.hexlify(self.ser.readline())
        return data
    
    def open(self):
        print("Open gripper")
        self.ser.write(b"\x09\x10\x03\xE8\x00\x03\x06\x09\x00\x00\x00\xFF\xFF\x72\x19")
        data = binascii.hexlify(self.ser.readline())
        return data
def servo_move_00(robot):
    while not robot.get_board_io_status(RobotIOType.User_DI, RobotUserIoName.user_di_00):
        robot.set_board_io_status(RobotIOType.User_DO, RobotUserIoName.user_do_00, 1)
        time.sleep(1)
        robot.set_board_io_status(RobotIOType.User_DO, RobotUserIoName.user_do_00, 0)
    print("position 1 has been reached")

def servo_move_01(robot):
    while not robot.get_board_io_status(RobotIOType.User_DI, RobotUserIoName.user_di_01):
        robot.set_board_io_status(RobotIOType.User_DO, RobotUserIoName.user_do_01, 1)
        time.sleep(1)
        robot.set_board_io_status(RobotIOType.User_DO, RobotUserIoName.user_do_01, 0)
    print("position 2 has been reached")

def move_along_z(robot,z):
# 沿Ｚ轴运动0.1毫米


    current_pos = robot.get_current_waypoint()
    
    current_pos['pos'][2] += z
    
    ik_result = robot.inverse_kin(current_pos['joint'], current_pos['pos'], current_pos['ori'])
    logger.info(ik_result)
    robot.move_line(ik_result['joint'])

def move_along_y(robot,y):
# 沿Ｚ轴运动0.1毫米


    current_pos = robot.get_current_waypoint()
    
    current_pos['pos'][1] += y
    
    ik_result = robot.inverse_kin(current_pos['joint'], current_pos['pos'], current_pos['ori'])
    logger.info(ik_result)
    robot.move_line(ik_result['joint'])

def move_along_x(robot,x):
# 沿Ｚ轴运动0.1毫米


    current_pos = robot.get_current_waypoint()
    
    current_pos['pos'][0] += x
    
    ik_result = robot.inverse_kin(current_pos['joint'], current_pos['pos'], current_pos['ori'])
    logger.info(ik_result)
    robot.move_line(ik_result['joint'])

def test_gripper():

    gripper = Gripper()
    gripper.open()
    gripper.close()
    gripper.open()

def test_io_servo():

    gripper = Gripper()
    

    Auboi5Robot.initialize()
    robot = Auboi5Robot()
    handle = robot.create_context()
    print("robot.rshd={0}".format(handle))

    # HOST_IP   = "192.168.56.10"
    try: 
        ip = '192.168.56.10'
        port = 8899
        result = robot.connect(ip, port)

        if result != RobotErrorType.RobotError_SUCC:
            print("connect server{0}:{1} failed.".format(ip, port))
            # raise Exception()
        else:
            robot.enable_robot_event()
            robot.init_profile()
            # joint_maxvelc = (1,1,1,1,1,1)
            joint_maxvelc_fast = (0.9,0.9,0.9,0.9,0.9,0.9)
            joint_maxvelc_slow = (0.5,0.5,0.5,0.5,0.5,0.5)

            # joint_maxvelc = (2.596177, 2.596177, 2.596177, 3.110177, 3.110177, 3.110177)
            joint_maxacc = (17.308779/2.5, 17.308779/2.5, 17.308779/2.5, 17.308779/2.5, 17.308779/2.5, 17.308779/2.5)
            robot.set_joint_maxacc(joint_maxacc)
            robot.set_joint_maxvelc(joint_maxvelc_fast)
            # robot.set_arrival_ahead_blend(0.05)
            # robot.set_arrival_ahead_distance(0.1)

            # io_config = robot.get_board_io_config(RobotIOType.User_DO)
            # print("io_status:{}".format(io_config))

            
            servo_move_00(robot)
            # pick_pose = [0.02802106738090515, -0.7555553913116455, 1.3110105991363525, 0.47127923369407654, np.deg2rad(90), np.deg2rad(-90)]
            # robot.move_joint(pick_pose)
            pick_pose_xyz = [0.7,-0.1,0.1684]
            pick_pose_rpy = [-179.9,-1.38,178.4]
            home_pose_xyz= [0.5,-0.1,0.1]
            
            
            # move_along_x(robot,-0.22)
            robot.move_to_target_in_cartesian(home_pose_xyz,pick_pose_rpy)
            gripper.open()
            gripper.close()
            gripper.open()
            servo_move_01(robot)
            #capture image
            servo_move_00(robot)

            robot.move_to_target_in_cartesian(pick_pose_xyz,pick_pose_rpy)
            robot.set_joint_maxvelc(joint_maxvelc_slow)
            move_along_z(robot,-0.1)
            gripper.close()
            move_along_z(robot,0.1)
            robot.set_joint_maxvelc(joint_maxvelc_fast)
            

            # pos = [0.012271463871002197, -0.37529003620147705, 1.915174961090088, 2.271044969558716, np.deg2rad(90), np.deg2rad(-173)]
            
            rot_pose_xyz = [0.4,-0.1,0.3]
            rot_pose_rpy = [-88,5,-88]
            robot.move_to_target_in_cartesian(rot_pose_xyz,rot_pose_rpy)
            current_pos = robot.get_current_waypoint()
            pos = current_pos['joint']
            pos[5] = np.deg2rad(-173)
            

            poses = [[pos[0],pos[1],pos[2],pos[3],pos[4],pos[5]+n*np.deg2rad(90)] for n in range(4)]
            for i in poses:
            
                robot.move_joint(i)
                time.sleep(2)
            
            robot.move_to_target_in_cartesian(pick_pose_xyz,pick_pose_rpy)
            robot.move_joint([0.012271463871002197, -0.37529003620147705, 1.915174961090088, 2.271044969558716, np.deg2rad(-90), np.deg2rad(-173)])
            # current_pos = robot.get_current_waypoint()
            # pos = current_pos['joint']
            # pos[4] = np.deg2rad(-90)
            robot.move_to_target_in_cartesian(pick_pose_xyz,pick_pose_rpy)

            robot.set_joint_maxvelc(joint_maxvelc_slow)
            move_along_z(robot,-0.1)
            gripper.open()
            move_along_z(robot,0.1)

            robot.move_to_target_in_cartesian(home_pose_xyz,pick_pose_rpy)

            time.sleep(2)
            robot.disconnect()

    except KeyboardInterrupt:
        robot.move_stop()

    except RobotError as e:
        print("robot Event:{0}".format(e))
        robot.move_stop()
        robot.disconnect()


    finally:
        # 断开服务器链接
        if robot.connected:
            # 断开机械臂链接
            robot.disconnect()
        # 释放库资源
        Auboi5Robot.uninitialize()
        print("run end-------------------------")
    # robot.move_joint(joint_radian)

def test_sim():
    

    Auboi5Robot.initialize()
    robot = Auboi5Robot()
    handle = robot.create_context()
    print("robot.rshd={0}".format(handle))

    # HOST_IP   = "192.168.56.10"
    try: 
        # ip = '192.168.109.130'
        ip = '192.168.56.10'
        port = 8899
        result = robot.connect(ip, port)

        if result != RobotErrorType.RobotError_SUCC:
            print("connect server{0}:{1} failed.".format(ip, port))
            # raise Exception()
        else:
            robot.enable_robot_event()
            robot.init_profile()
            # joint_maxvelc = (1,1,1,1,1,1)
            joint_maxvelc_fast = (0.9,0.9,0.9,0.9,0.9,0.9)
            joint_maxvelc_slow = (0.5,0.5,0.5,0.5,0.5,0.5)

            # joint_maxvelc = (2.596177, 2.596177, 2.596177, 3.110177, 3.110177, 3.110177)
            joint_maxacc = (17.308779/1, 17.308779/1, 17.308779/1, 17.308779/1, 17.308779/1, 17.308779/1)
            robot.set_joint_maxacc(joint_maxacc)
            robot.set_joint_maxvelc(joint_maxvelc_fast)

            # print(robot.set_tool_dynamics_param(tool_dynamics={"position": (0.0, 0.0, 0.15),"payload": 0.0,"inertia": (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)}))
            
            # print(robot.get_tool_dynamics_param())
            # robot.set_none_tool_dynamics_param()
            # print(robot.get_tool_dynamics_param())

            # robot.set_arrival_ahead_blend(0.05)
            # robot.set_arrival_ahead_distance(0.1)

            # io_config = robot.get_board_io_config(RobotIOType.User_DO)
            # print("io_status:{}".format(io_config))

            
            # servo_move_00(robot)
            # pick_pose = [0.02802106738090515, -0.7555553913116455, 1.3110105991363525, 0.47127923369407654, np.deg2rad(90), np.deg2rad(-90)]
            # robot.move_joint(pick_pose)

            #### Work flow should be measuring real grip Z coordinate, plus 0.1 to it to get pick_pose_xyz's Z
            #### Set tool center, and set focus distance
            pick_pose_xyz = [-0.1,-0.7,0.1684]
            # pick_pose_rpy = [-179.9,-1.38,178.4]
            pick_pose_rpy = [-180,0.01,180]

            home_pose_xyz= [-0.1,-0.5,0.1]
            
            

            robot.move_to_target_in_cartesian(home_pose_xyz,pick_pose_rpy)
            

            robot.move_to_target_in_cartesian(pick_pose_xyz,pick_pose_rpy)
            robot.set_joint_maxvelc(joint_maxvelc_slow)
            move_along_z(robot,-0.1)
            # gripper.close()
            move_along_z(robot,0.1)
            robot.set_joint_maxvelc(joint_maxvelc_fast)
            

            # pos = [0.012271463871002197, -0.37529003620147705, 1.915174961090088, 2.271044969558716, np.deg2rad(90), np.deg2rad(-173)]
            

            ##check here, xyz does not match with the pick_xyz
            rot_pose_xyz = [-0.1,-0.7,0.3]
            # rot_pose_rpy = [180,90,180]
            rot_pose_rpy = [90,0,0]

            robot.move_to_target_in_cartesian(rot_pose_xyz,rot_pose_rpy)
            current_pos = robot.get_current_waypoint()
            pos = current_pos['joint']
            pos[5] = np.deg2rad(-173)
            

            poses = [[pos[0],pos[1],pos[2],pos[3],pos[4],pos[5]+n*np.deg2rad(90)] for n in range(4)]
            for i in poses:
            
                robot.move_joint(i)
                time.sleep(2)
            
            robot.move_to_target_in_cartesian(pick_pose_xyz,pick_pose_rpy)
            # robot.move_joint([0.012271463871002197, -0.37529003620147705, 1.915174961090088, 2.271044969558716, np.deg2rad(-90), np.deg2rad(-173)])
            current_pos = robot.get_current_waypoint()
            pos = current_pos['joint']
            print(current_pos['ori'])
            pos[4] = np.deg2rad(-90)
            robot.move_joint(pos)
            # robot.move_joint(pos)
            # current_pos = robot.get_current_waypoint()
            # print(current_pos['ori'])
            # robot.move_to_target_in_cartesian(pick_pose_xyz,robot.quaternion_to_rpy(current_pos['ori']))
            pos[4] = np.deg2rad(-0)
            robot.move_joint(pos)

            robot.move_to_target_in_cartesian(pick_pose_xyz,pick_pose_rpy)

            robot.set_joint_maxvelc(joint_maxvelc_slow)
            move_along_z(robot,-0.1)
            # gripper.open()
            move_along_z(robot,0.1)

            robot.move_to_target_in_cartesian(home_pose_xyz,pick_pose_rpy)

            time.sleep(2)
            

    except KeyboardInterrupt:
        robot.move_stop()

    except RobotError as e:
        print("robot Event:{0}".format(e))
        # robot.move_stop()
        # robot.disconnect()


    finally:
        # 断开服务器链接
        if robot.connected:
            # 断开机械臂链接
            robot.disconnect()
        # 释放库资源
        Auboi5Robot.uninitialize()
        print("run end-------------------------")
    # robot.move_joint(joint_radian)

import cv2
def test_1():
    gripper = Gripper()

    laptop_ip = "192.168.56.20"
    camera_ip = "192.168.56.50"
    capture = VideoCapture(network_ip=laptop_ip, camera_ip=camera_ip)
    
    Auboi5Robot.initialize()
    robot = Auboi5Robot()
    handle = robot.create_context()
    print("robot.rshd={0}".format(handle))

    # HOST_IP   = "192.168.56.10"
    try: 
        ip = '192.168.56.10'
        port = 8899
        result = robot.connect(ip, port)

        if result != RobotErrorType.RobotError_SUCC:
            print("connect server{0}:{1} failed.".format(ip, port))
            # raise Exception()
        else:
            robot.enable_robot_event()
            robot.init_profile()
            # joint_maxvelc = (1,1,1,1,1,1)
            joint_maxvelc_fast = (0.9,0.9,0.9,0.9,0.9,0.9)
            joint_maxvelc_slow = (0.5,0.5,0.5,0.5,0.5,0.5)

            # joint_maxvelc = (2.596177, 2.596177, 2.596177, 3.110177, 3.110177, 3.110177)
            joint_maxacc = (17.308779/2.5, 17.308779/2.5, 17.308779/2.5, 17.308779/2.5, 17.308779/2.5, 17.308779/2.5)
            robot.set_joint_maxacc(joint_maxacc)
            robot.set_joint_maxvelc(joint_maxvelc_fast)
            
            servo_move_00(robot)
            # pick_pose = [0.02802106738090515, -0.7555553913116455, 1.3110105991363525, 0.47127923369407654, np.deg2rad(90), np.deg2rad(-90)]
            # robot.move_joint(pick_pose)
            pick_pose_xyz = [-0.12,-0.7,0.14]
            pick_pose_rpy = [-179.9,0,0]
            home_pose_xyz= [-0.12,-0.5,0.1]
            joint_home = [np.deg2rad(-90),np.deg2rad(-30),np.deg2rad(90),np.deg2rad(5),np.deg2rad(90),np.deg2rad(90)]
            robot.move_joint(joint_home)
            robot.move_to_target_in_cartesian(home_pose_xyz,pick_pose_rpy)
            gripper.open()
            gripper.close()
            gripper.open()
            servo_move_01(robot)
            #capture image
            # Take image
            ret, frame = capture.read()
            # Save image
            cv2.imwrite("static/image1.jpg", frame)
            servo_move_00(robot)

            robot.move_to_target_in_cartesian(pick_pose_xyz,pick_pose_rpy)
            robot.set_joint_maxvelc(joint_maxvelc_slow)
            move_along_z(robot,-0.1)
            gripper.close()
            move_along_z(robot,0.1)
            robot.set_joint_maxvelc(joint_maxvelc_fast)
            

            # pos = [0.012271463871002197, -0.37529003620147705, 1.915174961090088, 2.271044969558716, np.deg2rad(90), np.deg2rad(-173)]
            
            rot_pose_xyz = [-0.12,-0.6,0.3]
            rot_pose_rpy = [88,0,0]
            robot.move_to_target_in_cartesian(rot_pose_xyz,rot_pose_rpy)
            current_pos = robot.get_current_waypoint()
            pos = current_pos['joint']
            pos[5] = np.deg2rad(-173)
            ret, frame = capture.read()
            # Save image
            cv2.imwrite("static/image2.jpg", frame)
            

            poses = [[pos[0],pos[1],pos[2],pos[3],pos[4],pos[5]+n*np.deg2rad(90)] for n in range(4)]
            for id, i in enumerate(poses):
            
                robot.move_joint(i)
                ret, frame = capture.read()
                # Save image
                cv2.imwrite(f"static/image{id+3}.jpg", frame)
            
            robot.move_to_target_in_cartesian(pick_pose_xyz,pick_pose_rpy)
            
            robot.set_joint_maxvelc(joint_maxvelc_slow)
            move_along_z(robot,-0.1)
            gripper.open()
            move_along_z(robot,0.1)

            robot.move_to_target_in_cartesian(home_pose_xyz,pick_pose_rpy)
            capture.release()

            robot.disconnect()

    except KeyboardInterrupt:
        robot.move_stop()

    except RobotError as e:
        print("robot Event:{0}".format(e))
        robot.move_stop()
        robot.disconnect()


    finally:
        # 断开服务器链接
        if robot.connected:
            # 断开机械臂链接
            robot.disconnect()
        # 释放库资源
        Auboi5Robot.uninitialize()
        print("run end-------------------------")
    # robot.move_joint(joint_radian)

def test_2():
        # gripper = Gripper()
    

    Auboi5Robot.initialize()
    robot = Auboi5Robot()
    handle = robot.create_context()
    print("robot.rshd={0}".format(handle))

    # HOST_IP   = "192.168.56.10"
    
    ip = '192.168.56.10'
    port = 8899
    result = robot.connect(ip, port)

    if result != RobotErrorType.RobotError_SUCC:
        print("connect server{0}:{1} failed.".format(ip, port))
        # raise Exception()
    servo_move_00(robot)
    servo_move_01(robot)

    

if __name__ == '__main__':
    # test_get_joints_real()
    # test_move_real()
    # test_io_servo()
    # test_gripper()
    # test_move_capture()
    test_1()
    print("test completed")