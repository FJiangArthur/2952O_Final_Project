#!/usr/bin/env python

# Don't forget to chmod +x 

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import cv2
import matplotlib.pyplot as plt
bridge = CvBridge()


def show_image(img):
    cv2.imshow("Image Window", img)
    cv2.waitKey(3)

def callback(img_msg):
    rospy.loginfo(img_msg.header)
    cv2_img = None
    rospy.loginfo('Image received...')
    try:
        # Convert your ROS Image message to OpenCV2
        cv2_img = bridge.imgmsg_to_cv2(img_msg, "passthrough") #bgr8
    except CvBridgeError, e:
        rospy.logerr("CvBridge Error: {0}".format(e))

    # Show the converted image
    show_image(cv2_img)


# This ends up being the main while loop.
def rgb_listener(topic_name='/yolov4_publisher/color/image'):
    rospy.init_node('rgb_listener', anonymous=False)
    # Create a subscriber with appropriate topic, custom message and name of callback function.
    rospy.Subscriber(topic_name, Image, callback)
    # Wait for messages on topic, go to callback function when new messages arrive.
    rospy.spin()


def depth_listener(topic_name='/yolov4_publisher/depth/image'):
    rospy.init_node('depth_listener', anonymous=False)
    # Create a subscriber with appropriate topic, custom message and name of callback function.
    rospy.Subscriber(topic_name, Image, callback)
    # Wait for messages on topic, go to callback function when new messages arrive.
    rospy.spin()

# Main function.
if __name__ == '__main__':
    # Initialize the node and name it.
    # Go to the main loop.
    # Initialize an OpenCV Window named "Image Window"
    cv2.namedWindow("Image Window", 1)
    rgb_listener()
    test_loop_rate = rospy.Rate(1)
    test_loop_rate.sleep()