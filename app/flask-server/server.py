from flask import Flask, Response
import pyrealsense2 as rs
import numpy as np
import cv2

# from realsense_camera import *
# from mask_rcnn import *

# from measure_object_distance import run

app = Flask(__name__)


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(1)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        ret, frame = self.video.read()
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()


class RealsenseCamera:
    def __init__(self):
        # Configure depth and color streams
        self.pipeline = rs.pipeline()

        self.config = rs.config()

        # Get device product line for setting a supporting resolution
        self.pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
        self.pipeline_profile = self.config.resolve(self.pipeline_wrapper)
        self.device = self.pipeline_profile.get_device()
        self.device_product_line = str(
            self.device.get_info(rs.camera_info.product_line))

        found_rgb = False
        for s in self.device.sensors:
            if s.get_info(rs.camera_info.name) == 'RGB Camera':
                print("Found realseanse")
                found_rgb = True
                break
        if not found_rgb:
            print("The demo requires Depth camera with Color sensor")
            exit(0)

        self.config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

        if self.device_product_line == 'L500':
            self.config.enable_stream(
                rs.stream.color, 960, 540, rs.format.bgr8, 30)
        else:
            self.config.enable_stream(
                rs.stream.color, 640, 480, rs.format.bgr8, 30)

        # Start streaming
        self.pipeline.start(self.config)
        align_to = rs.stream.color
        self.align = rs.align(align_to)

        print("Stream has started!!")

    def get_frame_stream(self):
        # Wait for a coherent pair of frames: depth and color
        frames = self.pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        # if not depth_frame or not color_frame:
        #     continue

        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(
            depth_image, alpha=0.03), cv2.COLORMAP_JET)

        depth_colormap_dim = depth_colormap.shape
        color_colormap_dim = color_image.shape

        # If depth and color resolutions are different, resize color image to match depth image for display
        if depth_colormap_dim != color_colormap_dim:
            resized_color_image = cv2.resize(color_image, dsize=(
                depth_colormap_dim[1], depth_colormap_dim[0]), interpolation=cv2.INTER_AREA)
            images = np.hstack((resized_color_image, depth_colormap))
        else:
            images = np.hstack((color_image, depth_colormap))

        ret, jpeg = cv2.imencode('.jpg', images)
        return jpeg.tobytes()

    def __del__(self):
        self.pipeline.stop()
        self.video.release()


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def genRealsense(camera):
    while True:
        frame = camera.get_frame_stream()
        # print(frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/realsense')
def realsense():
    print("hit realsense member")

    # run measure_object_distance
    # yield run()

    # return "completed"
    return Response(genRealsense(RealsenseCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/members')
def members():
    return {'members': ['John', 'Mary', 'Bob']}


if __name__ == '__main__':
    app.run(debug=True)
