#!/usr/bin/env python
#-*- coding: utf-8 -*-

#--------------configuration section-----------------
# 파이썬으로 시작하는 코드임을 명시적으로 알려준다.
# utf-8 인코딩방식을 이용해 한글주석을 사용가능하게 끔한다.
#----------------------------------------------------

#-------------------import section-------------------
# rospy:
# String:기본적인 문자열 통신을 위해 import
# Mode control을 위해 노드간 통신용 msg type을 별도로 선언
import rospy
from std_msgs.msg import String
from mode_control.msg import Mode
#----------------------------------------------------

def talkcallback1(mode):
    '''
    Subscriber이므로 메세지 수신마다 Callback함수가 작동한다.
    mode의 상태를 확인 후, mode=0이면 관련 문자열을 출력한다.
    mode=1이면 아무동작을 수행하지 않는다.
    '''
    if (mode.mode==0):
        hello_str = "hello jinsung"
        rospy.loginfo('Talker1 is publishing')
        pub.publish(hello_str)
    else:
        pass

#-------------------------Main------------------------
#프로그램은 여기서부터 시작(Main start point)
if __name__ == '__main__':
    try:
        '''
        Node명: talker1
        1 Publisher: mode에 맞게 문자열을 송신한다.
        1 Subscriber:mode를 수신한다.
        '''
        rospy.init_node('talker1', anonymous=False)   
        pub = rospy.Publisher('chatter', String, queue_size=10)
        rospy.Subscriber('mode_control', Mode, talkcallback1)
        
        rospy.spin()
    except rospy.ROSInterruptException:
        pass