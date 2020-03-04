# #!/usr/bin/env python
# #-*- coding:utf-8 -*-

# #---------------------------Import section-----------------------------
# import rospy 
# import math
# import copy
# from std_msgs.msg import Int64
# from nav_msgs.msg import Odometry
# from move_base_msgs.msg import MoveBaseActionResult,MoveBaseActionFeedback,MoveBaseFeedback
# from geometry_msgs.msg import Vector3,Quaternion,PoseStamped,Twist
# from tf.transformations import quaternion_from_euler,euler_from_quaternion  
# #-----------------------------------------------------------------------

# # ---------------------------------------------------------------------------- #
# #                      Mode realtime update
# #
# # 모드를 지속적으로 실시간으로 update하는 subscriber callback 함수
# # 모드를 다른 함수에서도 참조하기 위해 불가피하게 전역변수 선언
# # ---------------------------------------------------------------------------- #
# def is_reached_callback(result):
#     global is_reached_status

#     print(result.status)
#     print("="*15); print('\n')
# #-------------------------Main------------------------
# if __name__ == '__main__':
#     try:
#         #--------------------Initialize node ---------------------
#         rospy.init_node('Patrol', anonymous=False)
#         rospy.Subscriber('move_base/feedback',MoveBaseActionFeedback,is_reached_callback)
        
# # ---------------------------------------------------------------------------- #
# #                     Setup variables & main function call                     #
# # ---------------------------------------------------------------------------- #
#         global is_reached_status
#         rospy.spin()

#     except rospy.ROSInterruptException:
#         pass

#!/usr/bin/env python
#-*- coding:utf-8 -*-

#---------------------------Import section-----------------------------
import rospy 
import math
import copy
from std_msgs.msg import Int64
from nav_msgs.msg import Odometry
from move_base_msgs.msg import MoveBaseActionResult
from geometry_msgs.msg import Vector3,Quaternion,PoseStamped,Twist
from tf.transformations import quaternion_from_euler,euler_from_quaternion  
#-----------------------------------------------------------------------

# ---------------------------------------------------------------------------- #
#                      Mode realtime update
#
# 모드를 지속적으로 실시간으로 update하는 subscriber callback 함수
# 모드를 다른 함수에서도 참조하기 위해 불가피하게 전역변수 선언
# ---------------------------------------------------------------------------- #
def mode_callback(mode):
    global current_mode
    current_mode = mode.data

# ---------------------------------------------------------------------------- #
#                      Current position of Robot realtime update                  
# 
# 로봇의 현재좌표를 지속적으로 업데이트
#  - X-Y-Z 좌표 
#  - 로봇의 헤드 방향(Orientation)
# ---------------------------------------------------------------------------- #
def current_pose_callback(odom_data):

    global current_pose
    current_pose.pose.position.x = odom_data.pose.pose.position.x
    current_pose.pose.position.y = odom_data.pose.pose.position.y
    
    current_pose.pose.orientation.x = odom_data.pose.pose.orientation.x
    current_pose.pose.orientation.y = odom_data.pose.pose.orientation.y
    current_pose.pose.orientation.z = odom_data.pose.pose.orientation.z
    current_pose.pose.orientation.w = odom_data.pose.pose.orientation.w

def is_reached_callback(result):
    global goal_result
    goal_result = result.status.status

def go_patrol_point(x,y):
# ---------------------------------------------------------------------------- #
#                      Assign Patrol point and orientation
# 지정된 patrol point 위치 및 로봇 헤드 방향 지정
# ---------------------------------------------------------------------------- #
    global switch_patrol 

    if (switch_patrol == 0):
        yaw = math.radians(90)
    elif (switch_patrol == 1):
        yaw = math.radians(180)
    elif (switch_patrol == 2):
        yaw = math.radians(270)
    else :
        yaw = math.radians(360)

    robot_orient = Quaternion(*quaternion_from_euler(0,0,yaw))
    robot_destination = PoseStamped() 

    robot_destination.pose.position.x = x 
    robot_destination.pose.position.y = y 
    robot_destination.pose.position.z = 0.0
    
    robot_destination.pose.orientation.x = robot_orient.x
    robot_destination.pose.orientation.y = robot_orient.y
    robot_destination.pose.orientation.z = robot_orient.z
    robot_destination.pose.orientation.w = robot_orient.w
    
    pub_destination.publish(robot_destination)

