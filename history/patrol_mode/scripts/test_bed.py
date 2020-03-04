#!/usr/bin/env python
#-*- coding: utf-8 -*-

#-------------------import section-------------------
# rospy:기본적인 출력을 위해 import
# String:기본적인 문자열 통신을 위해 import
# Mode control을 위해 노드간 통신용 msg type을 별도로 선언
import copy 
import math         
import rospy
from nav_msgs.msg import Odometry
from std_msgs.msg import String,Int64
from move_base_msgs.msg import MoveBaseActionResult
from geometry_msgs.msg import Vector3,Quaternion,PoseStamped,Twist
from tf.transformations import quaternion_from_euler,euler_from_quaternion 

#----------------------------------------------------


# ---------------------------------------------------------------------------- #
#                      Current position of Robot realtime update                  
# 
# 로봇의 현재좌표를 지속적으로 업데이트
#  - X-Y-Z 좌표 
#  - 로봇의 헤드 방향(Orientation)
# ---------------------------------------------------------------------------- #
def current_pose_callback(odom_data):
    global current_pose
    current_pose.pose = odom_data.pose.pose

# ---------------------------------------------------------------------------- #
#                     Current robot status realtime update                     #
# 로봇의 현재 네비게이션 상태를 지속적으로 업데이트
#  이동 중: status = 1
#  목표지점 도달: status = 3
# ---------------------------------------------------------------------------- #
def status_callback(result):
    global robot_status
    
    if result.status.status == 3:
        robot_status = True
    else:
        pass

def cb_bounding_box(image_data):
    global global_x_mid
    global global_box_size
    global robot_status

    global_x_mid        =  image_data.x_mid
    global_box_size     =  image_data.box_size
    # print ('box_size :',global_box_size)
    # print ('center? :',global_x_mid)

    if global_box_size > 120000:
        pass # 경고음
    else :
        if robot_status == True:
            rospy.set_param('mode',2)

            detection_image_centralize()    

            rospy.set_param('mode',1)
            robot_status = False
        else:
            pass

def detection_image_centralize():
    
    rate_temp = rospy.Rate(10)
    while True:
        if global_x_mid < 0.45:
            angular_velocity = 1
    
        elif global_x_mid > 0.55:
            angular_velocity = -1


        twist.angular.x = 0
        twist.angular.y = 0
        twist.angular.z = angular_velocity
        pub_twist.publish(twist)

        if global_x_mid > 0.45 and global_x_mid < 0.55 : #xmid 가 0.5 가되면 정지
            twist.angular.x = 0
            twist.angular.y = 0
            twist.angular.z = 0
            pub_twist.publish(twist)

            rospy.set_param('navigation_status',1)
            break
        rate_temp.sleep()
        print("Rotating...");print('\n')
    # while True:
    #     if test_cnt == 10:
    #         break
    #     print("Image centralizing...%d"%test_cnt)
    #     print("Current mode:", rospy.get_param('mode'))
    #     test_cnt = test_cnt + 1
    #     pub_mode.publish(rospy.get_param('mode'))
    #     rate.sleep()


#----------------------------------------------------
# mode라고 불리는 int64 메세지타입을 지속적으로 publish함으로써 mode제어를 하는 노드
# custom message로 msg파일을 별도로 만들었고 쓸 수도 있으나 mode_control 패키지를 이용하는 다른
# 패키지들의 의존성을 최대한 낮추고자 std_msgs/Int64 메세지 타입을 사용한다.
# 파라미터 설정을 통해서 외부에서 mode제어를 할 수 있게 설정.
# while문에서는 현재 파라미터값을 계속 읽어드림과 동시에 mode를 publish한다.
# mode가 0번: Patrol
# mode가 1번: Navigation
# mode가 0->1로 전환되는 경우에 mode 전환 이전에 robot정지 신호 publish
#----------------------------------------------------
def mode_controller():

    while not rospy.is_shutdown():
        global current_pose
        global past_get_param

        # if((past_get_param == 0) and (rospy.get_param('mode') == 1)):
        #     rospy.set_param('mode',2)
        #     detection_image_centralize()
        #     rospy.set_param('mode',1)

        # past_get_param = rospy.get_param('mode')
        # print("Current mode:", rospy.get_param('mode'))
        # pub_mode.publish(rospy.get_param('mode'))

        rate_main.sleep()

