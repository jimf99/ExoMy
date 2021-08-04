#!/usr/bin/env python

# subscribe to [sensor_msgs/Image] /pi_cam
# grab all the bytes
# post to local docker hosted azureML object recognizer
# retrieve JSON results
# parse
# publish /traffic-cone-bounding-box format unknown
# wait for next one.

from wsgiref import headers
import rospy
import requests
import base64
import io
from sensor_msgs.msg import Image

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "image data recieved: data.data type: " + str(type(data.data)))
    dataStage1 = data.data.replace('[', '')
    dataStage2 = dataStage1.replace(']', '')
    dataToStrArray = dataStage2.split(',')

    print(dataToStrArray)

    dataToSend = [int(i) for i in dataToStrArray]
    
    # print("data: " + base64.encode(data.data, dataToSend))

    #my_files={'files': io.BytesIO(data.data)}
    my_headers = {"content-type":"image/jpeg"}
    azureMlUrl = "http://192.168.1.89:8181/image"
    x = requests.post(azureMlUrl, dataToSend) #, files = my_files, headers = my_headers) # data = base64.encodebytes(data.data))

    rospy.loginfo("Result: " + x.text)


if __name__ == "__main__":
    rospy.init_node('traffic-cone-recognizer', anonymous=True)

    rospy.Subscriber("/pi_cam/image_raw", Image, callback)

    rospy.spin()


