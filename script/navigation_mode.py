#!/usr/bin/env python
#-*- coding:utf-8 -*-
#==================== 의존성 패키지 및 메시지 ==================== 
# 패키지
import math                                              #삼각함수 등 
import rospy                                             #로스 파이 패키지
from random import *
from tf.transformations import quaternion_from_euler     #오일러-쿼터니안 변환
from tf.transformations import euler_from_quaternion     #쿼터니안-오일러 변환
import time
# 메시지
from darknet_ros_msgs.msg   import BoundingBoxes         # 이미지 정보 메세지 타입
from geometry_msgs.msg      import Vector3               # 벡터 (x,y,z)
from geometry_msgs.msg      import Quaternion            # 쿼터니언(x,y,z,w)
from geometry_msgs.msg      import PoseStamped           # 메세지 패키지 속 메세지 모듈을 가져와서 그중 PoseStamped를 가져온다.
from nav_msgs.msg           import Odometry              # 오도메트리 메시지
from turson.msg  import Box_data              # 박스 데이터 커스텀 메시지
from std_msgs.msg           import Int64                 # 모드 관련 메시지
from move_base_msgs.msg     import MoveBaseActionResult  # result 메시지

#==================== 전역 변수 설정 ==================== 
# 모드 관련
global_mode                     = 0 
global_result                   = False # 도착 여부
global_navigation_status        = 0 # 0: deactivated 1: activated

# 순간 오도메트리 
# global_temp_position_x          = 0     
# global_temp_position_y          = 0         
# global_temp_orientation_x       = 0
# global_temp_orientation_y       = 0
# global_temp_orientation_z       = 0
# global_temp_orientation_w       = 0

# 박스 정보
global_x_mid                    = 0
global_box_size                 = 0 
global_box_count                = 0  
person_detected                 = 0
# 현재 오도메트리
# global_current_position_x       = 0   
# global_current_position_y       = 0     
# global_current_orientation_x    = 0  
# global_current_orientation_y    = 0  
# global_current_orientation_z    = 0  
# global_current_orientation_w    = 0

current_pose                    = 0
#==================== callback 함수 (업데이트) ==================== 
def cb_real_pose(real_pose):
    global current_pose
    current_pose = real_pose
# 현재 메인 모드 업데이트 ([모드 컨트롤 노드] 모드)       
def cb_mode(mode):                        
    global global_mode
    global_mode = mode.data
    print ('mode : ',global_mode)

# 순간 오도메트리 업데이트 # Odometry msg
# def cb_temp_odometry(temp_odom_data):      

#     global global_temp_position_x  
#     global global_temp_position_y 
#     global global_temp_orientation_x  
#     global global_temp_orientation_y  
#     global global_temp_orientation_z  
#     global global_temp_orientation_w  

#     global_temp_position_x       = temp_odom_data.pose.pose.position.x
#     global_temp_position_y       = temp_odom_data.pose.pose.position.y 
#     global_temp_orientation_x    = temp_odom_data.pose.pose.orientation.x 
#     global_temp_orientation_y    = temp_odom_data.pose.pose.orientation.y 
#     global_temp_orientation_z    = temp_odom_data.pose.pose.orientation.z 
#     global_temp_orientation_w    = temp_odom_data.pose.pose.orientation.w 

# 바운딩 박스 업데이트   
def cb_bounding_box(image_data): #image_data 객체 리스트

    # 수정할 변수 
    global global_box_size  
    global global_x_mid
    
    global_box_size    = image_data.box_size
    global_x_mid       = image_data.x_mid
    
    #print ('box_size :',global_box_size)

    
#현재 오도메트리 정보 업데이트 [불필요]
# def cb_odometry(odom_data): # 현재 위치를 current_ 로 정의 후 global에 저장
#     # 수정할 변수
#     #글로벌로 쓰지 않으려면 퍼블리시 하는 함수로 짜야한다.
#     global global_current_position_x  
#     global global_current_position_y  
#     global global_current_orientation_x  
#     global global_current_orientation_y  
#     global global_current_orientation_z  
#     global global_current_orientation_w  

#     global_current_position_x       =  odom_data.pose.pose.position.x
#     global_current_position_y       =  odom_data.pose.pose.position.y
#     global_current_orientation_x    =  odom_data.pose.pose.orientation.x 
#     global_current_orientation_y    =  odom_data.pose.pose.orientation.y 
#     global_current_orientation_z    =  odom_data.pose.pose.orientation.z 
#     global_current_orientation_w    =  odom_data.pose.pose.orientation.w 

