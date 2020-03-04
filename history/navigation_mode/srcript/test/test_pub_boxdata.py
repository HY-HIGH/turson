#!/usr/bin/env python
#-*- coding:utf-8 -*-
# 퍼블리시할 정보 
# x_mid
# y_mid
# box_size
# -------------vector 3
# box_count
# -------------  


from darknet_ros_msgs.msg import BoundingBoxes #  이미지 정보 메세지 타입
from turson_navigation.msg import Box_data
import rospy #로스 파이 패키지


def cb_bounding_boxes(image_data): #image_data 객체 리스트
    pub = rospy.Publisher('/box_data', Box_data, queue_size=10) #토픽이름 부여, 자료형 
    # 수정할 변수 
   

    # 이부분 수정 필요 

    
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
   
    
    x_mid = ((x_max + x_min) / 2) / frame_width
    y_mid = ((y_max + y_min) / 2) / frame_height
    box_size = (x_length * y_length) 
    #box_size = (x_length * y_length) / (frame_height * frame_width)

    #print ("x_mid : ",x_mid) #0
    #print ("y_mid : ",y_mid) #0
    #print ("box_size : ",box_size)
    
    temp_box_data = Box_data()
    temp_box_data.x_mid         = x_mid
    temp_box_data.y_mid         = y_mid
    temp_box_data.box_size      = box_size
    temp_box_data.box_count     = box_count
    pub.publish(temp_box_data)

def node_init():
    rospy.init_node('pub_boxdata', anonymous=True)# 노드 초기화 #노드이름
    rate = rospy.Rate(1) # 발행 속도 10hz 
    rospy.Subscriber('/darknet_ros/bounding_boxes',BoundingBoxes,cb_bounding_boxes)
    while not rospy.is_shutdown():
        print('ok')
        rate.sleep

# 함수 시작부분

if __name__ == '__main__':
    try:
        node_init()
            
            
       
    except rospy.ROSInterruptException:
        pass