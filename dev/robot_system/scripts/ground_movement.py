#!/usr/bin/env python3

import math
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

rob1_laser_info = LaserScan()

def laserMessageReceived(msg):
	global rob1_laser_info
	#rob1_laser_info.ranges = msg.ranges.copy()
	#print(' - '.join(map(str, msg.ranges)))

def pubvel():
	global rob1_laser_info
	cmd_vel_pub = rospy.Publisher('/robot1/cmd_vel', Twist, queue_size=1000)
	rate = rospy.Rate(10)
	while not rospy.is_shutdown():
		twist = Twist()
		
		#Drive forward
		twist.linear.x = 0.0
		twist.angular.z = 0.0
		#if rob1_laser_info.ranges[0] > 1.5:
		#	twist.linear.x = 0.0
			
		cmd_vel_pub.publish(twist)
		rate.sleep()

if __name__ == '__main__':
	rospy.init_node('movement')
	rospy.Subscriber('/robot1/scan', LaserScan, laserMessageReceived)
	
	try:
		pubvel()
	except rospy.ROSInterruptException:
		pass
		
	rospy.spin()
