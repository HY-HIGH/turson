#!/usr/bin/env python 
#-*- coding:utf-8 -*-


import rospy 
from geometry_msgs.msg import PoseStamped


rospy.init_node('move_robot', anonymous=False)

def cb_destination(data): 
    
    
    goto_x = data.pose.position.x
    goto_y = data.pose.position.y
    goto_z = data.pose.position.z
    orientation_x = data.pose.orientation.x
    orientation_y = data.pose.orientation.y
    orientation_z = data.pose.orientation.z
    orientation_w = data.pose.orientation.w
    print("-----------------------")
    print("I will go x   : ",goto_x)
    print("I will go y   : ",goto_y)
    print("I will go y   : ",goto_z)
    print("orientation x : ",orientation_x)
    print("orientation y : ",orientation_y)
    print("orientation z : ",orientation_z)
    print("orientation w : ",orientation_w)
   # 퍼블리시 할 위치 값
    goto_action = PoseStamped() #instance
    goto_action.header.stamp = rospy.Time.now()
    goto_action.header.frame_id = "map"
    goto_action.pose.position.x = goto_x
    goto_action.pose.position.y = goto_y
    goto_action.pose.position.z = goto_z
    goto_action.pose.orientation.x = orientation_x
    goto_action.pose.orientation.y = orientation_y
    goto_action.pose.orientation.z = orientation_z
    goto_action.pose.orientation.w = orientation_w
    
    
    pub.publish(goto_action)
    
    
sub = rospy.Subscriber('set_robot_destination',PoseStamped, cb_destination) 

pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=10)

rospy.spin()
