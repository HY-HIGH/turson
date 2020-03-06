#!/usr/bin/env python
#-*- coding: utf-8 -*-

#-------------------import section-------------------
import copy 
import math         
import rospy

from std_msgs.msg import Int64                                              # 로봇의 모드 메세지 형식
from turson.msg  import Box_data                                            # 박스 데이터 커스텀 메시지
from nav_msgs.msg import Odometry                                           # 로봇의 현재위치 수신
from darknet_ros_msgs.msg import ObjectCount
from move_base_msgs.msg import MoveBaseActionResult                         # 로봇의 Navigation goal 도착여부 수신
from geometry_msgs.msg import Vector3,Quaternion,PoseStamped,Twist          # 로봇의 각종 움직임 제어,
from tf.transformations import quaternion_from_euler,euler_from_quaternion  # 로봇의 위치 및 방향 좌표변환
from text_color import color 
#----------------------------------------------------


#----------------------------------------------------
def current_pose_callback(real_pose):
    global current_pose
    current_pose = real_pose
def cb_result(result):
    global robot_status
    if result.status.status == 3:

        robot_status = True
    else :
        robot_status = False
def cb_bounding_box(image_data):
    global global_x_mid
    global global_box_size
    global robot_status
    global stop_signal
    global person_detect

    global_x_mid        =  image_data.x_mid
    global_box_size     =  image_data.box_size
    #print ('box_size :ospy.set_param('nav_once',0)5000 #1.5m

def box_count_callback(box_count):
    
    global global_box_count     
    global_box_count = box_count.count
    # print ("count :" + str(global_box_count))

def mode_converter():
    if global_box_count > 0: #사람이 검출
        print(' Person Detected | Size :{}'.format(global_box_size))
        if  global_box_size > enough_distance: # 사람이 가까이 있을 때 
            print(color.GREEN + "[Patrol Mode]"+'Too Close, Warning'+ color.END)
            
        elif global_box_size < too_far_distance:
            print(color.GREEN + "[Patrol Mode]"+'Too Far, Safe'+ color.END)
        
        elif (too_far_distance <= global_box_size <= enough_distance) : # 사람이 충분히 멀리 있고 
            print('Start Approach To Person')
            # 정지
            while True :
                if robot_status == True :
                    print(color.RED + "="*10 + color.END)
                    print(color.RED + "Robot stop!" + color.END)
                    print(color.RED + "="*10 + color.END)
                    break
                else : 
                    pub_stop_destination.publish(current_pose)
            
            rospy.set_param('mode',1)#네비게이션 모드
            print('Start Navigation Mode')
            while True:
                print(color.YELLOW + '[Navigation Mode]'+ color.END)
                if rospy.get_param('mode') == 0 :
                    break
                else: 
                    pass
        else:
            pass
    else :#사람이 검출되지 않음
        print(color.GREEN + '[Patrol Mode]'+ color.END)

# ---------------------------------------------------------------------------- #


#-------------------------Main------------------------
if __name__ == '__main__':
    try:
    #----Initialize node & Define publisher/subscriber---
        rospy.init_node('mode_controller', anonymous=False)

        rospy.Subscriber('/box_data',Box_data,cb_bounding_box)              # Person detection 데이터 수신
        rospy.Subscriber('/real_pose', PoseStamped, current_pose_callback)          # 로봇의 현재위치 확인
        rospy.Subscriber('/darknet_ros/found_object',ObjectCount,box_count_callback)    
        rospy.Subscriber('/move_base/result',MoveBaseActionResult,cb_result)    # 목적지 도착 여부 계속 서브스크라이브
        pub_stop_destination = rospy.Publisher('set_robot_destination', PoseStamped, queue_size=10)
    #--------------------Setup parameter-----------------
        rospy.set_param('mode',0)                                           # 로봇의 모드값 변환

    #-------------------Define variables-----------------
        global current_pose                                                 # 현재 robot의 위치
        global DISTANCE_MARGIN                                              # 정지를 위한 여유 거리
        global_box_count = 0
        global_x_mid = 0                                                    # Person detection box의 x 좌표의 중앙값
        person_detect = 0                                                   # Person detection 여부
        global_box_size = 0                                                 # Person detection box의 크기값
        RATE = rospy.Rate(10)                                                # while 반복 속도 제어, 1hz 
        DISTANCE_MARGIN = 0.1                                               # 로봇의 목표값과 센서값 오차범위
    #----------------Initiate main statement-------------
        while not rospy.is_shutdown():
            mode_converter()
            RATE.sleep()

    except rospy.ROSInterruptException:
        pass
