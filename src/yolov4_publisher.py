#!/usr/bin/env python

# Don't forget to chmod +x
import rospy
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge, CvBridgeError
import cv2

from yolov4_publisher import yolov4_publisher

bridge = CvBridge()
class yolov4_publisher(object):
    def __init__(self):
        self.descriptions = ""
        self.publisher = rospy.Publisher('object_position', String, queue_size=10)
        self.publisher = rospy.Publisher('segmented_img', Image, queue_size=10)

    def show_image(self, img):
        cv2.imshow("Image Window", img)
        cv2.waitKey(3)

    def publish_obj_pos(self, results, bbox, position):
        rospy.loginfo('obj pos publishing')
        self.pub.publish({"results":results, "bbox":bbox, "position":position})


    def publish_segmented_img(self, cv2_img, results, bbox, position):
        segmented_img = cv2_img.copy()
        top_left = (bbox.center.x - bbox.size_x // 2, bbox.y + bbox.size_y // 2)
        top_right = (bbox.center.x + bbox.size_x // 2, bbox.y + bbox.size_y // 2)
        bot_left = (bbox.center.x - bbox.size_x // 2, bbox.y - bbox.size_y // 2)
        bot_right = (bbox.center.x + bbox.size_x // 2, bbox.y - bbox.size_y // 2)

        cv2.rectangle(segmented_img,
                      top_left,  # upper left
                      bot_right,  # lower right
                      (0, 255, 0),  # color
                      thickness=2,
                      lineType=cv2.LINE_8  # line type
                      )
        self.pub.publish(bridge.cv2_to_imgmsg(segmented_img, encoding="passthrough"))



# Main function.
if __name__ == '__main__':
    rospy.init_node('yolov4_publisher', anonymous=False, log_level=rospy.INFO)
    publisher = yolov4_publisher()

    # Initialize an OpenCV Window named "Image Window"
    cv2.namedWindow("Image Window", 1)

    try:
        publisher.publish_controlvalue(desiredv=1.0, encoderv=2.0)
    except rospy.ROSInterruptException:
        pass