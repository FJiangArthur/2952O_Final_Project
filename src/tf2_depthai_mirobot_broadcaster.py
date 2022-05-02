#!/usr/bin/env python
import rospy

# to get commandline arguments
import sys

# because of transformations
import tf

import tf2_ros
import geometry_msgs.msg

if __name__ == '__main__':
    # for i in range(len(sys.argv)):
    #     print(f'Argv number {i} is {sys.argv[i]}')

    if len(sys.argv) < 7:
        rospy.logerr('Invalid number of parameters\nusage: '
                     './tf2__depthai_broadcaster.py '
                     ' x y z roll pitch yaw')
        sys.exit(0)
    else:
        if sys.argv[1] == 'base_link':
            rospy.logerr('Your static frame child name cannot be "base_link"')
            sys.exit(0)

        rospy.init_node('tf2_depthai_broadcaster')
        broadcaster = tf2_ros.StaticTransformBroadcaster()
        static_transformStamped = geometry_msgs.msg.TransformStamped()

        static_transformStamped.header.stamp = rospy.Time.now()
        static_transformStamped.header.frame_id = "base_link"
        static_transformStamped.child_frame_id = 'base_depthai'

        static_transformStamped.transform.translation.x = float(sys.argv[1])
        static_transformStamped.transform.translation.y = float(sys.argv[2])
        static_transformStamped.transform.translation.z = float(sys.argv[3])

        quat = tf.transformations.quaternion_from_euler(
                   float(sys.argv[4]),float(sys.argv[5]),float(sys.argv[6]))
        static_transformStamped.transform.rotation.x = quat[0]
        static_transformStamped.transform.rotation.y = quat[1]
        static_transformStamped.transform.rotation.z = quat[2]
        static_transformStamped.transform.rotation.w = quat[3]

        broadcaster.sendTransform(static_transformStamped)
        rospy.spin()