#!/usr/bin/env python
#-*- coding: utf-8 -*-

import rospy

from move_base_msgs.msg     import MoveBaseActionResult  # result 메시지

global_result = False     

def cb_result(result):
    global global_result
    if result.status.status == 3:

        global_result = True
        print('is it reached ? :',global_result)
    else :
        global_result = False

if __name__ == '__main__':
    # initialize node
    rospy.init_node('parameter_monitor')
    # print in console that the node is running
    rospy.loginfo('started parameter_monitor node !')
    # create tf listener
    rospy.Subscriber('/move_base/result',MoveBaseActionResult,cb_result)    # 목적지 도착 여부 계속 서브스크라이브

    # set the node to run 1 time per second (1 hz)
    rate = rospy.Rate(1.0)
    # loop forever until roscore or this node is down
    while not rospy.is_shutdown():
        try:
            



            rospy.loginfo('-----------------------------------------')
            rospy.loginfo('현재 mode :{}'.format(rospy.get_param('mode')))
            rospy.loginfo('current pose에 멈추면 1 이됨 :{}'.format(rospy.get_param('navigation_status')))
            rospy.loginfo('해당 값이 1 일 때만 네비게이션 목적지를 찍어줌 :{}'.format(rospy.get_param('nav_once')))
            rospy.loginfo('사람이 검출되고 centrallize 후 정지 하면 1이됨 :{}'.format(rospy.get_param('stop_signal')))
            print('')

            

        except rospy.ROSInterruptException:
            pass
        # sleep to control the node frequency
        rate.sleep()