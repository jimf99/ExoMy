#include "ros/ros.h"
#include "std_msgs/String.h"
#include "sensor_msgs/Image.h"

void imageRawCallback(const sensor_msgs::Image::ConstPtr& msg)
{
  ROS_INFO("I heard: [%d]", msg->data[0]);
}

int main(int argc, char **argv)
{
  /**
   * The ros::init() function needs to see argc and argv so that it can perform
   * any ROS arguments and name remapping that were provided at the command line.
   * For programmatic remappings you can use a different version of init() which takes
   * remappings directly, but for most command-line programs, passing argc and argv is
   * the easiest way to do it.  The third argument to init() is the name of the node.
   *
   * You must call one of the versions of ros::init() before using any other
   * part of the ROS system.
   */
  ros::init(argc, argv, "traffic_cone_ugh");

  ros::NodeHandle n;

  ros::Subscriber sub = n.subscribe("/pi_cam/image_raw", 1000, imageRawCallback);

  ros::spin();

  return 0;
}
