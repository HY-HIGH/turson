#!/usr/bin/env python 
#-*- coding:utf-8 -*-
# 목표지점 받아와서 로봇 움직인다.
# 쉬뱅 인터 프리터 지시줄 //파이썬이다.


import rospy #파이썬 노드
from geometry_msgs.msg import PoseStamped
from move_base_msgs.msg import MoveBaseActionResult
global_result = False
              
goto_x        = 0                   
goto_y        = 0           
goto_z        = 0           
orientation_x = 0       
orientation_y = 0       
orientation_z = 0       
orientation_w = 0       
           


def cb_result(result):
    global global_result
    if result.status.status == 3:

        global_result = True
        print('navigation :',global_result)
    else :
        global_result = False
        
def cb_destination(data): # data 메시지 받아옴 (목적지 데이터) ,처리 메세지가 도착할때 마다 콜백 함수 호출

    global global_result
    global goto_x
    global goto_y
    global goto_z
    global orientation_x
    global orientation_y
    global orientation_z
    global orientation_w
    
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
    

def goto ():
    global global_result

    rospy.init_node('move_turson', anonymous=True)
    rospy.Subscriber('/move_base/result',MoveBaseActionResult,cb_result) #사람 검출 여부 계속 서브 스크라이브 
    rospy.Subscriber('/set_robot_destination',PoseStamped, cb_destination) #함수 호출
    pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=10)
    rate = rospy.Rate(1) # 발행 속도 10hz 
    
    while not rospy.is_shutdown():
        if global_result == True:
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
            global_result = False
            
        rate.sleep

if __name__ == '__main__':
    try:
        goto()
            
            
       
    except rospy.ROSInterruptException:
        pass