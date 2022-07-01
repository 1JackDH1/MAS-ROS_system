#!/usr/bin/env python3

import rospy
import cv2
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from std_msgs.msg import Float32

# Thresholds for colour detection
red_upper_threshold = np.array([10, 255, 255])
red_lower_threshold = np.array([0, 50, 50])
green_upper_threshold = np.array([70, 255, 255])
green_lower_threshold = np.array([40, 40, 40])
blue_upper_threshold = np.array([140, 255, 255])
blue_lower_threshold = np.array([100, 150, 0])

def imageReceived(msg):
	bridge = CvBridge()
	
	try:
		cv_image = bridge.imgmsg_to_cv2(msg, 'bgr8')
		thresholding(cv_image)
	except CvBridgeError as e:
		print(e)

# Function for applying image thresholding and contour area extraction
def thresholding(cv_image):
	agent_pub = rospy.Publisher('/visualDetect', Float32, queue_size=1000)	
	hsv_frame = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
	img_red_threshold = cv2.inRange(hsv_frame, red_lower_threshold, red_upper_threshold)
	img_green_threshold = cv2.inRange(hsv_frame, green_lower_threshold, green_upper_threshold)
	img_blue_threshold = cv2.inRange(hsv_frame, blue_lower_threshold, blue_upper_threshold)
	
	cv2.imshow("Original image", cv_image)
	cv2.imshow("HSV image", hsv_frame)
	cv2.imshow("Image threshold", img_green_threshold)
	cv2.waitKey(500)
	
	contours, hierarchy = cv2.findContours(img_green_threshold, 1, 2)
	if len(contours) > 0:
		cnt = contours[0]
		print(cv2.contourArea(cnt))
		agent_pub.publish(cv2.contourArea(cnt))
	else:
		agent_pub.publish(0.0)
	

if __name__ == '__main__':
	rospy.init_node('colour_detector')
	
	try:
		rospy.Subscriber('/robot1/camera/rgb/image_raw', Image, imageReceived)
		rospy.Subscriber('/robot2/camera/rgb/image_raw', Image, imageReceived)
		rospy.Subscriber('/robot3/camera/rgb/image_raw', Image, imageReceived)
		rospy.Subscriber('/robot4/camera/rgb/image_raw', Image, imageReceived)
	except rospy.ROSInterruptException:
		pass
		
	rospy.spin()
