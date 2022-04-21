#!/usr/bin/env python3

import rospy
import cv2
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

red_lower_threshold = np.array([0, 50, 50])
red_upper_threshold = np.array([10, 255, 255])
#green_threshold
#blue_threshold

def imageReceived1(msg):
	bridge = CvBridge()
	
	try:
		cv_image = bridge.imgmsg_to_cv2(msg, 'bgr8')
		thresholding(cv_image)
	except CvBridgeError as e:
		print(e)
	
def imageReceived2(msg):
	bridge = CvBridge()
	
	try:
		cv_image = bridge.imgmsg_to_cv2(msg, 'bgr8')
		thresholding(cv_image)
	except CvBridgeError as e:
		print(e)

def thresholding(cv_image):
	agent_pub = rospy.Publisher('/visual_contours', Float32, queue_size=1000)	
	hsv_frame = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
	img_threshold = cv2.inRange(hsv_frame, red_lower_threshold, red_upper_threshold)
	#cv2.imshow("Image threshold", img_threshold)
	#cv2.waitKey(3)
	contours, hierarchy = cv2.findContours(img_threshold, 1, 2)
	if len(contours) > 0:
		cnt = contours[0]
		agent_pub.publish(cv2.contourArea(cnt))
	else:
		agent_pub.publish(0.0)
	

if __name__ == '__main__':
	rospy.init_node('colour_detector')
	
	try:
		#rospy.Subscriber('/robot1/camera/rgb/image_raw', Image, imageReceived1)
		rospy.Subscriber('/robot2/camera/rgb/image_raw', Image, imageReceived2)
	except rospy.ROSInterruptException:
		pass
		
	rospy.spin()
