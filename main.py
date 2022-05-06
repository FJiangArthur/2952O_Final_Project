import multiprocessing
from mirobot import *
# from oak_d_lite import *
from yolov5_realsense import *
import time
import pyrealsense2 as rs
import numpy as np
import cv2
import random
import torch
import time

# model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
#

# -*- coding: utf-8 -*-
import pyrealsense2 as rs
import numpy as np
import cv2

pipeline = rs.pipeline()  # 定义流程pipeline，创建一个管道
config = rs.config()  # 定义配置config
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 15)  # 配置depth流
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 15)  # 配置color流

pipe_profile = pipeline.start(config)  # streaming流开始

# 创建对齐对象与color流对齐
align_to = rs.stream.color
align = rs.align(align_to)  # rs.align 执行深度帧与其他帧的对齐



def get_aligned_images():
    frames = pipeline.wait_for_frames()  # 等待获取图像帧，获取颜色和深度的框架集
    aligned_frames = align.process(frames)  # 获取对齐帧，将深度框与颜色框对齐

    aligned_depth_frame = aligned_frames.get_depth_frame()  # 获取对齐帧中的的depth帧
    aligned_color_frame = aligned_frames.get_color_frame()  # 获取对齐帧中的的color帧

    #### 获取相机参数 ####
    depth_intrin = aligned_depth_frame.profile.as_video_stream_profile().intrinsics  # 获取深度参数（像素坐标系转相机坐标系会用到）
    color_intrin = aligned_color_frame.profile.as_video_stream_profile().intrinsics  # 获取相机内参

    #### 将images转为numpy arrays ####
    img_color = np.asanyarray(aligned_color_frame.get_data())  # RGB图
    img_depth = np.asanyarray(aligned_depth_frame.get_data())  # 深度图（默认16位）

    return color_intrin, depth_intrin, img_color, img_depth, aligned_depth_frame




model = torch.hub.load('ultralytics/yolov5', 'yolov5l6')
model.conf = 0.5

def get_mid_pos(frame,box,depth_data,randnum, depth_intrin):
    distance_list = []
    x_list = []
    y_list= []
    z_list = []
    mid_pos = [(box[0] + box[2])//2, (box[1] + box[3])//2]
    min_val = min(abs(box[2] - box[0]), abs(box[3] - box[1]))
    for i in range(randnum):
        bias = random.randint(-min_val//4, min_val//4)
        dist = depth_data[int(mid_pos[1] + bias), int(mid_pos[0] + bias)]


        x = int(mid_pos[0] + bias)
        y = int(mid_pos[1] + bias)
        camera_coordinate = rs.rs2_deproject_pixel_to_point(depth_intrin, [x, y], dist)


        cv2.circle(frame, (int(mid_pos[0] + bias), int(mid_pos[1] + bias)), 4, (255,0,0), -1)

        if dist:
            distance_list.append(dist)
        if camera_coordinate:
            x_list.append(camera_coordinate[0])
            y_list.append(camera_coordinate[1])
            z_list.append(camera_coordinate[2])
    distance_list = np.array(distance_list)
    distance_list = np.sort(distance_list)[randnum//2-randnum//4:randnum//2+randnum//4]
    x_list = np.array(x_list)
    x_list = np.sort(x_list)[randnum // 2 - randnum // 4:randnum // 2 + randnum // 4]
    y_list = np.array(y_list)
    y_list = np.sort(y_list)[randnum // 2 - randnum // 4:randnum // 2 + randnum // 4]
    z_list = np.array(z_list)
    z_list = np.sort(z_list)[randnum // 2 - randnum // 4:randnum // 2 + randnum // 4]
    return np.mean(distance_list), np.mean(x_list), np.mean(y_list), np.mean(z_list)

def dectshow(org_img, boxs,depth_data, depth_intrin,start_time, current_time, process_que=None):
    img = org_img.copy()
    mirobot_info_que = {}

    for box in boxs:
        cv2.rectangle(img, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (0, 255, 0), 2)
        dist, x, y, z = get_mid_pos(org_img, box, depth_data, 24, depth_intrin)

        mirobot_info_que[box[-1]] = {'x': x,
                                   'y': y,
                                   'z': z}

        cv2.putText(img, box[-1] + str(dist / 1000)[:4] + 'm',
                    (int(box[0]), int(box[1])), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        cv2.putText(img, 'x:' + str(x / 1000)[:4] + 'm',
                    (int(box[0]), int(box[1])+20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(img,  'y:' + str(y / 1000)[:4] + 'm',
                    (int(box[0]), int(box[1])+40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(img, 'z:' + str(z / 1000)[:4] + 'm',
                    (int(box[0]), int(box[1]) -20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    if (current_time - start_time) > 1 and process_que != None:
        process_que.put(mirobot_info_que)

    cv2.imshow('dec_img', img)


if __name__ == '__main__':

    queue = multiprocessing.Queue()




    # Configure depth and color streams
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 60)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 60)
    # Start streaming
    pipeline.start(config)
    start_time = time.monotonic()

    mirobot_p = multiprocessing.Process(target=mirobot_control, args=(queue,))
    mirobot_p.start()

    time.sleep(10)
    try:
        while True:
            color_intrin, depth_intrin, img_color, img_depth, aligned_depth_frame = get_aligned_images()
            # Wait for a coherent pair of frames: depth and color
            frames = pipeline.wait_for_frames()
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()
            if not depth_frame or not color_frame:
                continue
            # Convert images to numpy arrays

            depth_image = np.asanyarray(depth_frame.get_data())

            color_image = np.asanyarray(color_frame.get_data())

            results = model(color_image)
            boxs = results.pandas().xyxy[0].values
            current_time = time.monotonic()
            # boxs = np.load('temp.npy',allow_pickle=True)
            dectshow(color_image, boxs, depth_image, depth_intrin, start_time, current_time,queue)
            start_time = current_time

            # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
            depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
            # Stack both images horizontally
            images = np.hstack((color_image, depth_colormap))
            # Show images
            cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
            cv2.imshow('RealSense', images)
            key = cv2.waitKey(1)
            # Press esc or 'q' to close the image window
            if key & 0xFF == ord('q') or key == 27:
                cv2.destroyAllWindows()
                break
    finally:
        # Stop streaming
        pipeline.stop()

    # oak_d_lite_p = multiprocessing.Process(target=oak_d_lite_control, args=(queue,))
    # oak_d_lite_p.start()

    # queue.put(MyFancyClass('Fancy Dan'))

    # Wait for the worker to finish
    queue.close()
    queue.join_thread()
    mirobot_p.join()

