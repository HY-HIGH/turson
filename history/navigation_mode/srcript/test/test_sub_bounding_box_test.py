#!/usr/bin/env python
#-*- coding:utf-8 -*-

# 1. 이미지 정보 sub /darknet_ros/bounding_boxes

# 2. odom 정보 sub
# 3. mode 정보 sub

# 위치 좌표 및 오리엔테이션 퍼블리시 

from geometry_msgs.msg import PoseStamped #메세지 패키지 속 메세지 모듈을 가져와서 그중 PoseStamped를 가져온다.
from darknet_ros_msgs.msg import BoundingBoxes #  이미지 정보 메세지 타입
import rospy #로스 파이 패키지


# 전역 변수 설정 

global global_x_mid
global global_y_mid
global global_box_size
global global_box_count





def cb_bounding_boxes(image_data): #image_data 객체 리스트
    # 수정할 변수 
    global global_x_mid
    global global_y_mid
    global global_box_size
    global global_box_count

    # 이부분 수정 필요 

    #print ("I got image")
    
    # 1개의 박스만 받는다고 가정
    box_count = len(image_data.bounding_boxes)

    x_min = image_data.bounding_boxes[0].xmin
    x_max = image_data.bounding_boxes[0].xmax
    y_min = image_data.bounding_boxes[0].ymin
    y_max = image_data.bounding_boxes[0].ymax 
  
    float(x_min)
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
   
    
    global_x_mid = ((x_max + x_min) / 2) / frame_width
    global_y_mid = ((y_max + y_min) / 2) / frame_height
    global_box_size = (x_length * y_length) / (frame_height * frame_width)

    # print ("x_mid : ",global_x_mid) #0
    # print ("y_mid : ",global_y_mid) #0
    # print ("box_size : ",global_box_size)


    
    #get_xmin = data[0]
    # get_xmax = data[2]
    # get_ymin = data[3]
    # get_ymax = data[4]
    #get_xmin = data.xmin
    #get_ymin = image_data.bounding_boxes.ymin
    #get_xmax = image_data.bounding_boxes.xmax
    #get_ymax = image_data.bounding_boxes.ymax
   # print ('x_min : ',get_xmin)
    # print ('x_max : ',get_xmax)
    # print ('y_min : ',get_ymin)
    # print ('y_max : ',get_xmax)

    #return global_x_mid, global_y_mid, global_box_size, global_box_count
    
def destination():
    sub = rospy.Subscriber('/darknet_ros/bounding_boxes',BoundingBoxes,cb_bounding_boxes)
    pub = rospy.Publisher('set_robot_destination', PoseStamped, queue_size=10) #토픽이름 부여, 자료형 
    
    rospy.init_node('publish_position', anonymous=True)# 노드 초기화 #노드이름
    #x_mid, y_mid, box_size, box_count = cb_bounding_boxes()
    ### 정해진 형식###
    rate = rospy.Rate(1) # 발행 속도 10hz 
    while not rospy.is_shutdown():
        #hello_str = "hello world %s" % rospy.get_time()
        #rospy.loginfo(hello_str)

        robot_destination = PoseStamped() 
        
        robot_destination.pose.position.x = 1
        robot_destination.pose.position.y = 2
        robot_destination.pose.position.z = 0.0
        

        pub.publish(robot_destination)#퍼블리시 할 항목
        rate.sleep()# 반복문을 위한 일시정지
        # print ('------------------------------')
        # print ('current_x : ' ,)
        # print ('current_y : ' ,global_current_y)
        # print ('current_w : ' ,global_current_w)
        print ('                              ')
        print('goto position x:',robot_destination.pose.position.x)
        print('goto position y:',robot_destination.pose.position.y)
        print('goto position z:',robot_destination.pose.position.z)
        print('x_mid',global_x_mid)
     
        
# 함수 시작부분

if __name__ == '__main__':
    try:
       
        destination()
       
    except rospy.ROSInterruptException:
        pass