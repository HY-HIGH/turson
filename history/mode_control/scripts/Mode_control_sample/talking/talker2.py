#!/usr/bin/env python
#-*- coding: utf-8 -*-

#-------------------import section-------------------
# rospy:
# String:기본적인 문자열 통신을 위해 import
# Mode control을 위해 노드간 통신용 msg type을 별도로 선언
import rospy
from std_msgs.msg import String
from mode_control.msg import Mode
#----------------------------------------------------

def talkcallback2(mode):
    if (mode.mode==1):
        hello_str = "hello injae"
        rospy.loginfo('Talker2 is publishing')
        pub.publish(hello_str)
    else:
        pass

#-------------------------Main------------------------
#프로그램은 여기서부터 시작(Main start point)
#talker1과 구조가 똑같으므로 talker.py 주석참조
if __name__ == '__main__':
    try:
        rospy.init_node('talker2', anonymous=False)   
        pub = rospy.Publisher('chatter', String, queue_size=10)
        rospy.Subscriber('mode_control', Mode, talkcallback2)

        rospy.spin()
    except rospy.ROSInterruptException:
        pass
