import serial

class Light:

    def __init__(self, comport, baudrate=9600):
        self.ser = serial.Serial(comport, baudrate, timeout=1)

    def on(self, terminal):
        assert terminal in [0, 1, 2, 3]
        # Turn on light 1
        if terminal == 0:
            self.ser.write('$310FF16'.encode('utf-8'))
        # Turn on light 2
        elif terminal == 1:
            self.ser.write('$320FF15'.encode('utf-8'))
        # Turn on light 3
        elif terminal == 2:
            self.ser.write('$330FF14'.encode('utf-8'))
        # Turn on light 4
        elif terminal == 3:
            self.ser.write('$340FF13'.encode('utf-8'))

    def off(self, terminal):
        assert terminal in [0, 1, 2, 3]
        # Turn off light 1
        if terminal == 0:
            self.ser.write('$3100016'.encode('utf-8'))
        # Turn off light 2
        elif terminal == 1:
            self.ser.write('$3200015'.encode('utf-8'))
        # Turn off light 3
        elif terminal == 2:
            self.ser.write('$3300014'.encode('utf-8'))
        # Turn off light 4
        elif terminal == 3:
            self.ser.write('$3400013'.encode('utf-8'))
