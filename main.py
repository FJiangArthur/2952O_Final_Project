import multiprocessing
from mirobot import *
# from oak_d_lite import *
from yolov5_realsense import init_realsense
import time
import pyrealsense2 as rs
import numpy as np
import cv2
import random
import torch
import time



if __name__ == '__main__':

    queue = multiprocessing.Queue()

    mirobot_p = multiprocessing.Process(target=mirobot_control, args=(queue,))
    mirobot_p.start()

    realsense = multiprocessing.Process(target=init_realsense(), args=(queue,))
    realsense.start()

    # queue.put(MyFancyClass('Fancy Dan'))

    # Wait for the worker to finish
    queue.close()
    queue.join_thread()
    mirobot_p.join()
    realsense.join()

