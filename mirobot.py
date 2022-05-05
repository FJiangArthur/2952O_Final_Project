from wlkata_mirobot import WlkataMirobot
import time




def mirobot_control(process_q=None):
    def move_left(step=100, relative=False):
        arm.set_tool_pose(x=mirobot_location['x'],
                          y=mirobot_location['y'] + step,
                          z=mirobot_location['z'],
                          roll=0.0, pitch=0.0, yaw=0.0, mode='p2p', speed=2000, is_relative=relative)

    def move_right(step=100, relative=False):
        arm.set_tool_pose(x=mirobot_location['x'],
                          y=mirobot_location['y'] - step,
                          z=mirobot_location['z'],
                          roll=0.0, pitch=0.0, yaw=0.0, mode='p2p', speed=2000, is_relative=relative)

    def move_front(step=100, relative=False):
        arm.set_tool_pose(x=mirobot_location['x'] + step,
                          y=mirobot_location['y'],
                          z=mirobot_location['z'],
                          roll=0.0, pitch=0.0, yaw=0.0, mode='p2p', speed=2000, is_relative=relative)

    def move_back(step=100, relative=False):
        arm.set_tool_pose(x=mirobot_location['x'] - step,
                          y=mirobot_location['y'],
                          z=mirobot_location['z'],
                          roll=0.0, pitch=0.0, yaw=0.0, mode='p2p', speed=2000, is_relative=relative)

    def move_up(step=100, relative=False):
        arm.set_tool_pose(x=mirobot_location['x'],
                          y=mirobot_location['y'],
                          z=mirobot_location['z'] + step,
                          roll=0.0, pitch=0.0, yaw=0.0, mode='p2p', speed=2000, is_relative=relative)

    def move_down(step=100, relative=False):
        arm.set_tool_pose(x=mirobot_location['x'],
                          y=mirobot_location['y'],
                          z=mirobot_location['z'] - step,
                          roll=0.0, pitch=0.0, yaw=0.0, mode='p2p', speed=2000, is_relative=relative)
        
    arm = WlkataMirobot(portname='/dev/cu.usbserial-14310')
    mirobot_location = {'x': 202, 'y': 0, 'z': 181}  # Calibration numbers
    target_location = None
    print("Start Homing!")
    arm.home()

    arm.get_status()

    item_location = {}

    while True:
        mirobot_info_que = process_q.get()
        print(mirobot_info_que)
        if len(mirobot_info_que) != 0:
            if 'clock' in mirobot_info_que and 0 not in mirobot_info_que['clock'] :
                mirobot_location = mirobot_info_que['clock']
            if 'car' in mirobot_info_que and 0 not in mirobot_info_que['car']:
                target_location = mirobot_info_que['car']

        if target_location != None:

            if mirobot_location['x'] - target_location['x'] >= 10:
                print(mirobot_location)
                print(target_location)
                move_right()
            if target_location['x'] -mirobot_location['x'] >= 10:
                print(mirobot_location)
                print(target_location)
                move_left()
            if mirobot_location['y'] - target_location['y'] >= 10:
                print(mirobot_location)
                print(target_location)
                move_down()
            if target_location['y'] -mirobot_location['y'] >= 10:
                print(mirobot_location)
                print(target_location)
                move_up()
            if mirobot_location['z'] - target_location['z'] >= 10:
                print(mirobot_location)
                print(target_location)
                move_front()
            if target_location['z'] -mirobot_location['z'] >= 10:
                print(mirobot_location)
                print(target_location)
                move_back()








    # # Replicating 1E (Target A)
    # print("Setting arm to point A")
    # arm.set_tool_pose(x=142.1, y=-134.5, z=6.1)
    # print(f"After setting coordinate, the status of the arm is: {arm.status}")
    # # Replicating 1F (Target B)
    # target_angles = {1: 59.4, 2: 61.9, 3: 6, 4: 0.0, 5: -64.8, 6: 0}
    # arm.set_joint_angle(target_angles)
    # print(f"After setting joint angles, the status of the arm is: {arm.status}")

    # # Question 2D:
    # print("Move to target A")
    # arm.p2p_interpolation(x=142.1, y=-134.5, z=6.1)
    # print(f"Current position: {arm.pose}")
    # time.sleep(1)
    # print("Move to target B")
    # arm.p2p_interpolation(x=104.7, y=177.1, z=4.5)
    # print(f"Current position: {arm.pose}")
    # print(f"Current tool position in coordinate system {arm.pose}")
    #
    # # linear_interpolation (x=151.4, y=-119.0, z=-32.2) (x=78.8, y=181.4, z=-34.4)
    # print("Move to target A using linear_interpolation")
    # arm.linear_interpolation(x=142.1, y=-134.5, z=6.1)
    # print(f"Current position: {arm.pose}")
    # time.sleep(1)
    # print("Move to target B")
    # arm.linear_interpolation(x=104.7, y=177.1, z=4.5)
    # print(f"Current position: {arm.pose}")
    # print(f"Current tool position in coordinate system {arm.pose}")
    #
    # # door_interpolation
    # print("Move to target A using door_interpolation")
    # arm.door_interpolation(x=142.1, y=-134.5, z=6.1)
    # print(f"Current position: {arm.pose}")
    # time.sleep(5)
    # print("Move to target B")
    # arm.door_interpolation(x=104.7, y=177.1, z=4.5)
    # print(f"Current position: {arm.pose}")
    # print(f"Current tool position in coordinate system {arm.pose}")
    #
    # # Circular Inteporlation
    # print("Move to target A using door_interpolation")
    # arm.set_tool_pose(x=151.4, y=-119.0, z=-32.2)
    # print(f"Current position: {arm.pose}")
    # # time.sleep(5)
    # print("Move to target B")
    # arm.circular_interpolation(-75, 300, radius=200, is_cw=False)
    # print(f"Current position: {arm.pose}")
    # print(f"Current tool position in coordinate system {arm.pose}")
    #
    # # 3A
    # from wlkata_mirobot import WlkataMirobotTool
    # arm = WlkataMirobot(portname='/dev/cu.usbserial-14140')
    # print("Start Homing!")
    # arm.home()
    # arm.set_tool_type(WlkataMirobotTool.GRIPPER)
    # arm.set_tool_type(WlkataMirobotTool.FLEXIBLE_CLAW)
    # arm.set_tool_type(WlkataMirobotTool.SUCTION_CUP)
    #
    # # #3B
    # from wlkata_mirobot import WlkataMirobotTool
    # arm = WlkataMirobot(portname='/dev/cu.usbserial-14140')
    # print("Start Homing!")
    # arm.home()
    # arm.set_tool_type(WlkataMirobotTool.GRIPPER)
    #
    # arm.get_status()
    # arm.gripper_open()
    # arm.set_tool_pose(198.6, 0, 0.7)
    # arm.gripper_close()
    # arm.set_gripper_spacing(10)
    # time.sleep(5)
    # arm.set_tool_pose(198.2, 0, 32.5)
    #
    # # 3C
    # arm = WlkataMirobot(portname='/dev/cu.usbserial-14140')
    # print("Start Homing!")
    # arm.home()
    # arm.set_tool_type(WlkataMirobotTool.FLEXIBLE_CLAW)
    # arm.get_status()
    # arm.set_tool_pose(210.6, -10, 0.7, speed=500)
    # arm.pump_blowing()
    # time.sleep(5)
    # arm.set_tool_pose(210.6, -10, 35.7)
    # time.sleep(5)
    # arm.pump_suction()
    #
    # # # 3D
    # arm = WlkataMirobot(portname='/dev/cu.usbserial-14140')
    # print("Start Homing!")
    # arm.home()
    # arm.set_tool_type(WlkataMirobotTool.SUCTION_CUP)
    # arm.get_status()
    #
    # arm.set_tool_pose(198.6, 0, 35.7)
    # time.sleep(2)
    # arm.pump_suction()
    # arm.set_tool_pose(198.6, 0, 15.7, speed=500)
    #
    # time.sleep(5)
    # arm.set_tool_pose(210.6, -10, 35.7)
    # time.sleep(5)
    # arm.pump_blowing()


if __name__ == '__main__':
    mirobot_control()