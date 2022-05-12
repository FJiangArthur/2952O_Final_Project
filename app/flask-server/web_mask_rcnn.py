# https://pysource.com/instance-segmentation-mask-rcnn-with-python-and-opencv
from wlkata_mirobot import WlkataMirobot
import time
import cv2
import numpy as np

arm = WlkataMirobot(portname='/dev/cu.usbserial-10')
arm.home()

class WebMaskRCNN:
    def __init__(self):
        # Loading Mask RCNN

        self.net = cv2.dnn.readNetFromTensorflow("dnn/frozen_inference_graph_coco.pb",
                                                 "dnn/mask_rcnn_inception_v2_coco_2018_01_28.pbtxt")
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

        # Generate random colors
        np.random.seed(2)
        self.colors = np.random.randint(0, 255, (90, 3))

        # Conf threshold
        self.detection_threshold = 0.7
        self.mask_threshold = 0.3

        self.classes = []
        with open("dnn/classes.txt", "r") as file_object:
            for class_name in file_object.readlines():
                class_name = class_name.strip()
                self.classes.append(class_name)

        self.obj_boxes = []
        self.obj_classes = []
        self.obj_centers = []
        self.obj_contours = []

        # Distances
        self.distances = []

    def move_robot(self, cx, cy, obj_class):
        #    		spacing_mm = 100
        #    		arm.set_gripper_spacing(spacing_mm)
        #    		time.sleep(2)
        # gripper open
        #    		arm.gripper_open()
        #    		time.sleep(1)

        xNorm = cx / 1280
        yNorm = cy / 720

        xScaled = (xNorm * 450) + -215
        yScaled = 364 - ((yNorm * 200) + 117)

#    		if(cx > 800):
#    			xScaled =  (xNorm * 450) + -175
#
#    		if(cx < 800):
#
#    			xScaled =  (xNorm * 450) + -215


#    		xScaled =  round(xNorm * 300)
#    		yScaled =  round(yNorm * 300) + 50

# 		yScaled = cx / 6.4
# 		xScaled = cy / 3.6

        print("XScaled: " + str(xScaled))
        print("YScaled: " + str(yScaled))

        arm.set_tool_pose(yScaled, -xScaled, 160)

        time.sleep(1)
        time.sleep(1)

        arm.set_tool_pose(yScaled, -xScaled, 50)

        arm.pump_suction()

        time.sleep(1)

        arm.set_tool_pose(yScaled, -xScaled, 160)
        time.sleep(1)

        if(obj_class == "cow" or obj_class == "cat" or obj_class == "bird" or obj_class == "dog" or obj_class == "teddy bear"):
            arm.set_tool_pose(127,  225, 160)
            time.sleep(1)
            arm.set_tool_pose(127,  225, 50)
            arm.pump_off()
            time.sleep(1)
            arm.set_tool_pose(127,  225, 160)

        if(obj_class == "truck" or obj_class == "car" or obj_class == "bus"):
            arm.set_tool_pose(37,  175, 160)
            time.sleep(1)
            arm.set_tool_pose(37,  175, 50)
            arm.pump_off()
            time.sleep(1)
            arm.set_tool_pose(37,  175, 160)

        # gripper close
#    		arm.gripper_close()
        time.sleep(1)
        arm.set_tool_pose(177,  45, 121)
        # api.go_to_zero()

    def detect_objects_mask(self, bgr_frame):
        blob = cv2.dnn.blobFromImage(bgr_frame, swapRB=True)
        self.net.setInput(blob)

        boxes, masks = self.net.forward(
            ["detection_out_final", "detection_masks"])

        # Detect objects
        frame_height, frame_width, _ = bgr_frame.shape
        detection_count = boxes.shape[2]

#         print(frame_height)
#         print(frame_width)

        # Object Boxes
        self.obj_boxes = []
        self.obj_classes = []
        self.obj_centers = []
        self.obj_contours = []

        for i in range(detection_count):
            box = boxes[0, 0, i]
            class_id = box[1]
            score = box[2]
            color = self.colors[int(class_id)]
            if score < self.detection_threshold:
                continue

            # Get box Coordinates
            x = int(box[3] * frame_width)
            y = int(box[4] * frame_height)
            x2 = int(box[5] * frame_width)
            y2 = int(box[6] * frame_height)
            self.obj_boxes.append([x, y, x2, y2])

            cx = (x + x2) // 2
            cy = (y + y2) // 2
            self.obj_centers.append((cx, cy))

            # append class
            self.obj_classes.append(class_id)

            # Contours
            # Get mask coordinates
            # Get the mask
            mask = masks[i, int(class_id)]
            roi_height, roi_width = y2 - y, x2 - x
            mask = cv2.resize(mask, (roi_width, roi_height))
            _, mask = cv2.threshold(
                mask, self.mask_threshold, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(
                np.array(mask, np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            self.obj_contours.append(contours)

        return self.obj_boxes, self.obj_classes, self.obj_contours, self.obj_centers

    def draw_object_mask(self, bgr_frame):
        # loop through the detection
        for box, class_id, contours in zip(self.obj_boxes, self.obj_classes, self.obj_contours):
            x, y, x2, y2 = box
            roi = bgr_frame[y: y2, x: x2]
            roi_height, roi_width, _ = roi.shape
            color = self.colors[int(class_id)]

            roi_copy = np.zeros_like(roi)

            for cnt in contours:
                # cv2.f(roi, [cnt], (int(color[0]), int(color[1]), int(color[2])))
                cv2.drawContours(
                    roi, [cnt], - 1, (int(color[0]), int(color[1]), int(color[2])), 3)
                cv2.fillPoly(roi_copy, [cnt], (int(
                    color[0]), int(color[1]), int(color[2])))
                roi = cv2.addWeighted(roi, 1, roi_copy, 0.5, 0.0)
                bgr_frame[y: y2, x: x2] = roi
        return bgr_frame

    def draw_object_info(self, bgr_frame, depth_frame):
        # loop through the detection
        depth_mm = 0

        for box, class_id, obj_center in zip(self.obj_boxes, self.obj_classes, self.obj_centers):
            x, y, x2, y2 = box

            color = self.colors[int(class_id)]
            color = (int(color[0]), int(color[1]), int(color[2]))

            cx, cy = obj_center

            depth_mm = depth_frame[cy, cx]

            cv2.line(bgr_frame, (cx, y), (cx, y2), color, 1)
            cv2.line(bgr_frame, (x, cy), (x2, cy), color, 1)

            class_name = self.classes[int(class_id)]
            cv2.rectangle(bgr_frame, (x, y), (x + 250, y + 70), color, -1)
            cv2.putText(bgr_frame, class_name.capitalize(),
                        (x + 5, y + 25), 0, 0.8, (255, 255, 255), 2)
            cv2.putText(bgr_frame, "{} cm".format(depth_mm / 10),
                        (x + 5, y + 60), 0, 1.0, (255, 255, 255), 2)
            cv2.rectangle(bgr_frame, (x, y), (x2, y2), color, 1)
            print("Class: " + class_name)
            print("Coords: x- " + str(cx) + ", y- " + str(cy))
            if(class_name == "cow" or class_name == "cat" or class_name == "bird" or class_name == "dog" or class_name == "bear" or class_name == "truck" or class_name == "car" or class_name == "bus" or class_name == "teddy bear"):
                if(cx > 400):
                    self.move_robot(cx, cy, class_name)

#         if(depth_mm / 10 > 50):
#         	self.move_robot()
        return bgr_frame
