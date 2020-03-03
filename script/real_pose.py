#!/usr/bin/env python
import rospy
import tf
from geometry_msgs.msg      import PoseStamped           

if __name__ == '__main__':
    # initialize node
    rospy.init_node('tf_listener')
    # print in console that the node is running
    rospy.loginfo('started listener node !')
    # create tf listener
    listener = tf.TransformListener()
    # set the node to run 1 time per second (1 hz)
    rate = rospy.Rate(10.0)
    # loop forever until roscore or this node is down
    while not rospy.is_shutdown():
        try:
            # listen to transform
            (trans,rot) = listener.lookupTransform('/map', '/base_link', rospy.Time(0))
            # print the transform
            
            rospy.loginfo('---------')
            #rospy.loginfo('Translation: ' + str(trans))
            #rospy.loginfo('Rotation: ' + str(rot))
            pub_base_link = rospy.Publisher('/real_pose', PoseStamped, queue_size = 10) 
            real_pose = PoseStamped()
            real_pose.pose.position.x        =        trans[0]
            real_pose.pose.position.y        =        trans[1]     
            real_pose.pose.position.z        =        trans[2]     
            real_pose.pose.orientation.x     =        rot[0] 
            real_pose.pose.orientation.y     =        rot[1] 
            real_pose.pose.orientation.z     =        rot[2] 
            real_pose.pose.orientation.w     =        rot[3] 
            pub_base_link.publish(real_pose)

        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue
        # sleep to control the node frequency
        rate.sleep()