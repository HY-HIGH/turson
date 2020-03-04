#!/usr/bin/env python
#-*- coding:utf-8 -*-
# 0 : patrol
# 1 : navigation
# activation  조건: 사람 검출(mode == 1 ), 목적지 도착
# ------------- 


global_mode                    = 1 #  테스트용 (사람 검출 됨)

global_navigation_control      = False #사람이 탐지되고 회전하여 중간에 사람이 맞춰 지면 활성화

global_temp_position_x         = 0     
global_temp_position_y         = 0         
global_temp_orientation_x      = 0
global_temp_orientation_y      = 0
global_temp_orientation_z      = 0
global_temp_orientation_w      = 0

   

global_result                  = False #도착 여부

import rospy #로스 파이 패키지
from turson_navigation.msg import Mode 
# from actionlib_msgs.msg import GoalStatusArray
# from move_base_msgs.msg import MoveBaseActionFeedback
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Odometry # 오도메트리 서브스크라이브
from std_msgs.msg import Int64
from move_base_msgs.msg import MoveBaseActionResult


# /move_base/status (actionlib_msgs/GoalStatusArray)
# Provides status information on the goals that are sent to the move_base action.



def cb_temp_odometry(odom_data): # 순간 오도메트리

    global global_temp_position_x  
    global global_temp_position_y 
    global global_temp_orientation_x  
    global global_temp_orientation_y  
    global global_temp_orientation_z  
    global global_temp_orientation_w  

    global_temp_position_x       = odom_data.pose.pose.position.x
    global_temp_position_y       = odom_data.pose.pose.position.y 
    global_temp_orientation_x    = odom_data.pose.pose.orientation.x 
    global_temp_orientation_y    = odom_data.pose.pose.orientation.y 
    global_temp_orientation_z    = odom_data.pose.pose.orientation.z 
    global_temp_orientation_w    = odom_data.pose.pose.orientation.w 
        
def cb_mode(mode): # 1: activate navigation
    global global_mode
    global_mode = mode.data
    print ('mode : ',global_mode)
   

def cb_result(result):
    global global_result
    if result.status.status == 3:

        global_result = True
        print('navigation :',global_result)
    else :
        global_result = False
        
        
   

   

# 함수 시작부분

if __name__ == '__main__':
    try:
        rospy.init_node('navigation_status', anonymous=True)# 노드 초기화 #노드이름
        rate = rospy.Rate(1) # 발행 속도 10hz 
        rospy.Subscriber('mode_control',Int64,cb_mode) #사람 검출 여부 계속 서브 스크라이브 
        rospy.Subscriber('/move_base/result',MoveBaseActionResult,cb_result) #사람 검출 여부 계속 서브 스크라이브 

        

        # pub_mode = rospy.Publisher('/navigation_status', Int64, queue_size=10) #네비게이션 모드 발행
        pub_temp_odom = rospy.Publisher('/temp_odom', PoseStamped, queue_size=10) #그 순간의 오도메트리 발행

        
        mode = Int64()
        temp_odom = PoseStamped()

        
        print("[INFO] publish when robot reached ")

        while not rospy.is_shutdown():
            if global_result == True:
                rospy.Subscriber('/odom',Odometry,cb_temp_odometry)

                # mode.data = 1
                # pub_mode.publish(mode) # 1이 들어 올 때만 box2coordinate 노드에서 무브 로봇 으로 퍼블리시

                temp_odom.pose.position.x     =  global_temp_position_x               
                temp_odom.pose.position.y     =  global_temp_position_y 
                temp_odom.pose.position.z     =  0.0    
                temp_odom.pose.orientation.x  =  global_temp_orientation_x            
                temp_odom.pose.orientation.y  =  global_temp_orientation_y            
                temp_odom.pose.orientation.z  =  global_temp_orientation_z            
                temp_odom.pose.orientation.w  =  global_temp_orientation_w    

                pub_temp_odom.publish(temp_odom)
                print("navigation activated")
                global_result = False
                # mode.data = 0
                # pub_mode.publish(mode)
                
            # else:
            #     mode.data = 0
            #     pub_mode.publish(mode)
            #     #print("navigation deactivated")
            #     pass
                

            rate.sleep
            
            
       
    except rospy.ROSInterruptException:
        pass