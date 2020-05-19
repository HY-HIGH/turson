#!/usr/bin/env python
#-*- coding:utf-8 -*-
#==================== 의존성 패키지 및 메시지 ==================== 
# 패키지
import sys
import math                                              #삼각함수 등 
import rospy                                             #로스 파이 패키지
from random import *
from tf.transformations import quaternion_from_euler     #오일러-쿼터니안 변환
from tf.transformations import euler_from_quaternion     #쿼터니안-오일러 변환
import time
# 메시지
from darknet_ros_msgs.msg   import ObjectCount
from darknet_ros_msgs.msg   import BoundingBoxes         # 이미지 정보 메세지 타입
from geometry_msgs.msg      import Vector3               # 벡터 (x,y,z)
from geometry_msgs.msg      import Quaternion            # 쿼터니언(x,y,z,w)
from geometry_msgs.msg      import PoseStamped           # 메세지 패키지 속 메세지 모듈을 가져와서 그중 PoseStamped를 가져온다.
from nav_msgs.msg           import Odometry              # 오도메트리 메시지
from turson.msg             import Box_data              # 박스 데이터 커스텀 메시지
from std_msgs.msg           import Int64                 # 모드 관련 메시지
from move_base_msgs.msg     import MoveBaseActionResult  # result 메시지
from geometry_msgs.msg      import Twist          # 로봇의 각종 움직임 제어,
from text_color import color 
#==================== 전역 변수 설정 ==================== 
MAX_LIST_COUNT = 30
COUNT_THREASH_HOLD = 0.2
# 모드 관련
global_mode                     = 0 
global_result                   = False # 도착 여부
average_box_count = 0
global_box_count = 0
temp_count_list = [] #글로벌로 선언 
# 박스 정보
global_x_mid                    = 0
global_box_size                 = 0 
global_box_count                = 0  
global_no_person                = False
# real pose
current_pose                    = 0
#==================== callback 함수 (업데이트) ==================== 
def cb_real_pose(real_pose):
    global current_pose
    current_pose = real_pose
   


def cb_box_count(box_count) :
    global global_box_count
    # global average_box_count

    # Box Count
    if box_count.count > 0:
        bool_person = (box_count.count / box_count.count)## 존재 0 or 1
    else :
        bool_person = 0
    temp_count_list.append(bool_person)

    if len(temp_count_list) > MAX_LIST_COUNT:
        temp_count_list.pop(0)
        # print("list count    : ",len(temp_count_list))
        # print("last 10 index : ",temp_count_list[20:29])
    #float (average_list)
    sum_list=float(sum(temp_count_list))
    list_length= float (len(temp_count_list))
    average_list = float(sum_list/list_length)
    # print ("average          : ",average_list)
    if average_list > COUNT_THREASH_HOLD:
        average_box_count = 1
    elif average_list <= COUNT_THREASH_HOLD:
        average_box_count = 0
    
    global_box_count = average_box_count
    # print ("is there person? : ",average_box_count)
    
    # print ("box_count : ",average_box_count)
    # print ("______________________________________")
    
# 바운딩 박스 업데이트   
def cb_bounding_box(image_data): #image_data 객체 리스트

    # 수정할 변수 
    global global_box_size  
    global global_x_mid
    
    global_box_size    = image_data.box_size
    global_x_mid       = image_data.x_mid
    
    #print ('box_size :',global_box_size)

    


# 결과 업데이트 (도착시 메인 모드 0으로 바꾸어 준다)
def cb_result(result):
    global global_result
    if result.status.status == 3:

        global_result = True
    else :
        global_result = False

#==================== 커스텀 함수 ====================

# 시간 홀드 함수
def waiting_timer(second):
    time_end = time.time() + second
    print (color.YELLOW +"[Navigation] : waiting %d second"%(second) + color.END)
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
    
    #print ("[Navigation]radians angle         : ",angle_radian)
    print ( color.YELLOW +"[Navigation] : Calculation Finished : " +color.END)

    print ( color.YELLOW +"[Navigation] : Calculated Angle :{} ".format(transformed_angle) +color.END)


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
    print ( color.YELLOW +"[Navigation] : Calculated Destination : ({},{}) ".format(cal_position_x,cal_position_y) +color.END)
    
    return cal_position_x,cal_position_y    

