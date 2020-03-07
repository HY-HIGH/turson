#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os
import sys
import subprocess
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))) 

import rospy 
from text_color import color
# from darknet_ros_msgs.msg import ObjectCount

# def cb_box_count(box_count) :
#     global global_box_count     
#     global_box_count = box_count.count
#     print ("count :" + str(global_box_count))

def init_node():
    while not rospy.is_shutdown():
        print('Working now')
        RATE.sleep()

if __name__ == '__main__':
    try:
    #----Initialize node & Define publisher/subscriber---
        rospy.init_node('box_count', anonymous=False)
        # rospy.Subscriber('/darknet_ros/found_object',ObjectCount,cb_box_count)           
    #-------------------Define variables-----------------
        global_box_count = 0     
        RATE = rospy.Rate(1)
    #----------------Initiate main statement-------------
        os.chdir(os.path.expanduser("~"))
        os.chdir('./catkin_ws/src')
        result = subprocess.check_output ('ls', shell=True)
        print(color.GREEN  + "="*25 + color.END)
        print(color.GREEN +'[ok] '+ color.END + '패키지 목록 출력')
        print(result.decode().strip('\n'))
        print(color.GREEN + "="*25 + '\n' + color.END)
        print(color.GREEN +'[ok] ' + color.END + 'Test node initiate' )
        init_node()

    except rospy.ROSInterruptException:
        pass

