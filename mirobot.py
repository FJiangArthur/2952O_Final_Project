import math

from wlkata_mirobot import WlkataMirobot,WlkataMirobotTool
import time

animals = {'dog','sheep', 'horse'}
cars = {'truck', 'car'}

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




def mirobot_control(process_q=None,stop_queue=None):
    arm = WlkataMirobot()
    # arm = WlkataMirobot(portname='COM3')
    # arm = WlkataMirobot(portname='/dev/cu.usbserial-14120')

    end_effector_abs = {'x': 202, 'y': 0, 'z': 181}  # Calibration numbers y->left, right, x->front, back

    mirobot_location = None
    target_location = {}

    arm.home()
    # arm.set_tool_type(WlkataMirobotTool.SUCTION_CUP)
    # I modified the source code to setup suction cup natively at boot up
    # /wlkata_mirobot/wlkata_mirobot.py:125
    print("Start Homing!")

    print(arm.get_status())
    once = False
    twice = False
    time.sleep(2)
    # arm.set_joint_angle({6:-90.0})

    while True:
        mirobot_info_que = process_q.get()
        print(mirobot_info_que)
        for key in mirobot_info_que.keys():
            if key == 'clock' and 0 not in mirobot_info_que[key].items():
                mirobot_location = mirobot_info_que['clock']
            else:
                 target_location[key] = mirobot_info_que[key]

        if target_location != None and mirobot_location != None:
            stop_queue.put("Stop")
            for current_target_key in target_location.keys():
                if not once:
                    ## Hard Coded
                    arm.set_tool_pose(y= int((-0.27) *(mirobot_location['x'] - target_location[current_target_key]['x']) * np.sign(mirobot_location['x'] - target_location[current_target_key]['x'])),
                                      x= int((0.09) *(mirobot_location['z'] - target_location[current_target_key]['z']) * np.sign(mirobot_location['z'] - target_location[current_target_key]['z'])),
                                      z= -120,
                                      roll=0.0, pitch=0.0, yaw=0.0, mode='p2p', speed=2000, is_relative=True)
                    once = True


                if once and not twice:
                    if abs(mirobot_location['x'] - target_location[current_target_key]['x']) >= 10:
                        arm.set_tool_pose(y= int((-0.05) *(mirobot_location['x'] - target_location[current_target_key]['x']) * np.sign(mirobot_location['x'] - target_location[current_target_key]['x'])),
                                             is_relative=True)

                    if abs(mirobot_location['z'] - target_location[current_target_key]['z']) >= 10:
                        arm.set_tool_pose(x=int(0.02 * (mirobot_location['z'] - target_location[current_target_key]['z']) *
                                             np.sign(mirobot_location['z'] - target_location[current_target_key]['z'])), is_relative=True)


                    # move_up_down(step= 60 * (1) * np.sign(mirobot_location['y'] - target_location[current_target_key]['y']))#abs(target_location[current_target_key]['y'] - mirobot_location['y']))
                    arm.set_tool_pose(z= -40, is_relative=True)

                    arm.gripper_close()
                    time.sleep(3)
                    arm.set_tool_pose(z=140,
                                      roll=0.0, pitch=0.0, yaw=0.0, mode='p2p', speed=2000, is_relative=True)

                    if current_target_key in animals:
                        arm.set_tool_pose(x=0, y=202, z=181)
                        arm.gripper_open()
                        time.sleep(3)
                    else:
                        arm.set_tool_pose(x=0, y=-202, z=181)
                        arm.gripper_open()
                        time.sleep(3)

                    arm.set_tool_pose(x=202, y= 0, z=181)
                    stop_queue.get()
                    twice = False
                    once = False

if __name__ == '__main__':
    mirobot_control()