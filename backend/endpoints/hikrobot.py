import numpy as np
import os
import sys
from ctypes import c_ubyte

# Hikrobot dependencies
os.environ["MVCAM_COMMON_RUNENV"] = "/opt/MVS/lib"
os.environ["MVCAM_SDK_PATH"] = "/opt/MVS"
sys.path.append("/opt/MVS/Samples/64/Python/MvImport")
from MvCameraControl_class import *

class VideoCapture:

    def __init__(self, network_ip, camera_ip):
    	print(f"[INFO] Connecting Hikvision ...")
    	self.camera = None
    	self.connect(network_ip, camera_ip)

    def connect(self, network_ip, camera_ip):
        # Camera already connected
        if self.camera is not None: return

        st_gige_device_info = MV_GIGE_DEVICE_INFO()
        # Camera IP address
        camera_ip_list = list(map(int, camera_ip.split('.')))
        st_gige_device_info.nCurrentIp = (
            (camera_ip_list[0] << 24) | (camera_ip_list[1] << 16) |
            (camera_ip_list[2] << 8)  | camera_ip_list[3])
        # PC IP address
        network_ip_list = list(map(int, network_ip.split('.')))
        st_gige_device_info.nNetExport = (
            (network_ip_list[0] << 24) | (network_ip_list[1] << 16) |
            (network_ip_list[2] << 8)  | network_ip_list[3])

        ################################################################
        # Camera setup
        ################################################################
        st_device_info = MV_CC_DEVICE_INFO()
        st_device_info.nTLayerType = MV_GIGE_DEVICE
        st_device_info.SpecialInfo.stGigEInfo = st_gige_device_info
        camera = MvCamera()

        # Create handle
        if camera.MV_CC_CreateHandle(st_device_info) != 0:
            raise Exception("camera.py: Create Handle Failed!")
        # Connect camera
        if camera.MV_CC_OpenDevice(MV_ACCESS_Exclusive, 0) != 0:
            raise Exception("camera.py: Open Camera Failed!")
        # Set optimal packet size (Only for gigE Camera)
        if st_device_info.nTLayerType == MV_GIGE_DEVICE:
            packet_size = camera.MV_CC_GetOptimalPacketSize()
            if packet_size > 0:
                camera.MV_CC_SetIntValue("GevSCPSPacketSize", packet_size)
        # Turn off trigger mode
        if camera.MV_CC_SetEnumValue("TriggerMode", MV_TRIGGER_MODE_OFF) != 0:
            raise Exception("camera.py: Turn off Trigger Mode Failed!")
        # Get Payload size
        st_param = MVCC_INTVALUE()
        memset(byref(st_param), 0, sizeof(MVCC_INTVALUE))
        if camera.MV_CC_GetIntValue("PayloadSize", st_param) != 0:
            raise Exception("camera.py: Get Payload Size Failed!")
        self.payload_size = st_param.nCurValue
        self.camera = camera

    def read(self):
        if self.camera.MV_CC_StartGrabbing() != 0:
            raise Exception("camera.py: Camera grabbing Failed!")

        st_device_list = MV_FRAME_OUT_INFO_EX()
        memset(byref(st_device_list), 0, sizeof(st_device_list))

        # Create data buffer
        data_buffer = (c_ubyte * self.payload_size)()

        # Get Frame
        ret = self.camera.MV_CC_GetOneFrameTimeout(
            byref(data_buffer), self.payload_size, st_device_list, 2000)
        if ret != 0:
            print(f"[Error] Get One Frame Timeout")
            return False, None

        image_width = st_device_list.nWidth
        image_height = st_device_list.nHeight
        rgb_size = 3 * image_width * image_height

        # Convert image to BGR
        st_convert_param = MV_CC_PIXEL_CONVERT_PARAM()
        memset(byref(st_convert_param), 0, sizeof(st_convert_param))
        st_convert_param.nWidth = st_device_list.nWidth
        st_convert_param.nHeight = st_device_list.nHeight
        st_convert_param.pSrcData = data_buffer
        st_convert_param.nSrcDataLen = st_device_list.nFrameLen
        st_convert_param.enSrcPixelType = st_device_list.enPixelType
        st_convert_param.enDstPixelType = PixelType_Gvsp_BGR8_Packed # PixelType_Gvsp_RGB8_Packed
        st_convert_param.pDstBuffer = (c_ubyte * rgb_size)()
        st_convert_param.nDstBufferSize = rgb_size
        if self.camera.MV_CC_ConvertPixelType(st_convert_param) != 0:
            print(f"[Error] Convert Pixel Type")
            del data_buffer
            return False, None

        # Create image buffer
        image_buffer = (c_ubyte * st_convert_param.nDstLen)()
        memmove(byref(image_buffer), st_convert_param.pDstBuffer, st_convert_param.nDstLen)

        # Convert to numpy array
        image = np.frombuffer(image_buffer, dtype=np.uint8, count=rgb_size)
        image = image.reshape((image_height, image_width, 3))
        del data_buffer
        del image_buffer

        if self.camera.MV_CC_StopGrabbing() != 0:
            raise Exception("camera.py: Camera stop grabbing Failed!")
        return True, image

    def release(self):
        # Check camera connected
        if self.camera is None: return
        if self.camera.MV_CC_CloseDevice() != 0:
            raise Exception("camera.py: Close Device Failed!")
        if self.camera.MV_CC_DestroyHandle() != 0:
            raise Exception("camera.py: Destroy Handle Failed")
