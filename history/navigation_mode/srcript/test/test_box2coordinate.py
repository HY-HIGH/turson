#!/usr/bin/env python
#-*- coding:utf-8 -*-

# 1. 이미지 정보 sub /darknet_ros/bounding_boxes
# 2. odom 정보 sub
# 3. mode 정보 sub

# 위치 좌표 및 오리엔테이션 퍼블리시 
import math
from tf.transformations import quaternion_from_euler
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Vector3 # 벡터 (x,y,z)
from geometry_msgs.msg import Quaternion #쿼터니언(x,y,z,w)
from geometry_msgs.msg import PoseStamped #메세지 패키지 속 메세지 모듈을 가져와서 그중 PoseStamped를 가져온다.
from darknet_ros_msgs.msg import BoundingBoxes #  이미지 정보 메세지 타입
import rospy #로스 파이 패키지
from random import *
from nav_msgs.msg import Odometry # 오도메트리 서브스크라이브
from turson_navigation.msg import Box_data #커스텀 메시지
from std_msgs.msg import Int64
from move_base_msgs.msg import MoveBaseActionResult

# 전역 변수 설정 
global_navigation_status        = 1
global_box_size                 = 0 
global_box_count                = 0  
global_current_position_x       = 0   
global_current_position_y       = 0     
global_current_orientation_x    = 0  
global_current_orientation_y    = 0  
global_current_orientation_z    = 0  
global_current_orientation_w    = 0
global_result                   = False




def cb_bounding_box(image_data): #image_data 객체 리스트

    # 수정할 변수 
    global global_box_size  
    global_box_size    = image_data.box_size     
    

def cb_odometry(odom_data): # 현재 위치를 current_ 로 정의 후 global에 저장
    # 수정할 변수
    #글로벌로 쓰지 않으려면 퍼블리시 하는 함수로 짜야한다.
    global global_current_position_x  
    global global_current_position_y  
    global global_current_orientation_x  
    global global_current_orientation_y  
    global global_current_orientation_z  
    global global_current_orientation_w  

    global_current_position_x       =  odom_data.pose.position.x
    global_current_position_y       =  odom_data.pose.position.y
    global_current_orientation_x    =  odom_data.pose.orientation.x 
    global_current_orientation_y    =  odom_data.pose.orientation.y 
    global_current_orientation_z    =  odom_data.pose.orientation.z 
    global_current_orientation_w    =  odom_data.pose.orientation.w 

def current_radian(): #현재 뱡향을 radian 값으로 리턴

    current_x = global_current_orientation_x
    current_y = global_current_orientation_y
    current_z = global_current_orientation_z
    current_w = global_current_orientation_w
    current_orient = Vector3(*euler_from_quaternion([current_x,current_y,current_z,current_w]))
    # * : positional argument 만 받겟다 
    
    return current_orient # Vector3


def calculate_coordinate(): #좌표값 계산
    global global_box_size
    global_box_size = 20000
    pi = math.pi

    distance_factor = 0.00001 # 박스 사이즈 값에 따른 거리 비율 # 수정 필요 .작을 수록 가까이 가야한다.

    orient = current_radian() 
    angle_radian = orient.z # yaw 값 그대로 들어감 
    angle_60 = math.degrees(angle_radian)
    print ("angle_radian : ",angle_radian)
    print ("angle_60     : ",angle_60)

    distance_person = distance_factor * global_box_size

    cal_position_x = (global_current_position_x + (distance_person * math.cos(angle_60)))

    cal_position_y = (global_current_position_y + (distance_person * math.sin(angle_60))) 
    
    return cal_position_x,cal_position_y

def cb_navigation_status(status):
    global global_navigation_status
    global_navigation_status = status.data 


def cb_result(result):
    global global_result
    if result.status.status == 3:

        global_result = True
        print('navigation :',global_result)
    else :
        global_result = False
    

    
def destination(): #메인 함수
    global global_result
    
    rospy.Subscriber('/navigation_status',Int64,cb_navigation_status) # 항상 
    rospy.Subscriber('/move_base/result',MoveBaseActionResult,cb_result) #사람 검출 여부 계속 서브 스크라이브 

    pub = rospy.Publisher('/set_robot_destination', PoseStamped, queue_size=10) #토픽이름 부여, 자료형 
    
    rospy.init_node('box2coordinate', anonymous=True)# 노드 초기화 #노드이름

    ### 정해진 형식###
    rate = rospy.Rate(1) # 발행 속도 10hz 
    while not rospy.is_shutdown():
        if global_result == True :

            rospy.Subscriber('/box_data',Box_data,cb_bounding_box)
            rospy.Subscriber('/temp_odom',PoseStamped,cb_odometry)

            robot_destination = PoseStamped()  #객체 선언 
            cal_x,cal_y = calculate_coordinate() 
            robot_destination.pose.position.x = cal_x
            robot_destination.pose.position.y = cal_y
            robot_destination.pose.position.z = 0.0
            robot_destination.pose.orientation.x = global_current_orientation_x  
            robot_destination.pose.orientation.y = global_current_orientation_y  
            robot_destination.pose.orientation.z = global_current_orientation_z  
            robot_destination.pose.orientation.w = global_current_orientation_w  

        
            pub.publish(robot_destination)#퍼블리시 할 항목
            global_result = False
        rate.sleep()# 반복문을 위한 일시정지
        # print ('                              ')
        # print('goto position x:',robot_destination.pose.position.x)
        # print('goto position y:',robot_destination.pose.position.y)
        # print('goto position z:',robot_destination.pose.position.z)
        # print ('------------------------------')
        # print ('current_x : ' ,)
        # print ('current_y : ' ,global_current_y)
        # print ('current_w : ' ,global_current_w)
        
     
        # print('goto orientation x:',robot_destination.pose.orientation.x)
        # print('goto orientation y:',robot_destination.pose.orientation.y)
        # print('goto orientation z:',robot_destination.pose.orientation.z)
        # print('goto orientation w:',robot_destination.pose.orientation.w)
        # print ('------------------------------')
        
# 함수 시작부분

if __name__ == '__main__':
    try:
       
        destination()
       
    except rospy.ROSInterruptException:
        pass