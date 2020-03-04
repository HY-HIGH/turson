#!/usr/bin/env python
#-*- coding:utf-8 -*-
# 이미지  정보를 받아 와서 목표지점 퍼블리시
import rospy #로스 파이 패키지
from random import *
from tf.transformations import quaternion_from_euler
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Vector3 # 벡터 (x,y,z)
from geometry_msgs.msg import Quaternion #쿼터니언(x,y,z,w)
from geometry_msgs.msg import PoseStamped #메세지 패키지 속 메세지 모듈을 가져와서 그중 PoseStamped를 가져온다.
# float64 x pose x
# float64 y pose y
# float64 z orientation

    

def destination():
    pub = rospy.Publisher('set_robot_destination', PoseStamped, queue_size=10) #토픽이름 부여, 자료형 
    rospy.init_node('publish_position', anonymous=True)# 노드 초기화 #노드이름
    
    ### 정해진 형식###
    rate = rospy.Rate(0.1) # 발행 속도 10hz 
    while not rospy.is_shutdown():
        #hello_str = "hello world %s" % rospy.get_time()
        #rospy.loginfo(hello_str)
        rand_0to1 = random()
        rand_radian = uniform(-2,2)
        yaw = rand_radian # yaw값 foseja -2~2 사이 (360도)
        #yaw = -1 # yaw값 정의

        robot_orient = Quaternion(*quaternion_from_euler(0,0,yaw)) #* positional argument 만 받겟다


        robot_destination = PoseStamped() 
        
        robot_destination.pose.position.x = 0.5
        robot_destination.pose.position.y = rand_0to1
        robot_destination.pose.position.z = 0.0
        
        robot_destination.pose.orientation.x = robot_orient.x
        robot_destination.pose.orientation.y = robot_orient.y
        robot_destination.pose.orientation.z = robot_orient.z
        robot_destination.pose.orientation.w = robot_orient.w


        
        
        pub.publish(robot_destination)#퍼블리시 할 항목
        rate.sleep()# 반복문을 위한 일시정지
        print("-----------------------")
        print('goto position x:',robot_destination.pose.position.x)
        print('goto position y:',robot_destination.pose.position.y)
        print('goto position z:',robot_destination.pose.position.z)
        print('goto orientation x:',robot_destination.pose.orientation.x)
        print('goto orientation y:',robot_destination.pose.orientation.y)
        print('goto orientation z:',robot_destination.pose.orientation.z)
        print('goto orientation w:',robot_destination.pose.orientation.w)
    

if __name__ == '__main__':
    try:
        destination()
       
    except rospy.ROSInterruptException:
        pass