#-------------------------Main------------------------
if __name__ == '__main__':
    try:


    #----Initialize node & Define publisher/subscriber---
        rospy.init_node('mode_controller', anonymous=False)

        pub_twist = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        pub_mode = rospy.Publisher('mode_control', Int64, queue_size=10)   

        rospy.Subscriber('/odom', Odometry, current_pose_callback)
        rospy.Subscriber('/move_base/result',MoveBaseActionResult,status_callback)
        rospy.Subscriber('/box_data',Box_data,cb_bounding_box)

    #--------------------Setup parameter-----------------
        rospy.set_param('mode',0)
        
    #-------------------Define variables-----------------
        global twist
        global robot_status
        global current_pose                       # 현재 robot의 위치
        global distance_margin                    # 정지를 위한 여유 거리
        global past_get_param                     # 모드 전환마다 해야 할 일 분기를 위해 선언


        global_box_size = 0
        global_x_mid      = 0
        robot_status = False
        distance_margin = 0.1
        current_pose = PoseStamped()              # 현재 로봇의 위치 실시간 update
        twist =Twist()                            # 제자리 회전을 위해 선언
        rate = rospy.Rate(1) # 1hz                # while 반복 속도 제어
        rate_main = rospy.Rate(0.5) # 0.5hz       # while 반복 속도 제어
        past_get_param = rospy.get_param('mode')  # Set parameter 'mode'
    #----------------Initiate main statement-------------
        mode_controller()                         # main while 문 포함

    except rospy.ROSInterruptException:
        pass




























#!/usr/bin/env python
#-*- coding:utf-8 -*-
# import rospy 
# import math
# import time
# from std_msgs.msg import Int64
# from nav_msgs.msg import Odometry
# from move_base_msgs.msg import MoveBaseActionResult
# from actionlib_msgs.msg import GoalStatusArray
# from geometry_msgs.msg import PoseStamped,Twist,Quaternion,Vector3
# from tf.transformations import quaternion_from_euler,euler_from_quaternion  
# def mode_callback(mode):
# # ---------------------------------------------------------------------------- #
# #                      Mode realtime update
# #
# # 모드를 지속적으로 실시간으로 update하는 subscriber callback 함수
# # 모드를 다른 함수에서도 참조하기 위해 불가피하게 전역변수 선언
# # ---------------------------------------------------------------------------- #
#     global current_mode
#     current_mode = mode.data

# def current_pose_callback(odom_data):
# # ---------------------------------------------------------------------------- #
# #                      Current position of Robot realtime update                  
# # 
# # 로봇의 현재좌표를 지속적으로 업데이트
# #  - X-Y-Z 좌표 
# #  - 로봇의 헤드 방향(Orientation)
# # ---------------------------------------------------------------------------- #
#     global current_pose
#     current_pose.pose = odom_data.pose.pose

# # ---------------------------------------------------------------------------- #
# #                     Current robot status realtime update                     #
# # 로봇의 현재 네비게이션 상태를 지속적으로 업데이트
# #  이동 중: status = 1
# #  목표지점 도달: status = 3
# # ---------------------------------------------------------------------------- #
# def status_callback(result):
#     global robot_status
    
#     if result.status.status == 3:
#         robot_status = True
#         print("Result:{}".format(result.status.status))
#     else:
#         print("Result:{}".format(result.status.status))
#         print("Nothing")



