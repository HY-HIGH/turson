#!/usr/bin/env python
#-*- coding:utf-8 -*-
# 이미지  정보를 받아 와서 목표지점 퍼블리시
import rospy #로스 파이 패키지
from random import *

from geometry_msgs.msg import PoseStamped #메세지 패키지 속 메세지 모듈을 가져와서 그중 PoseStamped를 가져온다.
# float64 x pose x
# float64 y pose y
# float64 z orientation

    

def destination():
    pub = rospy.Publisher('set_robot_destination', PoseStamped, queue_size=10) #토픽이름 부여, 자료형 
    rospy.init_node('publish_position', anonymous=True)# 노드 초기화 #노드이름
    
    ### 정해진 형식###
    rate = rospy.Rate(1) # 발행 속도 10hz 
    while not rospy.is_shutdown():
        #hello_str = "hello world %s" % rospy.get_time()
        #rospy.loginfo(hello_str)
        rand_float_1 = random()
        rand_float_2 = random()
        robot_destination = PoseStamped() 
        
        robot_destination.pose.position.x = 0.5
        robot_destination.pose.position.y = rand_float_1
        robot_destination.pose.position.z = rand_float_2
        pub.publish(robot_destination)#퍼블리시 할 항목
        rate.sleep()# 반복문을 위한 일시정지
        print('goto x:%lf',robot_destination.pose.position.x)
        print('goto x:%lf',robot_destination.pose.position.y)
        print('goto x:%lf',robot_destination.pose.position.z)

if __name__ == '__main__':
    try:
        destination()
       
    except rospy.ROSInterruptException:
        pass