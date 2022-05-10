import math

from wlkata_mirobot import WlkataMirobot,WlkataMirobotTool
import time


# https://pysource.com/instance-segmentation-mask-rcnn-with-python-and-opencv
from wlkata_mirobot import WlkataMirobot
# from mirobot import Mirobot
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



def mirobot_control(process_q=None):
    arm = WlkataMirobot()
    # arm = WlkataMirobot(portname='COM3')
    end_effector_abs = {'x': 202, 'y': 0, 'z': 181}  # Calibration numbers y->left, right, x->front, back

    mirobot_location = None
    target_location = None
    print("Start Homing!")
    arm.home()

    def miro_move_left_right(step=100, relative=False):
        target = end_effector_abs['y'] + step
        # if abs(target) > 230:
        #     target = 230 * np.sign(target)
        arm.set_tool_pose(x=end_effector_abs['x'],
                          y=target,
                          z=end_effector_abs['z'],
                          roll=0.0, pitch=0.0, yaw=0.0, mode='p2p', speed=2000, is_relative=relative)

        end_effector_abs['y'] = target



    def move_front_back(step=100, relative=False):
        target = end_effector_abs['x'] + step
        # if abs(target) > 290:
        #     target = 290 * np.sign(target)

        arm.set_tool_pose(x=target,
                          y=end_effector_abs['y'],
                          z=end_effector_abs['z'],
                          roll=0.0, pitch=0.0, yaw=0.0, mode='p2p', speed=2000, is_relative=relative)

        end_effector_abs['x'] = target

    # def move_back(step=100, relative=False):
    #     arm.set_tool_pose(x=end_effector_abs['x'] - step,
    #                       y=end_effector_abs['y'],
    #                       z=end_effector_abs['z'],
    #                       roll=0.0, pitch=0.0, yaw=0.0, mode='p2p', speed=2000, is_relative=relative)
    #     end_effector_abs['x'] = end_effector_abs['x'] - step


    def move_up_down(step=100, relative=False):
        target = end_effector_abs['z'] + step
        # if target < -100: 
        #      target = -100 
        # if target > 350:
        #     target = 350 

        arm.set_tool_pose(x=end_effector_abs['x'],
                          y=end_effector_abs['y'],
                          z=target,
                          roll=0.0, pitch=0.0, yaw=0.0, mode='p2p', speed=2000, is_relative=relative)
        end_effector_abs['z'] = target

    # def move_down(step=100, relative=False):
    #     arm.set_tool_pose(x=end_effector_abs['x'],
    #                       y=end_effector_abs['y'],
    #                       z=end_effector_abs['z'] - step,
    #                       roll=0.0, pitch=0.0, yaw=0.0, mode='p2p', speed=2000, is_relative=relative)
    #     end_effector_abs['z'] = end_effector_abs['z'] + step


    # arm = WlkataMirobot(portname='/dev/cu.usbserial-14120')
    

    print(arm.get_status())
    once = False
    twice = False
    item_location = {}
    while True:
        mirobot_info_que = process_q.get()
        print(mirobot_info_que)
        if len(mirobot_info_que) != 0:
            if 'clock' in mirobot_info_que and 0 not in mirobot_info_que['clock'] :
                mirobot_location = mirobot_info_que['clock']
            if 'car' in mirobot_info_que and 0 not in mirobot_info_que['car']:
                target_location = mirobot_info_que['car']


        if target_location != None and mirobot_location != None:
            if not once: 
                if abs(mirobot_location['x'] - target_location['x']) >= 50:
                    print("Moving left-right")
                    print("Mirobot Clock location: ",mirobot_location)
                    print("Target Location:", target_location)
                    print("Mirobot end effector location:", end_effector_abs)
                    # miro_move_left_right(step=(target_location['x'] - mirobot_location['x'])*230/350)
                    miro_move_left_right(step=50 * (-1) * np.sign(mirobot_location['x'] - target_location['x']))
                    # time.sleep(2)


                if abs(mirobot_location['z'] - target_location['z']) >= 100:
                    print("Moving front-back")
                    print("Mirobot Clock location: ", mirobot_location)
                    print("Target Location:", target_location)
                    print("Mirobot end effector location:", end_effector_abs)
                    # move_front_back(step=(mirobot_location['z'] - target_location['z'])*290/500)
                    move_front_back(step=50 * np.sign(mirobot_location['z'] - target_location['z']))
                    # time.sleep(2)


                if abs(mirobot_location['y'] - target_location['y']) >= 50:
                    move_up_down(step= 180 * (1) * np.sign(mirobot_location['y'] - target_location['y']))
                    # time.sleep(2)
                
                once = True
            
            if once and not twice:
                if abs(mirobot_location['x'] - target_location['x']) >= 50:
                    print("Moving left-right")
                    print("Mirobot Clock location: ",mirobot_location)
                    print("Target Location:", target_location)
                    print("Mirobot end effector location:", end_effector_abs)
                    # miro_move_left_right(step=(target_location['x'] - mirobot_location['x'])*230/350)
                    miro_move_left_right(step=10 * (-1) * np.sign(mirobot_location['x'] - target_location['x']))
                    # time.sleep(2)


                if abs(mirobot_location['z'] - target_location['z']) >= 100:
                    print("Moving front-back")
                    print("Mirobot Clock location: ", mirobot_location)
                    print("Target Location:", target_location)
                    print("Mirobot end effector location:", end_effector_abs)
                    # move_front_back(step=(mirobot_location['z'] - target_location['z'])*290/500)
                    move_front_back(step=15 * np.sign(mirobot_location['z'] - target_location['z']))
                    # time.sleep(2)


                if abs(mirobot_location['y'] - target_location['y']) >= 50:
                    print("Moving up-down")
                    print("step:",(target_location['y'] - mirobot_location['y']))
                    print("Mirobot end effector location:", end_effector_abs)
                    # move_up_down(step= 60 * (1) * np.sign(mirobot_location['y'] - target_location['y']))#abs(target_location['y'] - mirobot_location['y']))
                    move_up_down(step= 10 * (1) * np.sign(mirobot_location['y'] - target_location['y']))
                    # time.sleep(2)

            
            arm.set_tool_type(WlkataMirobotTool.SUCTION_CUP)
            arm.pump_suction()
            time.sleep(5)
            arm.set_tool_pose(x=end_effector_abs['x'],
                          y=end_effector_abs['y'],
                          z=180,
                          roll=0.0, pitch=0.0, yaw=0.0, mode='p2p', speed=2000, is_relative=relative)
            end_effector_abs['z'] = 180

            arm.set_tool_pose(x=50,
                          y=60,
                          z=20,
                          roll=0.0, pitch=0.0, yaw=0.0, mode='p2p', speed=2000, is_relative=relative)

            end_effector_abs['z'] = 20
            end_effector_abs['y'] = 60
            end_effector_abs['x'] = 50

if __name__ == '__main__':
    mirobot_control()