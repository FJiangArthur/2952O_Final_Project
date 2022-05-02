#!/usr/bin/env python
# license removed for brevity
import rospy
import geometry_msgs.msg

def talker():
    pub = rospy.Publisher('depthai_target_pose', geometry_msgs.msg.Pose, queue_size=1)
    rospy.init_node('depthai_target_pose', anonymous=True)
    rate = rospy.Rate(0.1) # 10hz
    while not rospy.is_shutdown():
        # TODO: Change this to real target goal
        hello_pose = geometry_msgs.msg.Pose()
        hello_pose.orientation.w = 0
        hello_pose.position.x = 0.1
        hello_pose.position.y = 0.1
        hello_pose.position.z = 0.1
        pub.publish(hello_pose)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass