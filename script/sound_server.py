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
                print ("person detected")
                s1.play()
                sleep(4)
    
            else:
                soundhandle.stopAll()
                print ("person warning")
                s2.play()
                sleep(4)

                
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

    s1 = soundhandle.waveSound("person.ogg", 1)
    s2 = soundhandle.waveSound("danger.ogg", 1)
    s3 = soundhandle.waveSound("corona.ogg", 1)
    
    soundhandle.stopAll()

    sound_server()
