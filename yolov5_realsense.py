import random
import random
import time

import cv2
import numpy as np
# -*- coding: utf-8 -*-
import pyrealsense2 as rs
import torch


def init_realsense(process_que=None):
    # Configure depth and color streams
    start_time = time.monotonic()
    model = torch.hub.load('ultralytics/yolov5', 'yolov5l6')
    model.conf = 0.5
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 60)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 60)
    align_to = rs.stream.color
    align = rs.align(align_to)

    def get_aligned_images():
        frames = pipeline.wait_for_frames()
        aligned_frames = align.process(frames)

        aligned_depth_frame = aligned_frames.get_depth_frame()
        aligned_color_frame = aligned_frames.get_color_frame()

        depth_intrin = aligned_depth_frame.profile.as_video_stream_profile().intrinsics
        color_intrin = aligned_color_frame.profile.as_video_stream_profile().intrinsics

        img_color = np.asanyarray(aligned_color_frame.get_data())
        img_depth = np.asanyarray(aligned_depth_frame.get_data())

        return color_intrin, depth_intrin, img_color, img_depth, aligned_depth_frame

    def get_mid_pos(frame, box, depth_data, randnum, depth_intrin):
        distance_list = []
        x_list = []
        y_list = []
        z_list = []
        mid_pos = [(box[0] + box[2]) // 2, (box[1] + box[3]) // 2]
        min_val = min(abs(box[2] - box[0]), abs(box[3] - box[1]))
        for i in range(randnum):
            bias = random.randint(-min_val // 4, min_val // 4)
            dist = depth_data[int(mid_pos[1] + bias), int(mid_pos[0] + bias)]

            x = int(mid_pos[0] + bias)
            y = int(mid_pos[1] + bias)
            camera_coordinate = rs.rs2_deproject_pixel_to_point(depth_intrin, [x, y], dist)

            cv2.circle(frame, (int(mid_pos[0] + bias), int(mid_pos[1] + bias)), 4, (255, 0, 0), -1)

            if dist:
                distance_list.append(dist)
            if camera_coordinate:
                x_list.append(camera_coordinate[0])
                y_list.append(camera_coordinate[1])
                z_list.append(camera_coordinate[2])
        distance_list = np.array(distance_list)
        distance_list = np.sort(distance_list)[randnum // 2 - randnum // 4:randnum // 2 + randnum // 4]
        x_list = np.array(x_list)
        x_list = np.sort(x_list)[randnum // 2 - randnum // 4:randnum // 2 + randnum // 4]
        y_list = np.array(y_list)
        y_list = np.sort(y_list)[randnum // 2 - randnum // 4:randnum // 2 + randnum // 4]
        z_list = np.array(z_list)
        z_list = np.sort(z_list)[randnum // 2 - randnum // 4:randnum // 2 + randnum // 4]
        return np.mean(distance_list), np.mean(x_list), np.mean(y_list), np.mean(z_list)

    def dectshow(org_img, boxs, depth_data, depth_intrin, process_que):
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

            cv2.putText(img, 'x:' + str(x)[:4] + 'mm',
                        (int(box[0]), int(box[1]) + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv2.putText(img, 'y:' + str(y)[:4] + 'mm',
                        (int(box[0]), int(box[1]) + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv2.putText(img, 'z:' + str(z )[:4] + 'mm',
                        (int(box[0]), int(box[1]) - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        

        cv2.imshow('dec_img', img)
        return mirobot_info_que

    # Start streaming
    pipeline.start(config)
    
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
            current_time = time.monotonic()
            depth_image = np.asanyarray(depth_frame.get_data())

            color_image = np.asanyarray(color_frame.get_data())

            results = model(color_image)
            boxs= results.pandas().xyxy[0].values
            #boxs = np.load('temp.npy',allow_pickle=True)
            info_q = dectshow(color_image, boxs, depth_image, depth_intrin, process_que)
            if (current_time - start_time) > 3:
                start_time = current_time
                process_que.put(info_q)

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

