#!/usr/bin/env python3

import math
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String
from nav_msgs.msg import Odometry
from itertools import chain
import numpy as np

robot_name = 'rob2'
#msgArray = np.array([robot_name, '-'], dtype='S')
rob2_laser_info = LaserScan()
agent_msg = 'clear'
current_state = 0

def rob2LaserMessageReceived(msg):
	global rob2_laser_info
	rob2_laser_info = msg
	#print(' - '.join(map(str, rob2_laser_info.ranges)))
	
def agentMessageReceived(msg):
	global agent_msg
	agent_msg = msg
	
def odomMessageReceived(msg):
	odom_pub = rospy.Publisher('/robotPose', Odometry, queue_size=1000)
	rate = rospy.Rate(0.2)
	while not rospy.is_shutdown():
		odom_pub.publish(msg)
		rate.sleep()

def pubvel():
	rospy.sleep(2)	# Need time for robot sensors to work and bring in data
	global rob2_laser_info
	global current_state
	global agent_msg
	global msgArray
	cmd_vel_pub1 = rospy.Publisher('/robot2/cmd_vel', Twist, queue_size=1000)
	agent_pub = rospy.Publisher('/objLaserDetect', String, queue_size=1000)
	rate = rospy.Rate(10)
	while not rospy.is_shutdown():
		twist2 = Twist()
		
		if current_state == 0:
			# Driving forward
			twist2.linear.x = 2.0
			twist2.angular.z = 0.0
			current_state = 1
			print('state 0')
			print(agent_msg)

		elif current_state == 1:
			print('state 1')
			# Wall following
			if rob2_laser_info.ranges[45] < 0.4 and rob2_laser_info.ranges[135] > 0.4:
				twist2.linear.x = 2.0
				twist2.angular.z = 0.3
			if rob2_laser_info.ranges[45] > 0.4 and rob2_laser_info.ranges[135] < 0.4:
				twist2.linear.x = 2.0
				twist2.angular.z = -0.3
			
			# Checking agent messages
			if agent_msg == 'clear':
				current_state = 2
			elif 'turn_away' in str(agent_msg):
				current_state = 3
		
		elif current_state == 2:
			print('state 2')
			# Check for object in front of robots
			# Chain together ranges for iteration over frontal laser scanner sensors
			for index in chain(range(324, 360, 2), range(0, 35, 2)):
				if rob2_laser_info.ranges[index] < 0.8:
					twist2.linear.x = 0.0
					twist2.angular.z = 0.0
					agent_pub.publish('front_object_robot2')
					break
			current_state = 0

		elif current_state == 3:
			print('state 3')
			# Object forward - turning left
			twist2.linear.x = 0.0
			twist2.angular.z = 1.0
			if rob2_laser_info.ranges[0] > 0.8:
				agent_msg = 'clear'
				current_state = 0
			
		cmd_vel_pub1.publish(twist2)
		rate.sleep()

if __name__ == '__main__':
	rospy.init_node('movement2')
	rospy.Subscriber('/robot2/scan', LaserScan, rob2LaserMessageReceived)
	rospy.Subscriber('/java_to_ros/robot2', String, agentMessageReceived)
	rospy.Subscriber('/robot2/odom', Odometry, odomMessageReceived)
	
	try:
		pubvel()
	except rospy.ROSInterruptException:
		pass
		
	rospy.spin()
