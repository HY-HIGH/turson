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
from geometry_msgs.msg import PoseStamped #메세지 패키지 속 메세지 모듈을 가져와서 그중 PoseStamped를 가져온다.


class Destination():

    
    def __init__(self): # 초기화
        float global_x_mid
        float global_y_mid
        float global_box_size
        float global_box_float
        float global_current_position_x  
        float global_current_position_y  
        float global_current_orientation_x  
        float global_current_orientation_y  
        float global_current_orientation_z  
        float global_current_orientation_w  



    def cb_bounding_boxes(self,image_data): #image_data 객체 리스트
        # 수정할 변수 
      

        # 이부분 수정 필요 

        # print ("I got image")
        
        # 1개의 박스만 받는다고 가정
        box_count = len(image_data.bounding_boxes)

        x_min = image_data.bounding_boxes[0].xmin
        x_max = image_data.bounding_boxes[0].xmax
        y_min = image_data.bounding_boxes[0].ymin
        y_max = image_data.bounding_boxes[0].ymax 
    
        float(x_min)# float 으로 변경
        float(x_max)
        float(y_min)
        float(y_max)
        
        # print ("x_min : ",x_min) #0
        # print ("x_max : ",x_max) #640
        # print ("y_min : ",y_min) #0
        # print ("y_min : ",y_max) #480
        # print ("box_count : ",box_count)
        frame_width = 640.0 #가로
        frame_height = 480.0 #세로 
        x_length = x_max - x_min
        y_length = y_max - y_min
    
        
        global_x_mid = ((x_max + x_min) / 2) / frame_width
        global_y_mid = ((y_max + y_min) / 2) / frame_height
        global_box_size = (x_length * y_length) / (frame_height * frame_width)

        print ("x_mid : ",global_x_mid) #0
        print ("y_mid : ",global_y_mid) #0
        print ("box_size : ",global_box_size)

        

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

    def current_radian(self): #현재 뱡향을 radian 값으로 리턴
        
        current_x = global_current_orientation_x 
        current_y = global_current_orientation_y
        current_z = global_current_orientation_z
        current_w = global_current_orientation_w
        current_orient = Vector3(*euler_from_quaternion([current_x,current_y,current_z,current_w]))
        # * : positional argument 만 받겟다 
        
        return current_orient # Vector3


    def calculate_coordinate(): #좌표값 계산
        global global_box_size
        pi = math.pi

        distance_factor = 2 # 박스 사이즈 값에 따른 거리 비율 # 수정 필요

        orient = current_radian() 
        angle = orient.z # yaw 값 그대로 들어감 
        distance_person = distance_factor * global_box_size

        cal_position_x = (global_current_position_x + (distance_person * math.cos(angle*pi)))
        cal_position_y = (global_current_position_y + (distance_person * math.sin(angle*pi))) 
        
        return cal_position_x,cal_position_y

        
    
    rospy.Subscriber('/darknet_ros/bounding_boxes',BoundingBoxes,cb_bounding_boxes)
    rospy.Subscriber('/odom',Odometry,cb_odometry)
    pub = rospy.Publisher('/set_robot_destination', PoseStamped, queue_size=10) #토픽이름 부여, 자료형 
    
    rospy.init_node('pub_box2coordinate', anonymous=True)# 노드 초기화 #노드이름
    
    ### 정해진 형식###
    rate = rospy.Rate(1) # 발행 속도 10hz 
    while not rospy.is_shutdown():
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
        rate.sleep()# 반복문을 위한 일시정지
        # print ('------------------------------')
        # print ('current_x : ' ,)
        # print ('current_y : ' ,global_current_y)
        # print ('current_w : ' ,global_current_w)
        print ('                              ')
        print('goto position x:',robot_destination.pose.position.x)
        print('goto position y:',robot_destination.pose.position.y)
        print('goto position z:',robot_destination.pose.position.z)
        # print('goto orientation x:',robot_destination.pose.orientation.x)
        # print('goto orientation y:',robot_destination.pose.orientation.y)
        # print('goto orientation z:',robot_destination.pose.orientation.z)
        # print('goto orientation w:',robot_destination.pose.orientation.w)
        # print ('------------------------------')
            
# 함수 시작부분

if __name__ == '__main__':
    try:
       
        Destination()
       
    except rospy.ROSInterruptException:
        pass