def box_size_2_distance(): # 박스크기가 5000 이하나 75000이상이면 패스 
    print ( color.YELLOW +'[Navigation] : Box Size : {}'.format(global_box_size) + color.END)
   
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
        #print("----------------------")
        print(color.YELLOW +"[Navigation] : Now Robot Calculate The Destination "+color.END) 
        distance_person = 1.0
        return distance_person
    else :
        print(color.YELLOW +"[Navigation] : No Need To Calculate"+color.END)
        return 0 

        #color.YELLOW + +color.END

# mode 가 1이 되면 시작
# 메인 함수    ## 대대적인 수정
def navigation(): 
    global global_result
    global global_navigation_status
    global global_mode
    global global_no_person
    twist = Twist()

    #rospy.set_param('mode',0) #테스트 용


    rospy.init_node('navigation', anonymous=False)                                           # 노드 초기화 #노드이름

    pub_destination = rospy.Publisher('/set_robot_destination', PoseStamped, queue_size = 10) #로봇의 목적지 퍼블리시
    pub_twist = rospy.Publisher('cmd_vel', Twist, queue_size=10)        # 로봇의 움직임 제어
    
    rospy.Subscriber('/move_base/result',MoveBaseActionResult,cb_result)    # 목적지 도착 여부 계속 서브스크라이브
    rospy.Subscriber('/box_data',Box_data,cb_bounding_box)
    rospy.Subscriber('/real_pose',PoseStamped,cb_real_pose)
    rospy.Subscriber('/darknet_ros/found_object',ObjectCount,cb_box_count)           

    message_rate = rospy.Rate(1)
    rate = rospy.Rate(10) # 발행 속도 10hz 
    while not rospy.is_shutdown(): #네비게이션 노드 유지
        
        global_mode = rospy.get_param('mode') # 모드를 받아오면 시작

        if global_mode == 1:
            global_no_person = False #사람 있음
            print("[INFO]: Navigation Mode Activate ")
            rospy.set_param('person_detected',1)
            rospy.set_param('person_warning',0)
            rospy.set_param('person_cleared',0)


            while True: # 센트럴 라이징 시작 (중심에 올때까지 계속)
                centralize_rate = rospy.Rate(10)
                global global_x_mid
                if global_box_count > 0 :  #사람이 있으면
                    if global_x_mid <= 0.48:
                        angular_velocity = 0.07
                    elif global_x_mid >= 0.52:
                        angular_velocity = -0.07
                    else :
                        angular_velocity = 0
                    
                    twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = angular_velocity
                    pub_twist.publish(twist)
                    print(color.YELLOW + "[Navigation] : Centralizing...Before Navigation"+color.END)
                    print(color.YELLOW + "[Navigation] : x_mid :{}".format(global_x_mid)+color.END)
            
                    if 0.48 < global_x_mid < 0.52 : # xmid 가 0.5 근처가 되면 정지
                        twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
                        pub_twist.publish(twist)
                        print(color.YELLOW + "[Navigation] : Centrallizing Finished"+color.END)
                        break
                 
                else: # 사람이 없으면 
                    while True:
                        if global_no_person == True: #아직 break 안함 global_no_person F
                            break # 223 줄
                        
                        second = 10 # x 초 주변 스캔                
                        time_final = time.time() + second
                        print (color.YELLOW + "[Navigation] : Lost Person, Now Searching While %d Seconds"%(second)+color.END)

                        if global_box_count > 0: 
                            break # 223 줄 break

                        while True:
                            if global_x_mid <= 0.48:
                                angular_velocity = 0.07

                            elif global_x_mid >= 0.52:
                                angular_velocity = -0.07

                            else :
                                angular_velocity = 0
                            twist.angular.x = 0;twist.angular.y = 0;twist.angular.z = angular_velocity
                           
                            pub_twist.publish(twist)
                            
                            if (global_box_count > 0) :# 시간 상관 없이 돌다가 사람이 검출되면 

                                break #234
                            if (time.time() > time_final)and(global_box_count == 0): # 10초 
                                global_no_person = True
                                break  #234
                if (global_no_person == True):
                    break#202
                centralize_rate.sleep()
            if global_no_person == True : 
                rospy.set_param('mode',0) #센트럴 모드 진입 후  10초 후에도 사람이 없으면 패트롤 모드 강제 전환 
                continue
