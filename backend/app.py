import cv2
import numpy as np
from camera import VideoCapture
from flask import Flask
from flask_cors import CORS
from endpoints.aubogripper import Gripper
from endpoints.auborobot import AuboRobot
from endpoints.hikrobot import VideoCapture
from endpoints.lights import Light

app = Flask(__name__)
CORS(app)

def capture(lights, camera):
    '''
    Captures 4 images by switching on each light one by one.
    Returns the average of the 4 images.
    '''
    # Switch on light 1
    lights.on(0)
    # Store list of images
    frames = []
    # Take first image
    ret, frame = camera.read()
    frames.append(frame)
    # Take 2, 3, 4 image
    terminals = range(4)
    for current, next in zip(terminals, terminals[1:]):
        lights.off(current)
        lights.on(next)

        ret, frame = camera.read()
        frames.append(frame)
    # Switch off light 4
    lights.off(3)
    # Create average image
    avg_img = frames[0]
    for i in range(1, len(frames)):
        alpha = 1.0 / (i + 1)
        avg_img = cv2.addWeighted(frames[i], alpha, avg_img, 1.0 - alpha, 0.0)

    return avg_img

@app.route('/api/inspection')
def inspect():

    # Initialize gripper
    gripper = Gripper()

    # Initialize Light control
    lights_comport = "COM3"
    lights_baudrate = 9600
    lights = Light(lights_comport, lights_baudrate)

    # Initialize camera
    laptop_ip = "192.168.56.20"
    camera_ip = "192.168.56.50"
    camera = VideoCapture(network_ip=laptop_ip, camera_ip=camera_ip)

    # Initialize robot arm + vertical axis
    robot_ip = '192.168.56.10'
    robot_port = 8899
    robot = AuboRobot(robot_ip, robot_port)

    # Move up vertical axis
    robot.move_vertical_axis("up")

    # Move robot arm to home position
    joint_degress = [-90, -30, 90, 5, 90, 90]
    joint_radians= list(map(np.deg2rad, joint_degress))
    robot.move_joint(joint_radians)
    robot.move_cartesian([-0.12, -0.5, 0.1], [-179.9, 0, 0])

    # Test gripper
    gripper.open()
    gripper.close()
    gripper.open()

    # Move down vertial axis
    robot.move_vertical_axis("down")

    # Take image + save image
    frame = capture(lights, camera)
    cv2.imwrite("static/image1.jpg", frame)

    # Move up vertical axis
    robot.move_vertical_axis("up")

    # Pick up the shit
    robot.move_cartesian([-0.12, -0.7, 0.14], [-179.9, 0, 0])
    robot.slow()
    robot.move_along_z(-0.1)
    gripper.close()
    robot.move_along_z(0.1)
    robot.fast()

    # Move to camera
    robot.move_cartesian([-0.12, -0.6, 0.3], [88, 0, 0])

    # Take image + save image
    frame = capture(lights, camera)
    cv2.imwrite("static/image2.jpg", frame)

    # Rotate wrist 6 to take remaining 4 images
    waypoint = robot.get_current_waypoint()
    joint_radians = waypoint['joint']
    joint_radians[5] = np.deg2rad(-173)

    for i in range(4):
        joint_radians[5] += i * np.deg2rad(90)
        robot.move_joint(joint_radians)

        # Take image + save image
        frame = capture(lights, camera)
        cv2.imwrite(f"static/image{i + 3}.jpg", frame)


    # Put down shit
    robot.move_cartesian([-0.12, -0.7, 0.14], [-179.9, 0, 0])
    robot.slow()
    robot.move_along_z(-0.1)
    gripper.open()
    robot.move_along_z(0.1)
    robot.fast()

    # Back to home position
    robot.move_cartesian([-0.12, -0.5, 0.1], [-179.9, 0, 0])

    # Disconnect devices
    camera.release()
    robot.disconnect()

    # Return results
    return {
        "results": [
            {
                "image": f"http://localhost:5000/static/image1.jpg",
                "heatmap": f"http://localhost:5000/static/image1.jpg",
                "error": True
            },
            {
                "image": f"http://localhost:5000/static/image2.jpg",
                "heatmap": f"http://localhost:5000/static/image2.jpg",
                "error": False
            },
            {
                "image": f"http://localhost:5000/static/image3.jpg",
                "heatmap": f"http://localhost:5000/static/image3.jpg",
                "error": False
            },
            {
                "image": f"http://localhost:5000/static/image4.jpg",
                "heatmap": f"http://localhost:5000/static/image4.jpg",
                "error": False
            },
            {
                "image": f"http://localhost:5000/static/image5.jpg",
                "heatmap": f"http://localhost:5000/static/image5.jpg",
                "error": False
            },
        ]
    }
