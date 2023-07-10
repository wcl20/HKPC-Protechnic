import cv2
import os.path as osp
from vimba import *

class VideoCapture:

    def __init__(self, settings_file):
        self.settings_file = settings_file

    def read(self):
        with Vimba.get_instance() as vimba:
            with vimba.get_all_cameras()[0] as camera:
                camera.load_settings(self.settings_file, PersistType.All)
                frame = camera.get_frame()
                frame.convert_pixel_format(PixelFormat.Mono8)
                frame = frame.as_opencv_image()
                return frame

if __name__ == '__main__':

    settings_file = osp.join( "settings", "vimba.xml")

    capture = VideoCapture(settings_file)
    frame = capture.read()

    cv2.imshow("image", imutils.resize(frame, width=1000))
    cv2.waitKey(0)
