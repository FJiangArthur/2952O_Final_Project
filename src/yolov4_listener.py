#!/usr/bin/env python

# Don't forget to chmod +x
import rospy
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge, CvBridgeError
import cv2

from yolov4_publisher import yolov4_publisher

bridge = CvBridge()
class yolov4_subscriber(object):
    def __init__(self):
        self.descriptions = ""
        self.results = {}
        self.bbox = {}
        self.position = {}
        self.img_frame = None

        self.publisher = yolov4_publisher()
        rospy.Subscriber('/yolov4_publisher/color/image', Image, self.rgb_callback)
        rospy.Subscriber('/yolov4_publisher/color/yolov4_Spatial_detections', String, self.segmentation_callback)


    # def show_image(self, img):
    #     cv2.imshow("Image Window", img)
    #     cv2.waitKey(3)


    def rgb_callback(self, img_msg):
        rospy.loginfo(img_msg.header)
        cv2_img = None
        rospy.loginfo('Image received...')
        try:
            # Convert your ROS Image message to OpenCV2
            cv2_img = bridge.imgmsg_to_cv2(img_msg, "passthrough") #bgr8
        except CvBridgeError, e:
            rospy.logerr("CvBridge Error: {0}".format(e))

        # Show the converted image
        self.img_frame = cv2_img.copy()
        # self.show_image(cv2_img)

        self.publisher.publish_segmented_img()


    def segmentation_callback(self, seg_msg):
        # Sample msg with header taken from oak-d-lite #
        """
        header:
          seq: 267
          stamp:
            secs: 1651070902
            nsecs: 179045111
          frame_id: "oak_rgb_camera_optical_frame"
        detections:
          -
            results:
              -
                id: 0
                score: 0.526094436646
            bbox:
              center:
                x: 178.0
                y: 239.5
                theta: 0.0
              size_x: 410.0
              size_y: 407.0
            position:
              x: -0.00260641542263
              y: -0.0104256616905
              z: 0.376405805349
            is_tracking: False
            tracking_id: ''
        """
        rospy.login(seg_msg.header)
        description = seg_msg.descriptions

        if description is not None:
            self.results = {**description.results}
            self.bbox = {**description.bbox}
            # world_pos_x = description.position.x
            # world_pos_y = description.position.y
            # world_pos_z = description.position.z
            self.position = {**description}

            self.publisher.publish_obj_pos(self.results, self.bbox, self.position)


    def loop(self):
        rospy.logwarn("Starting Loop...")
        rospy.spin()

# Main function.
if __name__ == '__main__':
    # Initialize the node and name it.
    rospy.init_node('yolov4_listener', anonymous=False, log_level=rospy.WARN)
    # # Initialize an OpenCV Window named "Image Window"
    # cv2.namedWindow("Image Window", 1)
    sub = yolov4_subscriber()
    sub.loop()
