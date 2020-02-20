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
from geometry_msgs.msg import Vector3,Quaternion,PoseStamped,Twist
from tf.transformations import quaternion_from_euler,euler_from_quaternion 
from move_base_msgs.msg import MoveBaseActionResult
from turson.msg  import Box_data              # 박스 데이터 커스텀 메시지

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
# def status_callback(result):
#     global robot_status
    
#     if result.status.status == 3:
#         robot_status = True
#     else:
#         pass
def stop_callback(stop):
    global stop_signal

    if stop == 1:
        stop_signal = True
    else:
        pass

def cb_bounding_box(image_data):
    global global_x_mid
    global global_box_size
    global robot_status
    global stop_signal

    global_x_mid        =  image_data.x_mid
    global_box_size     =  image_data.box_size
    # print ('box_size :',global_box_size)
    # print ('center? :',global_x_mid)
    print('person detected')

    if global_box_size > 120000:
        print('over box_size')
        pass # 경고음

    else :
        if stop_signal == True:
            print('navigation mode')
            
            rospy.set_param('mode',2)

            detection_image_centralize()    

            rospy.set_param('mode',1)
            stop_signal = False
        else:
            pass





# def detection_image_centralize():
#     test_cnt = 0
#     while True:
#         global robot_status
#         print("Robot received stop signal!")
#         if robot_status == True: #로봇이 정지 신호를 받으면
#         # 돌아라
#             if  global_x_mid > 0.45 and global_x_mid < 0.55  :

#                 robot_status = False
#                 # 멈춰라
#                 break

#             print("Image centralizing...%d"%test_cnt)
#             print("param:",rospy.get_param('mode')); print('\n')

#             test_cnt = test_cnt + 1
#         pub_mode.publish(rospy.get_param('mode'))
#         rate.sleep()


def detection_image_centralize():
    
    rate_temp = rospy.Rate(10)
    while True:
        if global_x_mid < 0.45:
            angular_velocity = 1
    
        elif global_x_mid > 0.55:
            angular_velocity = -1
        
        else :
            angular_velocity = 0

        twist.angular.x = 0
        twist.angular.y = 0
        twist.angular.z = angular_velocity
        pub_twist.publish(twist)

        print("x_mid",global_x_mid)
        if global_x_mid > 0.45 and global_x_mid < 0.55 : #xmid 가 0.5 가되면 정지

            twist.angular.x = 0
            twist.angular.y = 0
            twist.angular.z = 0
            pub_twist.publish(twist)

            rospy.set_param('navigation_status',1)
            break
        rate_temp.sleep()
        print("Centralizing_Rotating...");print('\n')
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
        rospy.Subscriber('/stop_signal',Int64,stop_callback)

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
