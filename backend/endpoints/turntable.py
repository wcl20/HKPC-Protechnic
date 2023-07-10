import serial
import struct

class Turntable:

    def __init__(self, comport, baudrate=115200, id=1):
        self.ser = serial.Serial(comport, baudrate, timeout=1)
        self.ser.bytesize = serial.EIGHTBITS
        self.ser.parity = serial.PARITY_NONE
        self.ser.stopbits = serial.STOPBITS_ONE

        self.id = id

    def close(self):
        self.ser.close()

    def create_command(self, instruction, params=b'', broadcast=False):
        # 0x01  Ping
        # 0x02  Read data
        # 0x03  Write data
        # 0x04  Regwrite data
        # 0x05  Action
        # 0x06  Reset
        # 0x82  Syncread data
        # 0x03  Synwrite data
        assert instruction in [1, 2, 3, 4, 5, 6, 130, 131]
        # Table device id default is 1. Use id 254 to broadcast command
        id = bytes([254]) if broadcast else bytes([self.id])
        # instruction Id
        instruction = bytes([instruction])
        # Length is number of parameters N + 2
        length = bytes([2 + len(params)])
        # Checksum
        checksum = bytes([(sum(id + length + instruction + params) & 0xFF) ^ 0xFF])
        # Command starts with two leading bytes '\xff\xff'
        command = b'\xff\xff' + id + length + instruction + params + checksum
        print("command: ", command.hex())
        return command

    def run_command(self, command):
        # Read first 5 bytes of response \xff\xff (id) (length) (error)
        response = self.ser.read(5)
        while not response:
            self.ser.write(command)
            response = self.ser.read(5)

        print("response: ", response.hex())
        length = response[3]
        error = response[4]
        assert error == 0, "Turntable error"
        # Read remaing paramters
        params = b'' if length == 2 else self.ser.read(length - 2)
        # Read checksum
        checksum = self.ser.read(1)
        compute_checksum = bytes([(sum(response[2:] + params) &0xFF) ^0xFF])
        assert checksum == compute_checksum
        return params

    def ping(self):
        command = self.create_command(1)
        return self.run_command(command)

    def read(self, addr, size):
        params = bytes([addr]) + bytes([size])
        command = self.create_command(2, params)
        return self.run_command(command)

    def write(self, addr, params, broadcast=False):
        addr = bytes([addr])
        command = self.create_command(3, addr + params, broadcast=broadcast)
        return self.run_command(command)

    def get_version(self):
        params = self.read(3, 2)
        return struct.unpack("<H", params)[0]

    def get_position(self):
        params = self.read(56, 2)
        return struct.unpack("<H", params)[0]

    def move(self, position, speed=0, time=0):

        current_position = self.get_position()
        if abs(current_position - position) < 10: return

        assert 0 <= position <= 4095
        params = struct.pack("<H", position)
        params += struct.pack("<H", time)
        params += struct.pack("<H", speed)
        return self.write(42, params)


if __name__ == '__main__':
    
    TURNTABLE_COMPORT = "/dev/ttyUSB0"

    turntable = Turntable(TURNTABLE_COMPORT)

    current_position = turntable.get_position()
    print(current_position)