def rotating_mission():
    global switch_patrol
    if (switch_patrol == 0):
        yaw = math.radians(270)
    elif (switch_patrol == 1):
        yaw = math.radians(360)
    elif (switch_patrol == 2):
        yaw = math.radians(90)
    else :
        yaw = math.radians(180)
    
    while True:
        global current_pose
        global current_mode
        global twist

        current_quaternion = [current_pose.pose.orientation.x,current_pose.pose.orientation.y,current_pose.pose.orientation.z,current_pose.pose.orientation.w]
        euler = euler_from_quaternion(current_quaternion)
        current_yaw = euler[2] + math.pi

        # 제자리 회전 중이라도 mode가 navigation mode 혹은 Image centralizing 중이라면
        # while 즉시 종료
        if (current_mode == 1) or (current_mode == 2):
            break

        if abs(current_yaw - yaw) < 0.2:
            twist.angular.x = 0.0
            twist.angular.y = 0.0
            twist.angular.z = 0.0
            print("Stop!")
            pub_twist.publish(twist)
            break
        else: # 양수: 반시계방향 회전 | 음수: 시계방향 회전
            twist.angular.x = 0.0
            twist.angular.y = 0.0
            twist.angular.z = -0.8
            print(twist.angular)
            print("rotating...")
            pub_twist.publish(twist)

        rate.sleep()

def is_reached_position(target_x,target_y):
# ---------------------------------------------------------------------------- #
#                              Check target point                              #
#  현재위치와 지속적으로 비교하며 patrol point에 도착했는지 확인
#  도착했다면 patrol point 전환
#  도착하지 않았다면 Patrol point로 이동 명령 다시 내림
# ---------------------------------------------------------------------------- #
    global current_pose
    global switch_patrol
    global current_mode
    global reached

    go_patrol_point(target_x,target_y)

    if goal_result != 3:
        pass
    else: 
    # patrol point에 도착하지 못하면, 해당위치로 계속 이동
    if ((abs(target_x - current_pose.pose.position.x) > distance_margin) or \
        (abs(target_y - current_pose.pose.position.y) > distance_margin)):
        if:
            pass
        else:
            go_patrol_point(target_x,target_y)
    
    # patrol point에 도착하면, 제자리 회전임무 수행
    else : 
        rotating_mission()
        switch_patrol_point()

        
def set_switch_patrol():
# ---------------------------------------------------------------------------- #
#                    Initialize goal point and patrol point             
# 초기 목표지점 지정
# - x,y 지정
# - switch_patrol 변수는 orientation 지정 및 x,y좌표 전환을 위해 사용된다.
# ---------------------------------------------------------------------------- #
    global x_goal
    global y_goal
    global switch_patrol

    x_goal = TOP_RIGHT[0]
    y_goal = TOP_RIGHT[1]
    switch_patrol = 0

def switch_patrol_point():
# ---------------------------------------------------------------------------- #
#                           Switch patrol x,y point 
# ---------------------------------------------------------------------------- #
    global x_goal
    global y_goal
    global switch_patrol
    
    if switch_patrol < 4:
        switch_patrol = switch_patrol +1
    else :
        switch_patrol = 0
    
    if switch_patrol == 0:
        x_goal = TOP_RIGHT[0]
        y_goal = TOP_RIGHT[1]
    elif switch_patrol == 1:
        x_goal = TOP_LEFT[0]
        y_goal = TOP_LEFT[1]
    elif switch_patrol == 2:
        x_goal = BOTTOM_LEFT[0]
        y_goal = BOTTOM_LEFT[1]
    else:
        x_goal = BOTTOM_RIGHT[0]
        y_goal = BOTTOM_RIGHT[1]

