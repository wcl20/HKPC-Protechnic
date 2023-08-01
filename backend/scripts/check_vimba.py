import os.path as osp
import cv2
import imutils
from mledge.endpoints.vimba_camera import VideoCapture

if __name__ == '__main__':

    settings_file = osp.join( "settings", "vimba.xml")

    capture = VideoCapture(settings_file)
    frame = capture.read()

    cv2.imshow("image", imutils.resize(frame, width=1000))
    cv2.waitKey(0)
