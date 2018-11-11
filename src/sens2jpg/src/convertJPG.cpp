#include "ros/ros.h"
#include "std_msgs/String.h"
#include "sensor_msgs/Image.h"

void _callback_OnRecieveImage(const sensor_msgs::Image::ConstPtr& msg){

}

int main(int argc, char **argv)
{
  ros::init(argc, argv, "listener");
  ros::NodeHandle n;
  ros::Subscriber _sub_Image = n.subscribe("/camera/image_raw", 5, _callback_OnRecieveImage);
  ros::spin();
  return 0;
}