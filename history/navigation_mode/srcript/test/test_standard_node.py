#!/usr/bin/env python
#-*- coding:utf-8 -*-

# -------------  


import rospy #로스 파이 패키지


def cb_bounding_boxes(image_data): #image_data 객체 리스트
    
    pub.publish(target_box_data)

def node_init():
    rate = rospy.Rate(1) # 발행 속도 10hz 
    while not rospy.is_shutdown():
        #print('ok')
        rate.sleep

# 함수 시작부분

if __name__ == '__main__':
    try:
        # 변수 선언 및 메인 함수
        rospy.init_node('pub_boxdata', anonymous=True)# 노드 초기화 #노드이름
        
        pub = rospy.Publisher('/box_data', Box_data, queue_size=10) #토픽이름 부여, 자료형 
        rospy.Subscriber('/darknet_ros/bounding_boxes',BoundingBoxes,cb_bounding_boxes)
        
        global_temp_position_x          = 0     
        global_temp_position_y          = 0         
        global_temp_orientation_x       = 0
        global_temp_orientation_y       = 0
        global_temp_orientation_z       = 0
        global_temp_orientation_w       = 0
        
        odom = Odometry()
        node_init()
            
            
       
    except rospy.ROSInterruptException:
        pass