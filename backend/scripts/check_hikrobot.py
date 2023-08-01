import cv2
import imutils
import sys
from mledge.endpoints.hikrobot_camera import VideoCapture

if __name__ == '__main__':

    HOST_IP   = "172.28.60.2"
    CAMERA_IP = "172.28.60.65"

    capture = VideoCapture(network_ip=HOST_IP, camera_ip=CAMERA_IP)

    ret, frame = capture.read()
    if not ret:
        print(f"[ERROR] Image capture failed!")
        sys.exit(1)

    cv2.imshow("image", imutils.resize(frame, width=800))
    cv2.waitKey(0)
