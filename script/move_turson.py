#!/usr/bin/env python 
#-*- coding:utf-8 -*-
# 목표지점 받아와서 로봇 움직인다.
# 쉬뱅 인터 프리터 지시줄 //파이썬이다.


import rospy #파이썬 노드
from geometry_msgs.msg import PoseStamped
from move_base_msgs.msg import MoveBaseActionResult
# global_result = False

rospy.init_node('move_turson', anonymous=False)



def cb_destination(data): # data 메시지 받아옴 (목적지 데이터) ,처리 메세지가 도착할때 마다 콜백 함수 호출
    #서브스크라이브한 위치값
    
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
    print('[INFO] : waiting for command...')

    
    
rospy.Subscriber('/set_robot_destination',PoseStamped, cb_destination) #함수 호출
print('[INFO] : waiting for command...')

pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=10)
rospy.spin()




