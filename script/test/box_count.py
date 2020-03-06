#!/usr/bin/env python
#-*- coding:utf-8 -*-
from darknet_ros_msgs.msg import ObjectCount

import rospy #로스 파이 패키지

def cb_box_count(box_count) :
    global global_box_count     
    global_box_count = box_count.count
    print ("count :" + str(global_box_count))
def init_node():
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        #print('ok')
        rate.sleep()

if __name__ == '__main__':
    try:


    #----Initialize node & Define publisher/subscriber---
        rospy.init_node('box_count', anonymous=False)


        rospy.Subscriber('/darknet_ros/found_object',ObjectCount,cb_box_count)           
       

  

    #-------------------Define variables-----------------
                                            
        global_box_count                  =0     

    #----------------Initiate main statement-------------
        init_node()

    except rospy.ROSInterruptException:
        pass
