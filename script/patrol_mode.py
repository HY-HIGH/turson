#!/usr/bin/env python
#-*- coding:utf-8 -*-

#---------------------------Import section-----------------------------
import math
import copy
import time
import rospy 
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
def current_pose_callback(real_pose):
    global current_pose
    current_pose = real_pose

# ---------------------------------------------------------------------------- #
#                     Current robot status realtime update                     #
# 로봇의 현재 네비게이션 상태를 지속적으로 업데이트
#  이동 중: status = 1
#  목표지점 도달: status = 3
# ---------------------------------------------------------------------------- #
def status_callback(result):
    global robot_status
    
    if result.status.status == 3:
        robot_status = True
    else:
        pass
# ---------------------------------------------------------------------------- #
#                      Assign Patrol point and orientation
# 지정된 patrol point 위치 및 로봇 헤드 방향 지정
# ---------------------------------------------------------------------------- #
def go_patrol_point(x,y):
    global switch_patrol 
    if (switch_patrol == 0):
        yaw = math.radians(0)
    elif (switch_patrol == 1):
        yaw = math.radians(0)
    elif (switch_patrol == 2):
        yaw = math.radians(180)
    else :
        yaw = math.radians(0)

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
    print("x_target:{} y_target:{}".format(x,y))

# ---------------------------------------------------------------------------- #
#                             Get current position                             #
# 현재위치를 받기 위해 일정시간이 필요함
# postion_timer함수는 그 시간을 확보하기 위한 timer
# ---------------------------------------------------------------------------- #
def position_timer(second):
    time_end = time.time() + second
    while True:
        if time.time() > time_end:
            break

# ---------------------------------------------------------------------------- #
#                               Rotating mission                               #
# Patrol point 도착 후 일정시간동안 시계방향으로 turtlebot이 회전하도록 하는 함수
# 회전함으로써 순찰지역의 사각지대를 최소화하기 위함
# 회전 중 current_mode =2, 즉, detection이 되어 image_centralizing 중이라면
# 모든 행동을 중지하고 image_centralizing에서 patrol_mode가 해야하는 역할을 수행
# ---------------------------------------------------------------------------- #

def rotating_mission(second):
    time_end = time.time() + second
    rate_temp = rospy.Rate(10)
    while True:
        if rospy.get_param('mode') == 2:
            print("Escape rotating mission!")
            break
        twist.angular.x = 0
        twist.angular.y = 0
        twist.angular.z = angular_velocity
        pub_twist.publish(twist)

        if time.time() > time_end:
            twist.angular.x = 0
            twist.angular.y = 0
            twist.angular.z = 0
            pub_twist.publish(twist)
            break
        rate_temp.sleep()
        print("Patrol_Rotating...")

def rotate_callibrate():
    global switch_patrol
    global current_pose
    if switch_patrol == 0:
        yaw = math.radians(180)
    elif switch_patrol == 1:
        yaw = math.radians(180)
    elif switch_patrol == 2:
        yaw = math.radians(360)
    else :
        yaw = math.radians(180)
    rate_temp = rospy.Rate(10)

    while True:
        global current_mode    
        current_quaternion = [current_pose.pose.orientation.x,current_pose.pose.orientation.y,current_pose.pose.orientation.z,current_pose.pose.orientation.w]
        euler = euler_from_quaternion(current_quaternion)
        current_yaw = euler[2]+math.pi
        if (abs((euler[2]+math.pi) - yaw)) < 0.3:
            twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = 0.0
            print('='*15);print("Callibration finished!!!");print('='*15);print('\n')
            pub_twist.publish(twist)
            break
        else: # 양수: 반시계방향 회전 | 음수: 시계방향 회전
            twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = -0.1  ## 속도 수정(-0.1)
            print("Callibrationing...")
            pub_twist.publish(twist)

        if rospy.get_param('mode') == 2:
            print("Escape rotating callibratioins!")
            break
        rate_temp.sleep()

