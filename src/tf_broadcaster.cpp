#include <ros/ros.h>
#include <tf/transform_broadcaster.h>

int main(int argc, char** argv){
  ros::init(argc, argv, "robot_tf_publisher");
  ros::NodeHandle n;

  ros::Rate r(100);

  tf::TransformBroadcaster broadcaster;

  while(n.ok()){
    broadcaster.sendTransform(
      tf::StampedTransform(
      // For Alejandro and Taraun:

      /*
      Here is the place where we change the location of the camera:
      x, y, z relative to the center of the Mirobot:
      20cm to base of mirobot.
      */
        tf::Transform(tf::Quaternion(0, 0, 0, 1), tf::Vector3(0.2, 0.2, 0.2)),
        ros::Time::now(),"base_link", "base_laser"));
    r.sleep();
  }
}