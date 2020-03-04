#!/usr/bin/env python 
#-*- coding:utf-8 -*-
# 목표지점 받아와서 로봇 움직인다.
#쉬뱅 인터 프리터 지시줄 //파이썬이다.


import rospy #파이썬 노드
from nav_msgs.msg import Odometry # 오도메트리 서브스크라이브

global_current_position_x    =0
global_current_position_y    =0
global_current_orientation_x =0 
global_current_orientation_y =0 
global_current_orientation_z =0 
global_current_orientation_w =0 

def cb_odometry(odom_data): # 현재 위치를 current_ 로 정의 후 global에 저장
    # 수정할 변수
    #글로벌로 쓰지 않으려면 퍼블리시 하는 함수로 짜야한다.
    global global_current_position_x  
    global global_current_position_y  
    global global_current_orientation_x  
    global global_current_orientation_y  
    global global_current_orientation_z  
    global global_current_orientation_w  

    global_current_position_x = odom_data.pose.pose.position.x
    global_current_position_y = odom_data.pose.pose.position.y
    
    global_current_orientation_x = odom_data.pose.pose.orientation.x 
    global_current_orientation_y = odom_data.pose.pose.orientation.y 
    global_current_orientation_z = odom_data.pose.pose.orientation.z 
    global_current_orientation_w = odom_data.pose.pose.orientation.w 
    x=odom_data.pose.pose.orientation.x 
    #print(x)


rospy.init_node('test_odom', anonymous=True) 
rospy.Subscriber('/odom',Odometry,cb_odometry)

while not rospy.is_shutdown():
    print ('global_odom_x' , global_current_position_x)
    print ('global_odom_x' ,global_current_orientation_x )


   




