#!/usr/bin/env python
from __future__ import print_function

#import roslib
#.load_manifest('my_package')
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import CompressedImage

import google_api

class ImageMsg2Image:
    def __init__(self, image_topic = "/raspicam_node/image/compressed"):
        self.image_sub = rospy.Subscriber(image_topic, CompressedImage, self.callback_Image)
        self.bridge = CvBridge()
        self.cv_image = 0
    def callback_Image(self,data):
        try:
            self.cv_image = self.bridge.compressed_imgmsg_to_cv2(data)
        except CvBridgeError as e:
            print(e)

def write_image(path,Im):
    cv2.imwrite(path, Im)


def main(args):
    file_id = ''
    file_id_array = []
    num_of_images = 5
    for i in range(0,num_of_images+1):
        file_id_array.append('')

    count = 0
    array_indx = 1
    google_api.init_api()
    rospy.init_node('ImageMsg2Image', anonymous=True)
    Im = ImageMsg2Image()
    rate = rospy.Rate(.5) # 1hz
    try:
        while not rospy.is_shutdown():
            write_image('/home/engietoday/Desktop/test/test.jpg',Im.cv_image)
            count = count + 1
            file_id = google_api.uploadImage(count)
            for i in range(0,num_of_images):
                file_id_array[i] = file_id_array[i+1]
            file_id_array[num_of_images] = file_id
            google_api.deleteImage(file_id_array[0])
            print(file_id_array)
            if count == num_of_images:
                count = 0
            rate.sleep()        

    except KeyboardInterrupt:
        print("Shutting down")  
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)