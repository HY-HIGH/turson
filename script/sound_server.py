#!/usr/bin/env python
import rospy, os, sys
from sound_play.msg import SoundRequest
#hothotfix test
from sound_play.libsoundplay import SoundClient

def sleep(t):
    try:
        rospy.sleep(t)
    except:
        pass

def sound_server():
    while not rospy.is_shutdown():
        if (rospy.get_param('person_detected') == 1):
            if (rospy.get_param('person_warning') == 1):
                soundhandle.stopAll()
                soundhandle.say('This is restricted area! please go back!')
                sleep(4)
            else:
                soundhandle.stopAll()
                soundhandle.say('Person Detected!')
                sleep(2)

                
        elif (rospy.get_param('person_cleared') == 1):
            soundhandle.stopAll()
            soundhandle.say('Person cleared!')
            sleep(2)
        else:
            soundhandle.stopAll()


        rate.sleep


if __name__ == '__main__':
    rospy.init_node('sound_server', anonymous = True)
    soundhandle = SoundClient()
    rate = rospy.Rate(10)

    rospy.set_param('person_detected',0)
    rospy.set_param('person_warnig',0)
    rospy.set_param('person_cleared',0)
    
    soundhandle.stopAll()

    sound_server()
