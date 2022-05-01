#!/usr/bin/env python
import rospy

# Because of transformations
import tf_conversions
import tf2_ros
import geometry_msgs.msg


def handle_target_pose(msg):
    br = tf2_ros.TransformBroadcaster()
    t = geometry_msgs.msg.TransformStamped()

    # pose_goal = geometry_msgs.msg.Pose()
    # pose_goal.orientation.w = 1.0
    # pose_goal.position.x = 0.4
    # pose_goal.position.y = 0.1
    # pose_goal.position.z = 0.4

    t.header.stamp = rospy.Time.now()
    # Name of the frame we are transforming from
    t.header.frame_id = "base_depthai"
    # Name of the frame translating to
    t.child_frame_id = "base_link"

    t.transform.translation.x = msg.position.x
    t.transform.translation.y = msg.position.y
    t.transform.translation.z = msg.position.z
    # (roll, pitch, yaw)
    q = tf_conversions.transformations.quaternion_from_euler(0, 0, 0)
    t.transform.rotation.x = q[0]
    t.transform.rotation.y = q[1]
    t.transform.rotation.z = q[2]
    t.transform.rotation.w = q[3]

    br.sendTransform(t)


if __name__ == '__main__':
    rospy.init_node('tf2_depthai_broadcaster')

    # This one listens to the poses
    rospy.Subscriber('depthai_target_pose',
                     geometry_msgs.msg.Pose,
                     handle_target_pose)
    rospy.spin()