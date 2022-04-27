#!/usr/bin/env python

# Don't forget to chmod +x
import rospy
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge, CvBridgeError
from depthai_ros_msgs.msg import SpatialDetectionArray
import cv2


bridge = CvBridge()
class yolo_publisher(object):
    def __init__(self):
        self.descriptions = ""
        self.obj_pos_publisher = rospy.Publisher('object_position', String, queue_size=10)
        self.seg_img_publisher = rospy.Publisher('segmented_img', Image, queue_size=10)

    def show_image(self, img):
        cv2.imshow("Image Window", img)
        cv2.waitKey(3)

    def publish_obj_pos(self, results, bbox, position):
        if None in (results, bbox, position):
            return

        rospy.loginfo('obj pos publishing')
        self.obj_pos_publisher.publish({"results":results, "bbox":bbox, "position":position})


    def publish_segmented_img(self, cv2_img, results, bbox, position):
        if cv2_img is None:
            print(bbox)
            return
        segmented_img = cv2_img.copy()

        for i in range(len(bbox)):
            top_left = (int(bbox[i].center.x - bbox[i].size_x // 2), int(bbox[i].center.y + bbox[i].size_y // 2))
            top_right = (int(bbox[i].center.x + bbox[i].size_x // 2), int(bbox[i].center.y + bbox[i].size_y // 2))
            bot_left = (int(bbox[i].center.x - bbox[i].size_x // 2), int(bbox[i].center.y - bbox[i].size_y // 2))
            bot_right = (int(bbox[i].center.x + bbox[i].size_x // 2), int(bbox[i].center.y - bbox[i].size_y // 2))

            cv2.rectangle(segmented_img,
                          top_left,  # upper left
                          bot_right,  # lower right
                          (0, 255, 0),  # color
                          thickness=2
                          )
        self.show_image(segmented_img)
        self.seg_img_publisher.publish(bridge.cv2_to_imgmsg(segmented_img, encoding="passthrough"))


class yolo_subscriber(object):
    def __init__(self):
        self.descriptions = ""
        self.results = None
        self.bbox = None
        self.position = None
        self.img_frame = None

        self.publisher = yolo_publisher()
        rospy.Subscriber('/yolov4_publisher/color/image', Image, self.rgb_callback)
        rospy.Subscriber('/yolov4_publisher/color/yolov4_Spatial_detections', SpatialDetectionArray, self.segmentation_callback)

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

        self.publisher.publish_segmented_img(self.img_frame, self.results,self.bbox,self.position)


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
        rospy.loginfo(seg_msg.header)
        detections = seg_msg.detections
        obj_counts = len(detections)
        self.results = [0] * obj_counts
        self.bbox = [0] * obj_counts
        self.position = [0] * obj_counts

        for i in range(obj_counts):
            if detections[i] is not None:
                self.results[i] = detections[i].results
                self.bbox[i] = detections[i].bbox
                # world_pos_x = description.position.x
                # world_pos_y = description.position.y
                # world_pos_z = description.position.z
                self.position[i] = detections[i].position

        self.publisher.publish_obj_pos(self.results, self.bbox, self.position)


    def loop(self):
        rospy.logwarn("Starting Loop...")
        rospy.spin()

# Main function.
if __name__ == '__main__':
    # Initialize the node and name it.
    rospy.init_node('yolov4_processor', anonymous=False, log_level=rospy.WARN)
    # Initialize an OpenCV Window named "Image Window"
    cv2.namedWindow("Image Window", 1)
    sub = yolo_subscriber()
    pub = sub.publisher
    sub.loop()
