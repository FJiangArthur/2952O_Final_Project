from flask import Flask, Response

from realsense import *
from webcam import *
from web_mask_rcnn import *

app = Flask(__name__)

_video_cam = VideoCamera()
_realsense = Realsense()
mrcnn = WebMaskRCNN()


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def genRealsense(camera):
    while True:
        # frame = camera.get_frame_stream()
        # yield (b'--frame\r\n'
        #        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

        # Get frame in real time from Realsense camera
        ret, bgr_frame, depth_frame = camera.get_frame_stream()

        print("Got bgr_frame, depth_frame")

        # Get object mask
        boxes, classes, contours, centers = mrcnn.detect_objects_mask(
            bgr_frame)

        # Draw object mask
        bgr_frame = mrcnn.draw_object_mask(bgr_frame)

        # Show depth info of the objects
        mrcnn.draw_object_info(bgr_frame, depth_frame)

        # cv2.imshow("depth frame", depth_frame)
        # cv2.imshow("Bgr frame", bgr_frame)

        ret, depth_jpg = cv2.imencode('.jpg', depth_frame)
        ret, color_jpg = cv2.imencode('.jpg', bgr_frame)

        depth_jpg = depth_jpg.tobytes()
        color_jpg = color_jpg.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + color_jpg + b'\r\n\r\n')

        key = cv2.waitKey(1)
        if key == 27:
            break

    _realsense.release()
    cv2.destroyAllWindows()


@ app.route('/realsenseMask')
def realsense():
    print("hit /realsenseMask flask route")

    return Response(genRealsense(_realsense),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@ app.route('/realsenseYolo')
def realsense():
    print("hit /realsenseYolo flask route")

    # return Response(genRealsense(_realsense),
    #                 mimetype='multipart/x-mixed-replace; boundary=frame')


@ app.route('/video_feed')
def video_feed():
    print("hit /video_feed flask route")

    return Response(gen(_video_cam),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@ app.route('/members')
def members():
    return {'members': ['John', 'Mary', 'Bob']}


if __name__ == '__main__':
    app.run(debug=True)
