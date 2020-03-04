#!/usr/bin/env python
#-*- coding:utf-8 -*-
# 0 : patrol
# 1 : navigation
# activation  조건: 사람 검출(mode == 1 ), 목적지 도착
# ------------- 
global_position_x              = 0         
global_position_y              = 0         
global_position_z              = 0         
global_orientation_x           = 0     
global_orientation_y           = 0         
global_orientation_z           = 0              
global_orientation_w           = 0 

global_mode                    = 1 #  테스트용 (사람 검출 됨)

global_current_position_x      = 0     
global_current_position_y      = 0     
global_current_orientation_x   = 0     
global_current_orientation_y   = 0     
global_current_orientation_z   = 0     
global_current_orientation_w   = 0     

global_temp_position_x         = 0     
global_temp_position_y         = 0         
global_temp_orientation_x      = 0
global_temp_orientation_y      = 0
global_temp_orientation_z      = 0
global_temp_orientation_w      = 0

import rospy #로스 파이 패키지
from turson_navigation.msg import Mode 
from actionlib_msgs.msg import GoalStatusArray
from move_base_msgs.msg import MoveBaseActionFeedback
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Odometry # 오도메트리 서브스크라이브
from std_msgs.msg import Int64


# /move_base/status (actionlib_msgs/GoalStatusArray)
# Provides status information on the goals that are sent to the move_base action.



def cb_goal(goal): # goal 목적지 정보를 글로벌에 저장 (turson_move)
    global global_position_x
    global global_position_y
    global global_position_z
    global global_orientation_x
    global global_orientation_y
    global global_orientation_z
    global global_orientation_w

    global_position_x        = goal.pose.position.x
    global_position_y        = goal.pose.position.y
    global_position_z        = goal.pose.position.z
    global_orientation_x     = goal.pose.orientation.x
    global_orientation_y     = goal.pose.orientation.y
    global_orientation_z     = goal.pose.orientation.z
    global_orientation_w     = goal.pose.orientation.w

def cb_odometry(odom_data): # 현재 오도메트리 받아옴

    global global_current_position_x  
    global global_current_position_y 

    global global_current_orientation_x  
    global global_current_orientation_y  
    global global_current_orientation_z  
    global global_current_orientation_w  

    global_current_position_x       = odom_data.pose.pose.position.x
    global_current_position_y       = odom_data.pose.pose.position.y
    
    global_current_orientation_x    = odom_data.pose.pose.orientation.x 
    global_current_orientation_y    = odom_data.pose.pose.orientation.y 
    global_current_orientation_z    = odom_data.pose.pose.orientation.z 
    global_current_orientation_w    = odom_data.pose.pose.orientation.w 

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
   

def is_it_reached():
    #bool result
    error = 0.1
    error_or = 0.5

    #비교
        
    if  ((abs(global_position_x - global_current_position_x   ) < error) and (abs(global_position_y    - global_current_position_y   ) < error)):
        #if ((abs(global_orientation_x - global_current_orientation_x) < error_or) and (abs(global_orientation_y - global_current_orientation_y) < error_or) and (abs(global_orientation_z - global_current_orientation_z) < error_or) and (abs(global_orientation_w - global_current_orientation_w) < error_or) ):
        result = True
        print (result)
    else :
        result = False
        print (result)


    return result

   

# 함수 시작부분

if __name__ == '__main__':
    try:
        rospy.init_node('navigation_status', anonymous=True)# 노드 초기화 #노드이름
        rate = rospy.Rate(0.1) # 발행 속도 10hz 
        rospy.Subscriber('mode_control',Int64,cb_mode) #사람 검출 여부 계속 서브 스크라이브 
        rospy.Subscriber('/move_base_simple/goal', PoseStamped,cb_goal ) # 목적지 정보 서브 스크라이브 
        rospy.Subscriber('/odom',Odometry,cb_odometry)

        pub_mode = rospy.Publisher('/navigation_status', Int64, queue_size=10) #토픽이름 부여, 자료형 
        pub_temp_odom = rospy.Publisher('/temp_odom', PoseStamped, queue_size=10) #토픽이름 부여, 자료형 

        mode = Int64()
        temp_odom = PoseStamped()

        
        print("[INFO] publish when robot reached ")

        while not rospy.is_shutdown():
            
            reached = is_it_reached()

             

            if (global_mode == 1) and (reached == True) : # 두 가지 조건 사람이 검출 되어야 하고 목적지에 도달한 상태 이어야 한다.
                rospy.Subscriber('/odom',Odometry,cb_temp_odometry)
                mode.data = 1 # 항상 1만 발행

                temp_odom.pose.position.x     =  global_temp_position_x               
                temp_odom.pose.position.y     =  global_temp_position_y               
                temp_odom.pose.orientation.x  =  global_temp_orientation_x            
                temp_odom.pose.orientation.y  =  global_temp_orientation_y            
                temp_odom.pose.orientation.z  =  global_temp_orientation_z            
                temp_odom.pose.orientation.w  =  global_temp_orientation_w       
            
                pub_mode.publish(mode) # 1이 들어 올 때만 box2coordinate 노드에서 무브 로봇 으로 퍼블리시
                pub_temp_odom.publish(temp_odom)
                print("navigation activated")
            else :
                mode.data = 0
                pub_mode.publish(mode)
                print("navigation deactivated")


            rate.sleep
            
            
       
    except rospy.ROSInterruptException:
        pass