#----------------------------------------------------------------------------------------------------
            print(color.YELLOW + "[Navigation] : Start Navigation"+color.END)
            
            robot_destination = PoseStamped()  # 객체 선언 
            cal_x,cal_y = calculate_coordinate() 
            robot_destination.pose.position.x = cal_x
            robot_destination.pose.position.y = cal_y
            robot_destination.pose.position.z = 0.0
            robot_destination.pose.orientation.x = current_pose.pose.orientation.x 
            robot_destination.pose.orientation.y = current_pose.pose.orientation.y 
            robot_destination.pose.orientation.z = current_pose.pose.orientation.z 
            robot_destination.pose.orientation.w = current_pose.pose.orientation.w 
            
            pub_destination.publish(robot_destination)      # 퍼블리시 할 항목
            global_result = False    
            while True:
                
                if global_result == True: # 도착하면
                    rospy.set_param('person_detected',1)
                    rospy.set_param('person_warning',1)
                    rospy.set_param('person_cleared',0)
                    
                    print (color.YELLOW + "[Navigation] : Goal Reached , Now Wait"+color.END)
                
                    # if global_box_count > 0  : #사람이 있다
                    while True:
                        print (color.YELLOW + "[Navigation] : Waiting...Until Clear|size:{}".format(global_box_size)+color.END)
                        if (global_box_size < 25000) and (global_box_count > 0):
                            print(color.YELLOW + "[Navigation] : Person Clear"+color.END)
                            print(color.YELLOW + "[Navigation] : Patrol Mode Start"+color.END)
                            rospy.set_param('person_detected',0)
                            rospy.set_param('person_warning',0)
                            rospy.set_param('person_cleared',1)
                            break
                        elif (global_box_count == 0) :
                            print(color.GREEN + "[INFO] : Patrol Mode Start After 5 second "+color.END)
                            waiting_timer(5) 
                            print(color.GREEN + "[INFO] : Patrol Mode Start"+color.END)
                            rospy.set_param('person_detected',0)
                            rospy.set_param('person_warning',0)
                            rospy.set_param('person_cleared',1)
                            break 
                        else:
                            pass    
                        message_rate.sleep()
                    # elif global_box_count == 0 : # 사람이 없다
                    #     print(color.GREEN +"[INFO] : Patrol Mode Start After 5 second " +color.END)
                    #     waiting_timer(5)  
                    #     print(color.GREEN +"[INFO] : Patrol Mode Start" +color.END)

                    rospy.set_param('mode',0) #파라미터 변경
                    global_result = False
                    # 패트롤 모드로 진입 -> 박스크기가 일정이상이면 그대로 패트롤

                    # 여기에서 파라미터를 바꾸어 줄것인지?

                    break
                else :
                    print (color.YELLOW + "[Navigation] : Going To Destination"+color.END)
                rate.sleep()

        elif global_mode == 0:
            print(color.GREEN + "[INFO]: Patrol Mode "+color.END)
            rospy.set_param('person_detected',0)
            rospy.set_param('person_warning',0)
            rospy.set_param('person_cleared',0)
           
        else:
            print(color.RED + "[INFO]: ERROR"+color.END)



        rate.sleep()    # 반복문을 위한 일시정지
       
        
# 함수 시작부분

if __name__ == '__main__':
    try:
        confirm = raw_input(color.RED+" 네비게이션 모드를 실행 하시겠습니까?.(y/n)"+ color.END)
        if confirm == 'y':
            print(color.YELLOW + "입력이 확인되었습니다. 네비게이션 모드를 실행합니다." + color.END)
            navigation()
        else:
            print(color.RED +"입력 확인이 올바르지 않습니다. 프로그램을 종료합니다." + color.END)
            sys.exit()
       
    except rospy.ROSInterruptException:
        pass