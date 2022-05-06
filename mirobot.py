import math

from wlkata_mirobot import WlkataMirobot
import time


# https://pysource.com/instance-segmentation-mask-rcnn-with-python-and-opencv
from wlkata_mirobot import WlkataMirobot
import time
import cv2
import numpy as np

# z: -54  - 350
# y:-230 - 230
# x: -290 - 290


def move_robot(arm, cx, cy):
    #    		spacing_mm = 100
    #    		arm.set_gripper_spacing(spacing_mm)
    #    		time.sleep(2)
    # gripper open
    #    		arm.gripper_open()
    #    		time.sleep(1)

    xNorm = cx / 416
    yNorm = cy / 416

    xScaled = (xNorm * 450) + -215
    yScaled = 364 - ((yNorm * 200) + 100)

    #    		xScaled =  round(xNorm * 300)
    #    		yScaled =  round(yNorm * 300) + 50

    # 		yScaled = cx / 6.4
    # 		xScaled = cy / 3.6

    print("XScaled: " + str(xScaled))
    print("YScaled: " + str(yScaled))

    arm.set_tool_pose(yScaled, -xScaled, 100)
    time.sleep(1)
    arm.set_tool_pose(yScaled, -xScaled, 0)
    arm.pump_suction()
    time.sleep(1)
    arm.set_tool_pose(yScaled, -xScaled, 100)
    time.sleep(1)
    arm.set_tool_pose(177, 45, 121)
    arm.pump_off()

def mirobot_new(process_q=None):
    arm = WlkataMirobot(portname='/dev/cu.usbserial-1430')
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
            if 'clock' in mirobot_info_que and 0 not in mirobot_info_que['clock']:
                mirobot_location = mirobot_info_que['clock']
            if 'cow' in mirobot_info_que and 0 not in mirobot_info_que['cow']:
                target_location = mirobot_info_que['cow']

        if target_location != None:
            move_robot(arm, target_location['x'], target_location['y'])



def mirobot_control(process_q=None):
    # def move(x_step, y_step, z_step, relative=False):
    #     print(x_step, y_step, z_step)
    #     arm.set_tool_pose(x=end_effector_abs['x'] - x_step,
    #                       y=end_effector_abs['y'] - y_step,
    #                       z=end_effector_abs['z'] - z_step,
    #                       roll=0.0, pitch=0.0, yaw=0.0, mode='p2p', speed=2000, is_relative=relative)
    #     print(end_effector_abs)
    #
    #     end_effector_abs['y'] += y_step
    #     end_effector_abs['x'] += x_step
    #     end_effector_abs['z'] += z_step

    def move_left(step=100, relative=False):
        arm.set_tool_pose(x=end_effector_abs['x'],
                          y=end_effector_abs['y'] + step,
                          z=end_effector_abs['z'],
                          roll=0.0, pitch=0.0, yaw=0.0, mode='p2p', speed=2000, is_relative=relative)

        end_effector_abs['y'] = end_effector_abs['y'] + step

    def move_right(step=100, relative=False):
        arm.set_tool_pose(x=end_effector_abs['x'],
                          y=end_effector_abs['y'] - step,
                          z=end_effector_abs['z'],
                          roll=0.0, pitch=0.0, yaw=0.0, mode='p2p', speed=2000, is_relative=relative)
        end_effector_abs['y'] = end_effector_abs['y'] - step

    def move_front(step=100, relative=False):
        arm.set_tool_pose(x=end_effector_abs['x'] + step,
                          y=end_effector_abs['y'],
                          z=end_effector_abs['z'],
                          roll=0.0, pitch=0.0, yaw=0.0, mode='p2p', speed=2000, is_relative=relative)
        end_effector_abs['x'] = end_effector_abs['x'] + step

    def move_back(step=100, relative=False):
        arm.set_tool_pose(x=end_effector_abs['x'] - step,
                          y=end_effector_abs['y'],
                          z=end_effector_abs['z'],
                          roll=0.0, pitch=0.0, yaw=0.0, mode='p2p', speed=2000, is_relative=relative)
        end_effector_abs['x'] = end_effector_abs['x'] - step
    def move_up(step=100, relative=False):
        arm.set_tool_pose(x=end_effector_abs['x'],
                          y=end_effector_abs['y'],
                          z=end_effector_abs['z'] + step,
                          roll=0.0, pitch=0.0, yaw=0.0, mode='p2p', speed=2000, is_relative=relative)
        end_effector_abs['z'] = end_effector_abs['z'] + step

    def move_down(step=100, relative=False):
        arm.set_tool_pose(x=end_effector_abs['x'],
                          y=end_effector_abs['y'],
                          z=end_effector_abs['z'] - step,
                          roll=0.0, pitch=0.0, yaw=0.0, mode='p2p', speed=2000, is_relative=relative)
        end_effector_abs['z'] = end_effector_abs['z'] + step


    arm = WlkataMirobot(portname='/dev/cu.usbserial-1430')
    end_effector_abs = {'x': 202, 'y': 0, 'z': 181}  # Calibration numbers

    mirobot_location = None
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

            # if abs(mirobot_location['x'] - target_location['x']) + abs(mirobot_location['y'] - target_location['y']) + abs(mirobot_location['z'] - target_location['z']):
            #     move( target_location['x'] - mirobot_location['x'], target_location['y'] - mirobot_location['y'], target_location['z'] -  mirobot_location['z'])
            #

            if mirobot_location['x'] - target_location['x'] >= 10:
                print("Moving right")
                print("Mirobot Clock location: ",mirobot_location)
                print("Target Location:", target_location)
                print("Mirobot end effector location:", end_effector_abs)
                move_right(step=mirobot_location['x'] - target_location['x'])


            if target_location['x'] -mirobot_location['x'] >= 10:
                print("Moving Right")
                print("Mirobot Clock location: ", mirobot_location)
                print("Target Location:", target_location)
                print("Mirobot end effector location:", end_effector_abs)
                move_left(step=abs(target_location['x'] - mirobot_location['x']))


            if mirobot_location['y'] - target_location['y'] >= 10:
                print("Moving down")
                print("Mirobot Clock location: ", mirobot_location)
                print("Target Location:", target_location)
                print("Mirobot end effector location:", end_effector_abs)
                move_down(step=mirobot_location['y'] - target_location['y'])


            if target_location['y'] -mirobot_location['y'] >= 10:
                print("Moving up")
                print("Mirobot Clock location: ", mirobot_location)
                print("Target Location:", target_location)
                print("Mirobot end effector location:", end_effector_abs)
                move_up(step=abs(target_location['y'] - mirobot_location['y']))


            if mirobot_location['z'] - target_location['z'] >= 10:
                print("Moving Front")
                print("Mirobot Clock location: ", mirobot_location)
                print("Target Location:", target_location)
                print("Mirobot end effector location:", end_effector_abs)
                move_front(step=mirobot_location['z'] - target_location['z'])

            if target_location['z'] -mirobot_location['z'] >= 10:
                print("Moving Back")
                print("Mirobot Clock location: ", mirobot_location)
                print("Target Location:", target_location)
                print("Mirobot end effector location:", end_effector_abs)
                move_back(step=abs(target_location['z'] - mirobot_location['z']))







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