def calculate_shortest_distance_between_robot_and_patrol_point():
    distance_list = []
    global switch_patrol

    distance_list.append( calculate_distance(TOP_LEFT[0],TOP_LEFT[1]) )
    distance_list.append( calculate_distance(TOP_RIGHT[0],TOP_RIGHT[1]) )
    distance_list.append( calculate_distance(BOTTOM_LEFT[0],BOTTOM_LEFT[1]) )
    distance_list.append( calculate_distance(BOTTOM_RIGHT[0],BOTTOM_RIGHT[1]) )
    
    min_patrol_point = distance_list.index(min(distance_list))

    if min_patrol_point == 0:
        switch_patrol = 0
        switch_patrol_point()
    elif min_patrol_point == 1:
        switch_patrol = 4
        switch_patrol_point()
    elif min_patrol_point == 2:
        switch_patrol = 1
        switch_patrol_point()
    else:
        switch_patrol = 2
        switch_patrol_point()

def calculate_distance(x,y):
    global current_pose
    distance = math.sqrt(math.pow((current_pose.pose.position.x - x),2)+ math.pow((current_pose.pose.position.y - y),2))

    return distance

def patrol_mode():
# ---------------------------------------------------------------------------- #
#                             Initiate patrol mode             
# Patrol mode를 시행하며, 지속적으로 현재의 mode 및 로봇의 위치를 확인하면서 해당 조건에 맞는
# Patrol point와 orientation을 publish
# Navigation 모드에 진입 후에는 지속적으로 복귀 point, 4가지 patrol point 중 최단거리 계산
# ---------------------------------------------------------------------------- #
    while True:
        global current_mode
        global current_pose

        if current_mode == 0 :
            rospy.loginfo("Patrol mode activating: %d"%current_mode)
            #is_reached_position(x_goal,y_goal)
            
        elif current_mode == 1:
            rospy.loginfo("Patrol mode deactivating: %d"%current_mode)
            #calculate_shortest_distance_between_robot_and_patrol_point()
        else:
            rospy.loginfo("Image centralizeing...: %d"%current_mode)
            #pub_stop_destination.publish(current_pose)
        rate.sleep()

   
#-------------------------Main------------------------
if __name__ == '__main__':
    try:
        #--------------------Initialize node ---------------------
        rospy.init_node('Patrol', anonymous=False)
        #------------------Define globalvariables-----------------
        global current_pose;global current_mode;global twist

        global BOTTOM_LEFT; global BOTTOM_RIGHT; global TOP_LEFT; global TOP_RIGHT

        global cnt
        global goal_result
        global switch_patrol
        global distance_margin
        #---------------------Define variables--------------------
        twist = Twist()                  # 로봇의 제자리 회전을 위해 필요
        current_mode = 0                 # 현재 로봇 모드 실시간 update
        current_pose = PoseStamped()     # 현재 로봇의 위치 실시간 update
        
        BOTTOM_LEFT = [-2,0.5]; BOTTOM_RIGHT = [-2,-0.5]; TOP_LEFT = [0.5,0.5]; TOP_RIGHT = [0.5,-0.5] # Patrol point 
        
        cnt = 0
        goal_result = False
        distance_margin = 0.1            # 현재위치와 Patrol point 사이의 허용오차
        rate = rospy.Rate(1)             # while문 속도 제어를 위한 변수
        #---------------------Set publisher & subscriber----------
        # 3 Publisher: 
        #   1) Twist:turtlebot 제자리 회전을 위해 위해 필요
        #   2) Navigation: Patrol point 위치로 이동하기 위해 필요
        #   3) Stop Navigation: 정지 위치 Navigationing을 하기 위해 필요
        # 2 Subscriber:
        #   1) Mode: 현재 모드를 업데이트 하기 위해 필요
        #   2) current_pose: 로봇의 현재 위치를 알기 위해 필요
        pub_twist = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        pub_destination = rospy.Publisher('set_robot_destination', PoseStamped, queue_size=10)
        pub_stop_destination = rospy.Publisher('set_robot_destination', PoseStamped, queue_size=10)
        rospy.Subscriber('mode_control',Int64, mode_callback) 
        rospy.Subscriber('/odom', Odometry, current_pose_callback)
        rospy.Subscriber('/move_base/result',MoveBaseActionResult,reached_callback)
# ---------------------------------------------------------------------------- #
#                     Setup variables & main function call                     #
# ---------------------------------------------------------------------------- #
        set_switch_patrol()              # 초기 Patrol point 위치 지정
        patrol_mode()                    # Patrol mode initiate

    except rospy.ROSInterruptException:
        pass