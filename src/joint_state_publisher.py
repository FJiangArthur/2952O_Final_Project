#!/usr/bin/env python

# Don't forget to chmod +x
import rospy
from sensor_msgs.msg import JointState
from std_msgs.msg import Header, String
from cv_bridge import CvBridge, CvBridgeError
from depthai_ros_msgs.msg import SpatialDetectionArray
import cv2

# a subscriber subscribe to segmented instance information, send to backend service for processing
# Once the backend service gets the information, we publish using joint_state_publisher
bridge = CvBridge()
class js_publisher(object):
    def __init__(self):
        self.descriptions = ""
        self.obj_pos_publisher = rospy.Publisher('joint_states', JointState, queue_size=10)


class seg_box_subscriber(object):
    def __init__(self):
        self.descriptions = ""
        self.results = None
        self.bbox = None
        self.position = None
        self.img_frame = None

        self.publisher = js_publisher()
        rospy.Subscriber('/object_position', String, self.update_joint_state_callback)


    def update_joint_state_callback(self, seg_box_msg):

        joint_state_str = JointState()
        joint_state_str.header = Header()
        joint_state_str.header.stamp = rospy.Time.now()
        joint_state_str.name = ['joint0', 'joint1', 'joint2', 'joint3']
        joint_state_str.position = [3, 0.5418, -1.7297, -3.1017]
        joint_state_str.velocity = []
        joint_state_str.effort = []
        pub.publish(joint_state_str)
        self.publisher.publish(joint_state_str)


# Main function.
if __name__ == '__main__':
    # Initialize the node and name it.
    rospy.init_node('joint_state_publisher', anonymous=False, log_level=rospy.WARN)
    rate = rospy.Rate(1)  # 1Hz


    while not rospy.is_shutdown():
        hello_str.header.stamp = rospy.Time.now()
        pub.publish(hello_str)
        rate.sleep()
