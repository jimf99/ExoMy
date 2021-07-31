#!/usr/bin/env python

# subscribe to [sensor_msgs/Image] /pi_cam
# grab all the bytes
# post to local docker hosted azureML object recognizer
# retrieve JSON results
# parse
# publish /traffic-cone-bounding-box format unknown
# wait for next one.

import rospy
from sensor_msgs.msg import Image

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "image data recieved")

if __name__ == "__main__":
    rospy.init_node('traffic-cone-recognizer', anonymous=True)

    rospy.Subscriber("/pi_cam/image_raw", Image, callback)

    rospy.spin()