# ---------------------------------------------------------------------------- #
#                              Check target point                              #
#  현재위치와 지속적으로 비교하며 patrol point에 도착했는지 확인
#  도착했다면 patrol point 전환
#  도착하지 않았다면 Patrol point로 이동 명령 다시 내림
# ---------------------------------------------------------------------------- #
def is_reached_position():
    global current_mode
    global current_pose
    global robot_status
    global robot_start
    global x_goal ; global y_goal
    global switch_patrol
    temp_error_check = False
    temp_switch_check = False
    if rospy.get_param('mode') == 2: # 이동 중에 대상이 포착된 경우 함수실행을 중지
        pass
    else:
        print("robot_start",robot_start)
        print("robot_status",robot_status)
        if (robot_start == False) and (robot_status == False): # 출발도 도착도 안했다면
            position_timer(0.8)
            past_position = copy.deepcopy(current_pose.pose.position)
            # print("past",past_position); print("="*15)
            # print("current",current_pose.pose.position);print('\n'*3)
            
            while True:
                if abs(past_position.x - current_pose.pose.position.x) > (distance_margin ) or \
                    abs(past_position.y - current_pose.pose.position.y) > (distance_margin ):
                    break
                else:#FIX
                    # if 조건을 바꾸는 곳: 현재와 목표위치와의 차이값이 거의 유사하거나 같다면 목적지 지정 잘못
                    if temp_error_check == False:
                        if abs(x_goal - current_pose.pose.position.x) < distance_margin and \
                            abs(y_goal - current_pose.pose.position.y) < distance_margin:
                            if temp_switch_check == False:
                                switch_patrol_point()
                                temp_error_check = True
                            else:
                                pass
                        else:#현재위치와 목표위치가 다르므로 error는 발생하지 않는다.
                            temp_error_check = True
                    # while을 계속 돌면서 수행될 곳, 아무일도 없이 넘어가야 함.    
                    else:
                        go_patrol_point(x_goal,y_goal)
                        print("Wait for start...\n")
                
                rate_main_while.sleep()
            
            robot_start = True
            temp_error_check = False
            temp_switch_check = False
            
        elif robot_start == True and robot_status == False : # 출발은 했는데 도착은 못했으면
            print("Moving...\n")

        elif robot_start == True and robot_status == True: # 출발도 했고 도착도 했다면
            robot_start = False
            robot_status = False

            rotating_mission(rotate_time_second)

            if rospy.get_param('mode') == 2:
                print("I do not rotate callibrate")
                pass
            else:
                rotate_callibrate()
            
            if rospy.get_param('mode') == 2:
                print("I do not switch patrol")
                pass
            else:
                switch_patrol_point()
        else: 
            robot_start  =  False
            robot_status =  False

                

# ---------------------------------------------------------------------------- #
#                    Initialize goal point and patrol point             
# 처음 목표지점 지정
# - x,y 지정
# - switch_patrol 변수는 orientation 지정 및 x,y좌표 전환을 위해 사용된다.
# ---------------------------------------------------------------------------- #       
def set_switch_patrol():
    global x_goal
    global y_goal
    global switch_patrol

    x_goal = TOP_RIGHT[0]
    y_goal = TOP_RIGHT[1]
    switch_patrol = 0

# ---------------------------------------------------------------------------- #
#                           Switch patrol x,y point 
# ---------------------------------------------------------------------------- #
def switch_patrol_point():
    global x_goal
    global y_goal
    global switch_patrol
    if switch_patrol < 3:
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
    # print("switch_patrol:{} x_target:{} y_target:{}".format(switch_patrol,x_goal,y_goal))

# ---------------------------------------------------------------------------- #
#          calculate_shortest_distance_between_robot_and_patrol_point          #
# Navigation 중 현재 위치 기준, 복귀 지점 계속 update 
# ---------------------------------------------------------------------------- #

def calculate_shortest_distance_between_robot_and_patrol_point():
    global switch_patrol
    distance_list = calculate_distance()
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

# ---------------------------------------------------------------------------- #
#                                    단순 거리계산                                #
# ---------------------------------------------------------------------------- #

def calculate_distance():
    global current_pose
    distance_1 = math.sqrt(math.pow((current_pose.pose.position.x - TOP_LEFT[0]),2)+ math.pow((current_pose.pose.position.y - TOP_LEFT[1]),2))
    distance_2 = math.sqrt(math.pow((current_pose.pose.position.x - TOP_RIGHT[0]),2)+ math.pow((current_pose.pose.position.y - TOP_RIGHT[1]),2))
    distance_3 = math.sqrt(math.pow((current_pose.pose.position.x - BOTTOM_LEFT[0]),2)+ math.pow((current_pose.pose.position.y - BOTTOM_LEFT[1]),2))
    distance_4 = math.sqrt(math.pow((current_pose.pose.position.x - BOTTOM_RIGHT[0]),2)+ math.pow((current_pose.pose.position.y - BOTTOM_RIGHT[1]),2))

    return [distance_1,distance_2,distance_3,distance_4]

