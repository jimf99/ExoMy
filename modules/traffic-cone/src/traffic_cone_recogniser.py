#!/usr/bin/env python

# subscribe to [sensor_msgs/Image] /pi_cam
# grab all the bytes
# post to local docker hosted azureML object recognizer
# retrieve JSON results
# parse
# publish /traffic-cone-bounding-box format unknown
# wait for next one.

from wsgiref import headers

from flask import request
from numpy import append
import rospy
import requests
import base64
import io
import struct
from sensor_msgs.msg import Image

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "image data recieved: data.data type: " + str(type(data.data)))
    #print("here is the data.data: " + data.data)
    #dataStage1 = data.data.replace('[', '')
    #dataStage2 = dataStage1.replace(']', '')
    #dataToStrArray = data.data.split(',') # dataStage2.split(',')

    myByteArray = bytearray(data.data)
    print(str(type(myByteArray)))
    myStruct = struct.unpack('>' + 'B'*len(data.data), data.data)
    print(str(type(myStruct)))

    #print(myStruct)

    #print (myByteArray)
    #print(dataToStrArray)

    #desired_array = [int(numeric_string) for numeric_string in data.data]
    #print(desired_array)
    #dataToSend = [int(i) for i in dataToStrArray]
    #print(dataToSend)

    # print("data: " + base64.encode(data.data, dataToSend))

    # new_file = open('/tmp/temp.jpg', 'wb')
    # new_file.write(data.data)
    # new_file.close()

    new_file = open('/tmp/temp1.jpg', 'wb')
    new_file.write(myStruct)
    new_file.close()

    #new_test = open('/tmp/temp.jpg', 'rb')
    my_files={'files': io.BytesIO(myStruct)}
    #test_file = {'files': open('/root/exomy_ws/src/traffic-cone/test_file.jpg', 'rb')}
    #test_file = open('/root/exomy_ws/src/traffic-cone/test_file.jpg', 'rb')
    my_headers = {"content-type":"image/jpeg"}
    azureMlImage = "http://192.168.1.89:8181/image"
    azureMLUrl = "http://192.168.1.89:8181/url"
    raw_image_url ="http://192.168.1.89:8080/snapshot"
    PARAMS = {'topic':'/pi_cam/image_raw'}

    #imageGet = requests.get(raw_image_url, PARAMS)
    # with open('/root/exomy_ws/src/traffic-cone/test_file_url.jpg', 'wb') as fd:
    #     for chunk in imageGet.iter_content(chunk_size=128):
    #         fd.write(chunk)

    x = requests.post(azureMlImage, my_files, headers = my_headers) # data = base64.encodebytes(data.data))
    #x = requests.post(azureMlImage, new_test, headers = my_headers)

    rospy.loginfo("Result: " + x.text)

    # test_file.seek(0)
    # print(test_file)
    # print("blah")

if __name__ == "__main__":
    rospy.init_node('traffic-cone-recognizer', anonymous=True)

    rospy.Subscriber("/pi_cam/image_raw", Image, callback)

    rospy.spin()


