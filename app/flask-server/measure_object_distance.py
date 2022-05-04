# https://pysource.com
from flask import Flask, make_response
import cv2
from realsense_camera import *
from mask_rcnn import *
import matplotlib
from matplotlib import pylab as plt
matplotlib.use('Agg')


def start_process():
    # Load Realsense camera
    rs = RealsenseCamera()
    mrcnn = MaskRCNN()

    while True:
        # Get frame in real time from Realsense camera
        ret, bgr_frame, depth_frame = rs.get_frame_stream()

        # Get object mask
        boxes, classes, contours, centers = mrcnn.detect_objects_mask(
            bgr_frame)

        # Draw object mask
        bgr_frame = mrcnn.draw_object_mask(bgr_frame)

        # Show depth info of the objects
        mrcnn.draw_object_info(bgr_frame, depth_frame)

        # cv2.imshow("depth frame", depth_frame)
        # cv2.imshow("Bgr frame", bgr_frame)

        # https://medium.datadriveninvestor.com/video-streaming-using-flask-and-opencv-c464bf8473d6

        retval, buffer = cv2.imencode('.png', depth_frame)
        response = make_response(buffer.tobytes())
        yield (b'--frame\r\n'
               b'Content-Type: image/png\r\n\r\n' + response + b'\r\n\r\n')

        key = cv2.waitKey(1)
        if key == 27:
            break

    rs.release()
    cv2.destroyAllWindows()


def run():
    yield start_process()
