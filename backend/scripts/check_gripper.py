from mledge.endpoints.gripper import Gripper

if __name__ == '__main__':

    ROBOT_IP  = "172.28.60.10"

    gripper = Gripper()
    gripper.connect(ROBOT_IP)
    gripper.activate()

    # Close
    gripper.move_and_wait_for_pos(255, 255, 255)
    print(f"Pos: {str(gripper.get_current_position())}")
    print(f"Open: {str(gripper.is_open())}")
    print(f"Close: {str(gripper.is_closed())}")

    # Open
    gripper.move_and_wait_for_pos(0, 255, 255)
    print(f"Pos: {str(gripper.get_current_position())}")
    print(f"Open: {str(gripper.is_open())}")
    print(f"Close: {str(gripper.is_closed())}")

    gripper.move_and_wait_for_pos(110, 255, 0)