# 네비게이션 상태 업데이트[불필요]  파라미터로 대체
# def cb_navigation_status(status):
#     global global_navigation_status
#     global_navigation_status = status.data 

# 결과 업데이트 (도착시 메인 모드 0으로 바꾸어 준다)
def cb_result(result):
    global global_result
    if result.status.status == 3:

        global_result = True
    else :
        global_result = False

#==================== 커스텀 함수 ====================
# 로봇 초기화 함수 [코딩 중...][필요없음]
# def initialize():
#     pub_initialize = rospy.Publisher('/set_robot_destination', PoseStamped, queue_size = 10) #로봇의 목적지 퍼블리시

#     robot_initialize = PoseStamped()  # 객체 선언 
#     robot_initialize.pose.position.x = global_current_position_x
#     robot_initialize.pose.position.y = global_current_position_y
#     robot_initialize.pose.position.z = 0.0
#     robot_initialize.pose.orientation.x = global_current_orientation_x  
#     robot_initialize.pose.orientation.y = global_current_orientation_y  
#     robot_initialize.pose.orientation.z = global_current_orientation_z  
#     robot_initialize.pose.orientation.w = global_current_orientation_w  
                
#     pub_initialize.publish(robot_initialize)      # 퍼블리시 할 항목
def waiting_timer(second):
    time_end = time.time() + second
    print ("waiting %d second"%(second))
    while True:
        if time.time() > time_end:
            break
# 로봇의 로컬 좌표를 글로벌 좌표계에서 쓸수있도록 변환
def angle_transform():
    orient = current_radian() 
    angle_radian = orient.z               # yaw 값 그대로 들어감 #라디안 이용 해서 계산 할것
    angle_60 = math.degrees(angle_radian) #라디안에서 60도 각으로 변환
    if angle_60 < 0:
        transformed_angle = angle_60 + 360
    else :
        transformed_angle = angle_60
    
    print ("radians angle         : ",angle_radian)

    print ("transformed angle     : ",transformed_angle)


    return angle_radian


# 현재 로봇의 방향을 쿼터니안에서 라디안 (오일러)값으로 리턴[return current_orient]
def current_radian():
    current_x = current_pose.pose.orientation.x
    current_y = current_pose.pose.orientation.y
    current_z = current_pose.pose.orientation.z
    current_w = current_pose.pose.orientation.w
    current_orient = Vector3(*euler_from_quaternion([current_x,current_y,current_z,current_w]))# * : positional argument 만 받겟다 
    return current_orient # Vector3

# 로봇이 가고자 하는 좌표값 계산 [return cal_position_x,cal_position_y]
def calculate_coordinate(): 
    distance_person = box_size_2_distance()


    transformed_angle = angle_transform() # 글로벌 좌표계에 맞는 좌표로 변환 # 라디안 값으로 변환 

    cal_position_x = (current_pose.pose.position.x  + (distance_person * math.cos(transformed_angle)))
    cal_position_y = (current_pose.pose.position.y  + (distance_person * math.sin(transformed_angle)))
    
    return cal_position_x,cal_position_y    

def box_size_2_distance(): # 박스크기가 5000 이하나 75000이상이면 패스 
    print ('box_size :',global_box_size)
   
    # if 5000 <= global_box_size < 6500 : 
    #     distance_person = 5.5
    # elif 6500 <= global_box_size < 7500 : 
    #     distance_person = 5.0
    # elif 7500 <= global_box_size < 10500 : 
    #     distance_person = 4.5
    # elif 10500 <= global_box_size < 13000 : 
    #     distance_person = 4.0
    # elif 13000 <= global_box_size < 21000 : 
    #     distance_person = 3.5
    # elif 21000 <= global_box_size < 25000 : 
    #     distance_person = 3.0    
    # elif 25000 <= global_box_size < 33000 : 
    #     distance_person = 2.5
    # elif 33000 <= global_box_size < 45000 : 
    #     distance_person = 2.0
    # elif 45000 <= global_box_size < 75000 : 
    #     distance_person = 1.5
    # else :
    #     pass
    if 25000 <= global_box_size < 75000 :
        print("----------------------")
        print("now robot go to person") 
        distance_person = 1.0
        return distance_person
    else :
        print("no need to navigation")
        return 0 



