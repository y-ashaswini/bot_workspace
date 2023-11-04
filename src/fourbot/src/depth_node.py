#!/usr/bin/env python

import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class image_converter:
 
  def __init__(self):
    # PUBLISH THE IMAGE WITH A CIRCLE IN THE MIDDLE (NOT REQUIRED)
    # PUBLISH THE DISTANCE FROM ROVER TO OBSTACLE 
    self.image_pub = rospy.Publisher("depthcam/color/img_opencv",Image, queue_size=10)
    self.dist_pub = rospy.Publisher("depthcam/color/distance_opencv",String, queue_size=10)

    self.bridge = CvBridge()
    
    # Subscriber to IMAGE RAW TOPIC
    self.image_sub = rospy.Subscriber("depthcam/depth/image_raw",Image,self.callback)

  def callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "32FC1")
    except CvBridgeError as e:
      print(e)

    f = cv_image.shape
    cols = f[0]
    rows = f[1]
    # image_raw contains the raw uint16 depths in mm from the kinect. image contains float depths in m

    if cols > 60 and rows > 60 :
      cv2.circle(cv_image, (int(rows/2), int(cols/2)), 50, 255)

    cv2.imshow("Image window", cv_image)
    cv2.waitKey(3)

    try:
      self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "32FC1"))
      self.dist_pub.publish(str(cv_image[int(rows/2)][int(cols/2)]))
    except CvBridgeError as e:
      print(e)

def main(args):
  ic = image_converter()
  rospy.init_node('image_converter', anonymous=True)
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
    
  cv2.destroyAllWindows()



if __name__ == '__main__':
  main(sys.argv)  
