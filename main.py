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
    # https://pythonspeed.com/articles/python-multiprocessing/?msclkid=413c793fd06911ecbe91ca2528ab95d1
    multiprocessing.set_start_method("spawn")
    queue = multiprocessing.Queue()
    stop_queue = multiprocessing.Queue()

    mirobot_p = multiprocessing.Process(target=mirobot_control, args=(queue,stop_queue,))
    mirobot_p.start()

    time.sleep(15)
    realsense = multiprocessing.Process(target=init_realsense, args=(queue,stop_queue))
    realsense.start()

    # Wait for the worker to finish
    queue.close()
    queue.join_thread()
    mirobot_p.join()
    realsense.join()

