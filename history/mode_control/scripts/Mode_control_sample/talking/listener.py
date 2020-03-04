#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from mode_control.msg import Mode

def listener_callback(data):
    rospy.loginfo("I heard %s", data.data)

  
def listener():

    rospy.init_node('listener', anonymous=False)
    rospy.Subscriber("chatter", String, listener_callback)
    
    rospy.spin()