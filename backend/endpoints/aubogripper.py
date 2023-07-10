import binascii
import serial

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
        self.ser.write(b"\x09\x10\x03\xE8\x00\x03\x06\x09\x00\x00\xFF\xFF\xFF\x42\x29")
        data = binascii.hexlify(self.ser.readline())
        return data

    def open(self):
        self.ser.write(b"\x09\x10\x03\xE8\x00\x03\x06\x09\x00\x00\x00\xFF\xFF\x72\x19")
        data = binascii.hexlify(self.ser.readline())
        return data
