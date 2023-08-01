from mledge.endpoints.turntable import Turntable

if __name__ == '__main__':

    TURNTABLE_COMPORT = "/dev/ttyUSB0"

    turntable = Turntable(TURNTABLE_COMPORT)

    current_position = turntable.get_position()
    print(current_position)