# def Timer(second):
#     time_end = time.time() + second
#     twist.angular.x = 0
#     twist.angular.y = 0
#     while True:
#         twist.angular.z = 1.5
#         pub_twist.publish(twist)
#         if time.time() > time_end:
#             twist.angular.z = 0
#             pub_twist.publish(twist)
#             break

# def rotation():
#     # temp = time.time()
#     # Timer(10.5)
#     # print("Time elapsed: %lf" %(time.time()-temp))
#     # temp_time = time.time()
#     # Timer(2)
#     # twist.angular.z = 0
#     # pub_twist.publish(twist)
#     # print("Time elapsed: %lf"%(time.time()-temp_time))
#     # while True:
#     #     global current_pose
#     #     yaw = math.radians(270)
   
#     #     current_quaternion = [current_pose.pose.orientation.x,current_pose.pose.orientation.y,current_pose.pose.orientation.z,current_pose.pose.orientation.w]
        
#     #     euler = euler_from_quaternion(current_quaternion)
#     #     current_yaw = euler[2]+math.pi
#     #     if (abs((euler[2]+math.pi) - yaw)) < 0.2:
#     #         twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = 0.0
#     #         print("Stop! differnece:",abs(euler[2]+math.pi-yaw))
#     #         print("yaw",yaw,"current_yaw",euler[2]+math.pi)
#     #         pub_twist.publish(twist)
#     #         break
#     #     else: # 양수: 반시계방향 회전 | 음수: 시계방향 회전
#     #         twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = -0.8
#     #         print("rotating...differnece:",abs(euler[2]+math.pi-yaw))
#     #         print("yaw:",yaw,"current_yaw:",euler[2]+math.pi)
#     #         pub_twist.publish(twist)
#     #         print("="*15)

#     #     rate.sleep()
#     while True:
#         global robot_status
#         if robot_status == True:
#             print("Arrived!")
#             robot_status = False
#         rate.sleep()

# if __name__ == '__main__':
#     try:
#         rospy.init_node('TEST', anonymous=False)
#         rospy.Subscriber('mode_control',Int64, mode_callback) 
#         rospy.Subscriber('/odom', Odometry, current_pose_callback)
#         pub_twist = rospy.Publisher('cmd_vel', Twist, queue_size=10)
#         #rospy.Subscriber('/move_base/status',GoalStatusArray,status_callback)
#         rospy.Subscriber('/move_base/result',MoveBaseActionResult,status_callback)
#         global current_mode
#         global current_pose
#         global twist
#         global rate 
#         global robot_status
        

#         current_pose = PoseStamped()
#         twist = Twist()
        
#         target_angular_vel  = 0.0
#         control_angular_vel = 0.0
#         robot_status = False
#         rate = rospy.Rate(10)
#         rotation()
        
#     except rospy.ROSInterruptException:
#         pass

# # import random
# # import time
# # import copy


# # a = [1, 2, 3]

# # b = copy.copy(a)

# # print("ID-A:{0},ID-B:{1} ".format(id(a),id(b)))
# # print("A:",a,"B:",b)
# # print("="*20)
# # a[0]=7
# # print("A:",a,"B:",b)
# # print("ID-A:{0},ID-B:{1} ".format(id(a),id(b)))

# # print("="*20)
# # b = copy.copy(a)
# # print("A:",a,"B:",b)
# # print("ID-A:{0},ID-B:{1} ".format(id(a),id(b)))
# # print(dir(b))

# #print("A:{0},B:{1} ".format(a,b)

#     # k = random.uniform(-1, 1)
#     # print ("k is %lf"%k)
    
#     # time.sleep(1)

#         # global switch_patrol
#     # if (switch_patrol == 0):
#     #     yaw = math.radians(270)
#     # elif (switch_patrol == 1):
#     #     yaw = math.radians(360)
#     # elif (switch_patrol == 2):
#     #     yaw = math.radians(90)
#     # else :
#     #     yaw = math.radians(180)