#!/usr/bin/env python3

import math
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String
from itertools import chain

rob2_laser_info = LaserScan()
agent_msg = 'clear'
current_state = 0
	
def rob2LaserMessageReceived(msg):
	global rob2_laser_info
	rob2_laser_info = msg
	#print(' - '.join(map(str, rob1_laser_info.ranges)))
	
def agentMessageReceived(msg):
	global agent_msg
	agent_msg = msg

def pubvel():
	rospy.sleep(2)	# Need time for robot sensors to work and bring in data
	global rob2_laser_info
	global current_state
	global agent_msg
	cmd_vel_pub2 = rospy.Publisher('/robot2/cmd_vel', Twist, queue_size=1000)
	agent_pub = rospy.Publisher('/ros_to_java', String, queue_size=1000)
	rate = rospy.Rate(10)
	while not rospy.is_shutdown():
		twist2 = Twist()
		
		if current_state == 0:
			# Driving forward
			twist2.linear.x = 8.0
			twist2.angular.z = 0.0
			current_state = 1
			print('state 0')
			print(agent_msg)

		elif current_state == 1:
			print('state 1')
			# Wall following
			if rob2_laser_info.ranges[45] < 1.0 and rob2_laser_info.ranges[135] > 1.0:
				twist2.linear.x = 8.0
				twist2.angular.z = 0.3
			if rob2_laser_info.ranges[45] > 1.0 and rob2_laser_info.ranges[135] < 1.0:
				twist2.linear.x = 8.0
				twist2.angular.z = -0.3
			
			# Checking agent messages
			if agent_msg == 'clear':
				current_state = 2
			elif 'turn_left' in str(agent_msg):
				current_state = 3
		
		elif current_state == 2:
			print('state 2')
			# Check for object in front of robots
			# Chain together ranges for iteration over frontal laser scanner sensors
			for index in chain(range(324, 360, 2), range(0, 35, 2)):
				if rob2_laser_info.ranges[index] < 0.8:
					robot_index = 2
					agent_pub.publish('front_object_robot2')
					break
			current_state = 0

		elif current_state == 3:
			print('state 3')
			# Object forward - turning left
			twist2.linear.x = 0.0
			twist2.angular.z = 1.0
			if rob2_laser_info.ranges[0] > 3.0:
				agent_msg = 'clear'
				robot_index = 0
				current_state = 0
			
		cmd_vel_pub2.publish(twist2)
		rate.sleep()

if __name__ == '__main__':
	rospy.init_node('movement2')
	rospy.Subscriber('/robot2/scan', LaserScan, rob2LaserMessageReceived)
	rospy.Subscriber('/java_to_ros', String, agentMessageReceived)
	
	try:
		pubvel()
	except rospy.ROSInterruptException:
		pass
		
	rospy.spin()
