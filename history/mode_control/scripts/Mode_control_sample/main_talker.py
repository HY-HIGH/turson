#!/usr/bin/env python
#-*- coding: utf-8 -*-

import rospy
from std_msgs.msg import String
import talking
from mode_control.msg import Mode

def maintalker():
    '''
    Name: main_talker
    Node:
         1 Publisher => Topic=mode_control, Message type=Mode.msg
         1 Parameter => 'mode'
    '''
    rospy.init_node('main_talker', anonymous=False)
    pub_mode = rospy.Publisher('mode_control', Mode, queue_size=10)
    #----------------------------------------------------
    # mode라고 불리는 int64 메세지타입을 지속적으로 퍼블리시함으로써 mode제어를 하는 코드.
    # 파라미터 설정을 통해서 외부에서 mode제어를 할 수 있게 설정.
    # while문에서는 현재 파라미터값을 계속 읽어드림과 동시에 mode를 퍼블리시한다.
    #----------------------------------------------------
    
    rate = rospy.Rate(10) # 10hz
    
    rospy.loginfo('Setting parameter->mode=0')
    rospy.set_param('mode',0)
    
    while not rospy.is_shutdown():
        rospy.loginfo('Current mode is %d'%(rospy.get_param('mode')))
        pub_mode.publish(rospy.get_param('mode'))

        rate.sleep()

if __name__ == '__main__':
    try:
        maintalker()

    except rospy.ROSInterruptException:
        pass