#!/usr/bin/env python
#-*- coding:utf-8 -*-


import rospy #로스 파이 패키지

from darknet_ros_msgs.msg   import ObjectCount
average_box_count = 0
global_box_count = 0
temp_count_list = [] #글로벌로 선언 
def cb_box_count(box_count): #image_data 객체 리스트
    
    global global_box_count
    global_box_count = box_count.count

    # Box Count
    if box_count.count > 0:
        bool_person = (box_count.count / box_count.count)## 존재 0 or 1
    else :
        bool_person = 0
    temp_count_list.append(bool_person)

    if len(temp_count_list) > 30:
        temp_count_list.pop(0)
        print("list count    : ",len(temp_count_list))
        print("last 10 index : ",temp_count_list[20:29])
    #float (average_list)
    sum_list=float(sum(temp_count_list))
    list_length= float (len(temp_count_list))
    average_list = float(sum_list/list_length)
    print ("average          : ",average_list)
    if average_list > 0.2:
        average_box_count = 1
    elif average_list <= 0.2:
        average_box_count = 0 
    
    # print ("is there person? : ",average_box_count)
    
    print ("box_count : ",average_box_count)
    print ("______________________________________")
    

    
 

def node_init():
    rospy.init_node('turson_box_count', anonymous=False)# 노드 초기화 #노드이름
    rate = rospy.Rate(10) # 발행 속도 10hz 
    rospy.Subscriber('/darknet_ros/found_object',ObjectCount,cb_box_count)           
    
    while not rospy.is_shutdown():
        #print('ok')
        rate.sleep

# 함수 시작부분

if __name__ == '__main__':
    try:
        node_init()
            
            
       
    except rospy.ROSInterruptException:
        pass