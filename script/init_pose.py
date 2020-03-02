#!/usr/bin/env python 
#-*- coding:utf-8 -*-


import rospy
from nav_msgs.msg import Odometry
from tf.transformations import quaternion_from_euler
from geometry_msgs.msg import PoseWithCovarianceStamped,PoseStamped


def current_pose_callback(odom_data):
# ---------------------------------------------------------------------------- #
#                      Current position of Robot realtime update                  
# 
# 로봇의 현재좌표를 지속적으로 업데이트
#  - X-Y-Z 좌표 
#  - 로봇의 헤드 방향(Orientation)
# ---------------------------------------------------------------------------- #
    global current_pose

    current_pose.pose.pose.position.x = odom_data.pose.pose.position.x
    current_pose.pose.pose.position.y = odom_data.pose.pose.position.y
    
    
    current_pose.pose.pose.orientation.x = odom_data.pose.pose.orientation.x
    current_pose.pose.pose.orientation.y = odom_data.pose.pose.orientation.y
    current_pose.pose.pose.orientation.z = odom_data.pose.pose.orientation.z
    current_pose.pose.pose.orientation.w = odom_data.pose.pose.orientation.w
    
def is_same_postion(initial_position,current_position):
# ---------------------------------------------------------------------------- #
#                   Compare current position and set position                  #
# 현재위치와 초기화 위치를 지속적으로 비교하면서 허용오차 범위에 들어올 때 True를 반환
# 그렇지 않으면 False 반환
# ---------------------------------------------------------------------------- #

    if(abs(initial_position.pose.pose.position.x - current_position.pose.pose.position.x) < margin and \
        abs(initial_position.pose.pose.position.y - current_position.pose.pose.position.y) < margin and \
            abs(initial_position.pose.pose.orientation.x - current_pose.pose.pose.orientation.x) < margin and \
                abs(initial_position.pose.pose.orientation.y - current_pose.pose.pose.orientation.y) < margin and \
                    abs(initial_position.pose.pose.orientation.z - current_pose.pose.pose.orientation.z) < margin and \
                        abs(initial_position.pose.pose.orientation.w - current_pose.pose.pose.orientation.w) < margin ):
        return True
    else:
        return False

# ---------------------------------------------------------------------------- #
#                           Setup Node and variables                           #
# ---------------------------------------------------------------------------- #
rospy.init_node('Initial_pose', anonymous=False)

rospy.Subscriber('/odom', Odometry, current_pose_callback)
pub = rospy.Publisher('/initialpose', PoseWithCovarianceStamped, queue_size = 10)


rate = rospy.Rate(1)
current_pose = PoseWithCovarianceStamped()
checkpoint = PoseWithCovarianceStamped()
margin = 0.2

# ---------------------------------------------------------------------------- #
#                              Initialize setpoint                             #
# ---------------------------------------------------------------------------- #
checkpoint.pose.pose.position.x = 0.0#-2.0
checkpoint.pose.pose.position.y = 0.0#-0.5
checkpoint.pose.pose.position.z = 0.0

[x,y,z,w]=quaternion_from_euler(0.0,0.0,0.0)
checkpoint.pose.pose.orientation.x = x
checkpoint.pose.pose.orientation.y = y
checkpoint.pose.pose.orientation.z = z
checkpoint.pose.pose.orientation.w = w


while True:
# ---------------------------------------------------------------------------- #
# Compare current position and set position and Repeat publishing set position 
# 현재위치와 초기화 위치를 지속적으로 비교하면서 허용오차 범위에 들어올 때까지 
# 지속적으로 초기화 위치 publish 허용오차 이내로 들어오면 종료
# ---------------------------------------------------------------------------- #
    if is_same_postion(checkpoint,current_pose):
        print("current_position")
        print(current_pose)

        print("\n\ncheck_position")
        print(checkpoint)
        print("-------------------Position initialize finished!!!!-------------------\n\n")
        break
    else:
        print("Publishing initial point...")
        print("current_position")
        print(current_pose)

        print("\n\ncheck_position")
        print(checkpoint)
        rate.sleep()
        pub.publish(checkpoint)