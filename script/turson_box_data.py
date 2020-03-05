#!/usr/bin/env python
#-*- coding:utf-8 -*-
# 퍼블리시할 정보 
# x_mid
# y_mid
# box_size
# box_count
# -------------  


from darknet_ros_msgs.msg import BoundingBoxes #  이미지 정보 메세지 타입
from turson.msg import Box_data #커스텀 메시지
import rospy #로스 파이 패키지
import time

def cb_bounding_boxes(image_data): #image_data 객체 리스트
    #rospy.set_param('person_detect',1) # 사람 포착
    pub = rospy.Publisher('/box_data', Box_data, queue_size=10) #토픽이름 부여, 자료형 
    # 수정할 변수 
   

    # 이부분 수정 필요 

    # 5개를 받아 평균 낸다. 
    # 여러개의 박스중 가장 큰 박스를 반환함
    target_box = [] # 가장 큰박스 정보 4가지 -> 퍼블리시 

    box_count = len(image_data.bounding_boxes) # 박스의 개수
    #temp_boxes = []# 리스트로 만들음 list()
    temp_boxes_size = [] #사이즈만 모아 놓은 리스트 

    for count in range (box_count): # 0번째 박스 부터 하나씩 대입한다.
        temp_x_min = image_data.bounding_boxes[count].xmin
        temp_x_max = image_data.bounding_boxes[count].xmax
        temp_y_min = image_data.bounding_boxes[count].ymin
        temp_y_max = image_data.bounding_boxes[count].ymax 
  
        float(temp_x_min)# float 으로 변경
        float(temp_x_max)
        float(temp_y_min)
        float(temp_y_max)
        
        #카메라 설정에 따라 변함
        frame_width = 640.0 #가로 
        frame_height = 480.0 #세로 
        
        temp_x_length = temp_x_max - temp_x_min
        temp_y_length = temp_y_max - temp_y_min
   
        temp_x_mid = ((temp_x_max + temp_x_min) / 2) / frame_width
        temp_y_mid = ((temp_y_max + temp_y_min) / 2) / frame_height

        temp_box_size = (temp_x_length * temp_y_length) 
        #temp_box_data = [temp_x_mid temp_y_mid temp_box_size] #3가지 정보 
       
        #temp_boxes.append(temp_box_data) #박스의 모든 정보 보관
        temp_boxes_size.append(temp_box_size) #박스 사이즈 정보 만을 보관 
    # 가장 큰 박스의 크기가 있는 리스트 번호 구하기
    # biggest_box_size = temp_boxes_size[0]
    # for temp_size in temp_boxes_size:
    #     if temp_size > biggest_box_size:
    #         biggest_box_size = temp_size  

    size_max = max(temp_boxes_size)
    num_max = temp_boxes_size.index(size_max) #가장 큰 박스의 리스트 번호
    x_min = image_data.bounding_boxes[num_max].xmin
    x_max = image_data.bounding_boxes[num_max].xmax
    y_min = image_data.bounding_boxes[num_max].ymin
    y_max = image_data.bounding_boxes[num_max].ymax 

    float(x_min)# float 으로 변경
    float(x_max)
    float(y_min)
    float(y_max)
    
    #카메라 설정에 따라 변함
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
    print ("box_size : ",box_size)
    print ("box_count : ",box_count)

    
    target_box_data               = Box_data()
    target_box_data.x_mid         = x_mid
    target_box_data.y_mid         = y_mid
    target_box_data.box_size      = box_size
    target_box_data.box_count     = box_count
    pub.publish(target_box_data)
    

def node_init():
    rospy.init_node('turson_box_data', anonymous=False)# 노드 초기화 #노드이름
    rate = rospy.Rate(1) # 발행 속도 10hz 
    rospy.Subscriber('/darknet_ros/bounding_boxes',BoundingBoxes,cb_bounding_boxes)
    while not rospy.is_shutdown():
        #print('ok')
        rate.sleep

# 함수 시작부분

if __name__ == '__main__':
    try:
        node_init()
            
            
       
    except rospy.ROSInterruptException:
        pass