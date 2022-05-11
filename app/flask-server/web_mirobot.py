import math

from wlkata_mirobot import WlkataMirobot, WlkataMirobotTool
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


def mirobot_control(process_q=None, stop_queue=None):
    arm = WlkataMirobot(portname='/dev/cu.usbserial-10')
    # arm = WlkataMirobot(portname='COM3')
    # arm = WlkataMirobot(portname='/dev/cu.usbserial-14120')

    # Calibration numbers y->left, right, x->front, back
    end_effector_abs = {'x': 202, 'y': 0, 'z': 181}

    mirobot_location = None
    target_location = None

    arm.home()
    # arm.set_tool_type(WlkataMirobotTool.SUCTION_CUP)
    # I modified the source code to setup suction cup natively at boot up
    # /wlkata_mirobot/wlkata_mirobot.py:125
    print("Start Homing!")

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

    print(arm.get_status())
    once = False
    twice = False
    item_location = {}
    while True:
        mirobot_info_que = process_q.get()
        print(mirobot_info_que)
        if len(mirobot_info_que) != 0:
            if 'clock' in mirobot_info_que and 0 not in mirobot_info_que['clock'].items():
                mirobot_location = mirobot_info_que['clock']
            if 'car' in mirobot_info_que and 0 not in mirobot_info_que['car'].items():
                target_location = mirobot_info_que['car']

        if target_location != None and mirobot_location != None:
            stop_queue.put("Stop")
            if not once:
                # if abs(mirobot_location['x'] - target_location['x']) >= 50:
                #     miro_move_left_right(step= (1.6) *(mirobot_location['x'] - target_location['x']) * np.sign(mirobot_location['x'] - target_location['x']))
                #     time.sleep(2)
                #
                # if abs(mirobot_location['z'] - target_location['z']) >= 50:
                #     move_front_back(step=50 * np.sign(mirobot_location['z'] - target_location['z']))
                #     time.sleep(2)
                #
                # if abs(mirobot_location['y'] - target_location['y']) >= 50:
                #     move_up_down(step= 150 * (1) * np.sign(mirobot_location['y'] - target_location['y']))
                #     time.sleep(2)

                # Hard Coded
                arm.set_tool_pose(y=int((-0.4) * (mirobot_location['x'] - target_location['x']) * np.sign(mirobot_location['x'] - target_location['x'])),
                                  x=int((0.07) * (mirobot_location['z'] - target_location['z']) * np.sign(
                                      mirobot_location['z'] - target_location['z'])),
                                  z=-100,
                                  roll=0.0, pitch=0.0, yaw=0.0, mode='p2p', speed=2000, is_relative=True)
                once = True
                stop_queue.get()  # Restart

            elif once and not twice:
                if abs(mirobot_location['x'] - target_location['x']) >= 10:
                    arm.set_tool_pose(y=int((-0.4) * (mirobot_location['x'] - target_location['x']) * np.sign(mirobot_location['x'] - target_location['x'])),
                                      is_relative=True)

                if abs(mirobot_location['z'] - target_location['z']) >= 10:
                    arm.set_tool_pose(x=int(0.15 * (mirobot_location['z'] - target_location['z']) *
                                            np.sign(mirobot_location['z'] - target_location['z'])), is_relative=True)

                # move_up_down(step= 60 * (1) * np.sign(mirobot_location['y'] - target_location['y']))#abs(target_location['y'] - mirobot_location['y']))
                arm.set_tool_pose(z=-40, is_relative=True)

                arm.pump_suction()
                time.sleep(3)
                arm.set_tool_pose(z=140,
                                  roll=0.0, pitch=0.0, yaw=0.0, mode='p2p', speed=2000, is_relative=True)

                arm.set_tool_pose(x=0,
                                  y=-20,
                                  z=180,
                                  roll=0.0, pitch=0.0, yaw=0.0, mode='p2p', speed=2000, is_relative=False)
                time.sleep(5)
                arm.pump_blowing()
                arm.pump_off()
                arm.set_tool_pose(x=202, y=0, z=181)
                stop_queue.get()
                twice = False
                once = False


if __name__ == '__main__':
    mirobot_control()
