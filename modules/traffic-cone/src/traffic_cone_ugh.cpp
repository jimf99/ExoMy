#include "ros/ros.h"
#include "std_msgs/String.h"
#include "sensor_msgs/Image.h"
#include <stdio.h>

void imageRawCallback(const sensor_msgs::Image::ConstPtr& msg)
{
  ROS_INFO("I heard: [%d], is size %d, array size %d", msg->data[0], sizeof(msg->data[0]), sizeof(msg->data)/sizeof(msg->data[0]));

  

  // FILE *file = fopen("image_test.jpg", "wb");
  // fwrite(msg->data, sizeof(msg->data[0]), 1920 * 480, *file);
  // fclose(file);

}

int main(int argc, char **argv)
{
  ros::init(argc, argv, "traffic_cone_ugh");

  ros::NodeHandle n;

  ros::Subscriber sub = n.subscribe("/pi_cam/image_raw", 1000, imageRawCallback);

  ros::spin();

  return 0;
}