# 정지 함수
def stop_robot():
    print('stop_robot')

# 메인 함수    
def navigation(): 
    global global_result
    global global_navigation_status
    global global_mode
    rospy.init_node('navigation', anonymous=False)                                           # 노드 초기화 #노드이름
    
    pub_destination = rospy.Publisher('/set_robot_destination', PoseStamped, queue_size = 10) #로봇의 목적지 퍼블리시
    #pub_temp_odom = rospy.Publisher('/temp_odom', PoseStamped, queue_size = 10)               #그 순간의 오도메트리 발행
    # rospy.Subscriber('/odom',Odometry,cb_odometry)
    rospy.Subscriber('mode_control',Int64,cb_mode)                          # 메인 노드 : 사람 검출 여부 계속 서브 스크라이브 
    rospy.Subscriber('/move_base/result',MoveBaseActionResult,cb_result)    # 목적지 도착 여부 계속 서브스크라이브
    rospy.Subscriber('/box_data',Box_data,cb_bounding_box)
    # rospy.Subscriber('/odom',Odometry,cb_temp_odometry)
    rospy.Subscriber('/real_pose',PoseStamped,cb_real_pose)

    rospy.set_param('navigation_status',0) #파라미터 변경



    mode = Int64()
    temp_odom = PoseStamped()
   

    rate = rospy.Rate(10) # 발행 속도 10hz 
    while not rospy.is_shutdown():
        global_navigation_status = rospy.get_param('navigation_status')
        if global_navigation_status == 1 :# 사람이 검출되면
            print("[INFO]: Navigation Activate ")
            global_mode = rospy.get_param('mode')
            if global_mode == 1:# 센트럴 라이징 완료 후
                print("[INFO]: Centrallizing Finished")
                nav_once =  rospy.get_param('nav_once')
                if nav_once == 1: # 한번만 
                #initialize()  필요 없음
                    print("[INFO]: Navigation Start  ")
                    

                    robot_destination = PoseStamped()  # 객체 선언 
                    cal_x,cal_y = calculate_coordinate() 
                    robot_destination.pose.position.x = cal_x
                    robot_destination.pose.position.y = cal_y
                    robot_destination.pose.position.z = 0.0
                    robot_destination.pose.orientation.x = current_pose.pose.orientation.x 
                    robot_destination.pose.orientation.y = current_pose.pose.orientation.y 
                    robot_destination.pose.orientation.z = current_pose.pose.orientation.z 
                    robot_destination.pose.orientation.w = current_pose.pose.orientation.w 
                    global_result = False
                    pub_destination.publish(robot_destination)      # 퍼블리시 할 항목
                    rospy.set_param('nav_once',0)
                else :
                    global_result = False
                    

                while True:
                    
                    if global_result == True: # 도착하면
                        print ("[Navigation] : goal reached , now wait")
                        
                        #정지 코드 [필요없을듯]
                        #rospy.set_param('person_detect',0)
                        past_time = time.time()
                        if global_box_size > 0  : #사람이 있다
                            while True:
                                print ("[Navigation] : Waiting...Until Clear|size:{}".format(global_box_size))
                                if global_box_size < 25000:
                                    print("[Navigation] : Person clear")
                                    break
                                else:
                                    pass
                        else : # 사람이 업ㅅ다
                            print("[Navigation] : No Person ")
                            waiting_timer(3)
                            

                        global_result = False
                        rospy.set_param('navigation_status',0) #파라미터 변경
                        rospy.set_param('nav_once',1)#네비게이션 한번만 모드  
                        print("[Navigation] : Navigation Finished")
                        rospy.set_param('mode',0) #파라미터 변경
                        # 패트롤 모드로 진입 -> 박스크기가 일정이상이면 그대로 패트롤

                        # 여기에서 파라미터를 바꾸어 줄것인지?

                        break


            elif global_mode == 0:
                print("[INFO]: Patrol Mode ")
            elif global_mode == 2:
                print("[INFO]: Centralize Mode ")
            else:
                print("[INFO]: WTF")

                

        elif global_navigation_status == 0 :
            print("[INFO]: Navigation Deactivated ")


        rate.sleep()    # 반복문을 위한 일시정지
       
        
# 함수 시작부분

if __name__ == '__main__':
    try:
       
        navigation()
       
    except rospy.ROSInterruptException:
        pass