# ---------------------------------------------------------------------------- #
#                             Initiate patrol mode             
# Patrol mode를 시행하며, 지속적으로 현재의 mode 및 로봇의 위치를 확인하면서 해당 조건에 맞는
# Patrol point와 orientation을 publish
# Navigation 모드에 진입 후에는 지속적으로 복귀 point, 4가지 patrol point 중 최단거리 계산
# Centralizing mode에서는 현위치 정지신호 계속발생, 정지이후에는 더 이상 발생하지 않음
# ---------------------------------------------------------------------------- #
def patrol_mode():
    temp_finished = False
    while True:
        global current_mode 
        global current_pose
        global robot_status
        global robot_start
        if rospy.get_param('mode') == 0 :
            print("[Patrol mode]: %d"%rospy.get_param('mode'))
            is_reached_position()
            temp_finished  = False
        elif rospy.get_param('mode') == 1:
            print("[Navigation mode]: %d"%rospy.get_param('mode'))
            calculate_shortest_distance_between_robot_and_patrol_point()
            robot_start = False
            robot_status = False
            temp_finished  = False
        else:
            print("temp_finished:{} robot_status:{}".format(temp_finished,robot_status)) # F F
            if temp_finished == False:#로봇이 멈출때 까지 실행
                if robot_status == False: #1
                    while True:
                        stop_rate = rospy.Rate(10)
                        print("Try to stop robot...") # 갖혀있음####
                        print('robot_status:{}'.format(robot_status))  
                        # print(current_pose);print('='*5)
                        pub_stop_destination.publish(current_pose)
                        if robot_status == True:
                            print("Robot stopped!") #2
                            temp_finished = True
                            rospy.set_param('stop_signal',1) #네비게이션 모드 진입
                            break
                        stop_rate.sleep()
            else:
                print("Do nothing") #3
                
            robot_start = False
            robot_status = False
        rate_main_while.sleep()

   
#-------------------------------------------------Main------------------------------------------------
if __name__ == '__main__':
    try:
        #--------------------Initialize node ---------------------
        rospy.init_node('Patrol', anonymous=False)
        #------------------Define global variables-----------------
        global current_pose;global current_mode;global twist                      # 로봇의 움직임 제어에 필요한 객체
        global BOTTOM_LEFT; global BOTTOM_RIGHT; global TOP_LEFT; global TOP_RIGHT# 로봇의 Patrol point 좌표지정

        global robot_status
        global robot_start
        global switch_patrol
        global distance_margin
        #---------------------Define variables--------------------
        twist = Twist()                  # 로봇의 제자리 회전을 위해 필요
        current_mode = 0                 # 현재 동작 모드 실시간 update
        current_pose = PoseStamped()     # 현재 로봇의 위치 실시간 update
        
        # BOTTOM_LEFT = [-2,0.5]; BOTTOM_RIGHT = [-2,-0.5]; TOP_LEFT = [0.5,0.5]; TOP_RIGHT = [0.5,-0.5] # Patrol point 
        #BOTTOM_LEFT = [-2,3]; BOTTOM_RIGHT = [0,0]; TOP_LEFT = [-5,-3]; TOP_RIGHT = [4,-2] # Patrol point 
        BOTTOM_LEFT = [6,0]; BOTTOM_RIGHT = [0,0]; TOP_LEFT = [4,0]; TOP_RIGHT = [2,0] # Patrol point 
        

        robot_start = False
        robot_status = False
        distance_margin = 0.1            # 현재위치와 Patrol point 사이의 허용오차
        rate_temp= rospy.Rate(10)
        rate_main_while = rospy.Rate(2)  # while문 속도 제어를 위한 변수
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
        rospy.Subscriber('/real_pose', PoseStamped, current_pose_callback)
        rospy.Subscriber('/move_base/result',MoveBaseActionResult,status_callback)
        # ------------------Configuration varaibles------------------
        angular_velocity = -0.1 ## 속도 수정(-0.1)
        rotate_time_second = 5.0
        rospy.set_param('stop_signal',0)
# ---------------------------------------------------------------------------- #
#                     Setup variables & main function call                     #
# ---------------------------------------------------------------------------- #
        set_switch_patrol()              # 초기 Patrol point 위치 지정
        patrol_mode()                    # Patrol mode initiate

    except rospy.ROSInterruptException:
        pass