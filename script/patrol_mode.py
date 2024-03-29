#!/usr/bin/env python
#-*- coding:utf-8 -*-

#---------------------------Import section-----------------------------
import sys
import math
import copy
import time
import rospy 
from text_color import color 
from std_msgs.msg import Int64
from nav_msgs.msg import Odometry
from darknet_ros_msgs.msg import ObjectCount        
from move_base_msgs.msg import MoveBaseActionResult
from geometry_msgs.msg import Vector3,Quaternion,PoseStamped,Twist
from tf.transformations import quaternion_from_euler,euler_from_quaternion  
# ---------------------------------------------------------------------------- #
#                             Initiate patrol mode(검증완료)             
# Patrol mode를 시행하며, 지속적으로 현재의 mode 및 로봇의 위치를 확인하면서 해당 조건에 맞는
# Patrol point와 orientation을 publish
# Navigation 모드에 진입 후에는 지속적으로 복귀 point, 4가지 patrol point 중 최단거리 계산
# Centralizing mode에서는 현위치 정지신호 계속발생, 정지이후에는 더 이상 발생하지 않음
# ---------------------------------------------------------------------------- #
def patrol_mode():
    while True:
        global robot_start
        global robot_status
        global current_pose
        main_mode = rospy.get_param('mode')
        if main_mode == 0 :
            print(color.GREEN + "[Patrol mode]: %d"%rospy.get_param('mode') + color.END)
            is_reached_position()
        elif main_mode == 1:
            print(color.YELLOW + "[Navigation mode]: %d"%rospy.get_param('mode')+ color.END)
            calculate_shortest_distance_between_robot_and_patrol_point()
            robot_start = False
            robot_status = False
        else :
            print(color.RED + "[Wrong mode]: %d"%rospy.get_param('mode') + color.END )
            robot_start = False
            roboat_status = False
            sys.exit()
        RATE.sleep() #10hz

# ---------------------------------------------------------------------------- #
#                      Current position of Robot realtime update(검증완료)                  
# 
# 로봇의 현재좌표를 지속적으로 업데이트
#  - X-Y-Z 좌표 
#  - 로봇의 헤드 방향(Orientation)
# ---------------------------------------------------------------------------- #
def current_pose_callback(real_pose):
    global current_pose
    current_pose = real_pose

# ---------------------------------------------------------------------------- #
#                     Current robot status realtime update(검증완료)                     
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
#                             BOX 유무(=사람유무) 수신                             #
# 0 = 사람 없음
# 0 > 사람 있음
# ---------------------------------------------------------------------------- #
def box_count_callback(box_count):
    global global_box_count     
    global_box_count = box_count.count
    
# ---------------------------------------------------------------------------- #
#                      Assign Patrol point and orientation(검증완료)
# 지정된 patrol point 위치 및 로봇 헤드 방향 지정
# ---------------------------------------------------------------------------- #
def go_patrol_point(x,y):
    global switch_patrol 
    robot_destination = PoseStamped() 

    if (switch_patrol == 0):
        yaw = math.radians(ORIENT[1])   # 두번째 포인트의 방향
    elif (switch_patrol == 1):
        yaw = math.radians(ORIENT[2])   # 세번째 포인트의 방향
    elif (switch_patrol == 2):
        yaw = math.radians(ORIENT[3])   # 네번째 포인트의 방향
    else :
        yaw = math.radians(ORIENT[0])   # 첫번째 포인트의 방향

    robot_orient = Quaternion(*quaternion_from_euler(0,0,yaw))

    robot_destination.pose.position.x = x 
    robot_destination.pose.position.y = y 
    robot_destination.pose.position.z = 0.0
    
    robot_destination.pose.orientation.x = robot_orient.x
    robot_destination.pose.orientation.y = robot_orient.y
    robot_destination.pose.orientation.z = robot_orient.z
    robot_destination.pose.orientation.w = robot_orient.w
    pub_destination.publish(robot_destination)

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
#                    Initialize goal point and patrol point(검증완료)             
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
#                           Switch patrol x,y point(검증완료) 
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
#          calculate_shortest_distance_between_robot_and_patrol_point(검증완료)  #
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
#                               단순 거리계산(검증완료)                             #
# ---------------------------------------------------------------------------- #
def calculate_distance():
    global current_pose
    distance_1 = math.sqrt(math.pow((current_pose.pose.position.x - TOP_LEFT[0]),2)+ math.pow((current_pose.pose.position.y - TOP_LEFT[1]),2))
    distance_2 = math.sqrt(math.pow((current_pose.pose.position.x - TOP_RIGHT[0]),2)+ math.pow((current_pose.pose.position.y - TOP_RIGHT[1]),2))
    distance_3 = math.sqrt(math.pow((current_pose.pose.position.x - BOTTOM_LEFT[0]),2)+ math.pow((current_pose.pose.position.y - BOTTOM_LEFT[1]),2))
    distance_4 = math.sqrt(math.pow((current_pose.pose.position.x - BOTTOM_RIGHT[0]),2)+ math.pow((current_pose.pose.position.y - BOTTOM_RIGHT[1]),2))

    return [distance_1,distance_2,distance_3,distance_4]
# ---------------------------------------------------------------------------- #
#                               Rotating mission                               #
# Patrol point 도착 후 일정시간동안 시계방향으로 turtlebot이 회전하도록 하는 함수
# 회전함으로써 순찰지역의 사각지대를 최소화하기 위함
# 모든 행동을 중지하고 image_centralizing에서 patrol_mode가 해야하는 역할을 수행
# ---------------------------------------------------------------------------- #
def rotating_mission(second):
    time_end = time.time() + second
    while True:
        if rospy.get_param('mode') == 1:
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
        print("[Patrol]: Rotating...")
        RATE.sleep()

def rotate_callibrate():
    global switch_patrol
    global current_pose
    if switch_patrol == 0:
        yaw = math.radians(CALLIBRATE_ORIENT[0])
    elif switch_patrol == 1:
        yaw = math.radians(CALLIBRATE_ORIENT[1])
    elif switch_patrol == 2:
        yaw = math.radians(CALLIBRATE_ORIENT[2])
    else :
        yaw = math.radians(CALLIBRATE_ORIENT[3])

    while True:
        current_quaternion = [current_pose.pose.orientation.x,current_pose.pose.orientation.y,current_pose.pose.orientation.z,current_pose.pose.orientation.w]
        euler = euler_from_quaternion(current_quaternion)
        current_yaw = euler[2] + math.pi

        if abs(current_yaw - yaw) < YAW_MARGIN:
            twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = 0.0
            pub_twist.publish(twist)
            break
        else: # 양수: 반시계방향 회전 | 음수: 시계방향 회전
            twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = angular_velocity
            print("[Patrol]: Rotating...")
            pub_twist.publish(twist)

        if rospy.get_param('mode') == 1:
            break

        RATE.sleep()
# ---------------------------------------------------------------------------- #
#                              Check target point                              #
#  현재위치와 지속적으로 비교하며 patrol point에 도착했는지 확인
#  도착했다면 patrol point 전환
#  도착하지 않았다면 Patrol point로 이동 명령 다시 내림
# ---------------------------------------------------------------------------- #
def is_reached_position():
    global robot_start
    global robot_status
    global current_pose
    global switch_patrol
    global global_box_count
    global x_goal; global y_goal
    error_check = False
    switch_check = False
    # print("\n=======================")
    # print("robot_start",robot_start)
    # print("robot_status",robot_status)
    # print("=======================")
    if rospy.get_param('mode') == 1: # Navigation mode일때는 해당함수 더 이상 수행하지 말 것
        print(color.YELLOW + '[Navigation] Activated' + color.END)
    elif rospy.get_param('mode') == 0:
        if (robot_start == False) and (robot_status == False): # 출발도 도착도 안했다면
            position_timer(POSITION_TIME) # 현재 위치 업로드 
            past_position = copy.deepcopy(current_pose.pose.position) # 현재위치 스냅샷
            while True:
                # 움직여서 벗어났다면 더이상 go_patrol_point 함수를 실행하지 않는다.
                if abs(past_position.x - current_pose.pose.position.x) > (DISTANCE_MARGIN) or \
                    abs(past_position.y - current_pose.pose.position.y) > (DISTANCE_MARGIN):
                    print(color.GREEN + "\n================" + color.END)
                    print(color.GREEN + "[Patrol]: Start!" + color.END)
                    print(color.GREEN + "================\n" + color.END)
                    break
                # 과거의 위치와 현재의 위치가 거의 유사한 경우 go_patrol_point를 지속적으로 publish한다.
                else:
                    # 현재와 목표위치와의 차이값이 거의 유사하거나 같다 = 목적지 지정 오류
                    if error_check == False:
                        if abs(x_goal - current_pose.pose.position.x) < DISTANCE_MARGIN and \
                            abs(y_goal - current_pose.pose.position.y) < DISTANCE_MARGIN:
                            if switch_check == False:
                                switch_patrol_point()
                                error_check = True
                            else:
                                pass
                        else:# 현재위치와 목표위치가 다르므로 error는 발생하지 않는다.
                            error_check = True
                    # while을 계속 돌면서 수행될 곳, 아무일도 없이 넘어가야 함.    
                    else:
                        go_patrol_point(x_goal,y_goal)
                        print("[Patrol]: Get ready for starting...")
                        print("Error_stack: {}".format(is_reached_position.error_stack))
                        is_reached_position.error_stack += 1
                        if is_reached_position.error_stack > ERROR_THRESHEHOLD:
                            switch_patrol_point()
                            is_reached_position.error_stack = 0
                # 출발 대기 중이더라도 Navigation mode로 전환되면 현재 작업 중단
                if rospy.get_param('mode') == 1:
                    break
                RATE.sleep()
            
            robot_start = True
            error_check = False
            switch_check = False
            
        elif robot_start == True and robot_status == False : # 출발은 했는데 도착은 못했으면
            print("[Patrol]: Turtlebot on the move...")
    
        elif robot_start == True and robot_status == True: # 출발도 했고 도착도 했다면
            robot_start = False
            robot_status = False
            if rospy.get_param('mode') == 1:
                pass
            else:
                rotating_mission(rotate_time_second)
            if rospy.get_param('mode') == 1:
                pass
            else:
                rotate_callibrate()

            print(color.GREEN +'='*30 + color.END)
            print(color.GREEN + "[Patrol]: Rotation finished!!!"+ color.END)
            print(color.GREEN + '='*30 + color.END + '\n')
            # 사람이 존재하지 않으면
            if global_box_count == 0 or rospy.get_param('mode') == 1:
                pass
            else:
                switch_patrol_point()

        else: # 205번째 상황 중간에 종료된 것이므로 다시 순찰모드로 전환해야 함 switch_patrol의 오류상황은 166번째 상황에서 처리(robot_start = False, robot_status = True)
            robot_start  =  False
            robot_status =  False
    else:
        print(color.RED + "[Wrong mode]: %d"%rospy.get_param('mode') + color.END )
        sys.exit()
            

#(검증완료)
def set_patrol_coordinate():
    global BOTTOM_LEFT; global BOTTOM_RIGHT; global TOP_LEFT; global TOP_RIGHT
    global ORIENT;global CALLIBRATE_ORIENT
    BOTTOM_LEFT = [-1,-3]; BOTTOM_RIGHT = [-1,0]; TOP_LEFT = [2,-3]; TOP_RIGHT = [2,0] # 4공학관 5층
    ORIENT = [360,270,180,90];CALLIBRATE_ORIENT = [90,360,270,180]
    # patrol_select = int(input("[장소를 입력해주세요]\n1)Turtlebot \n2)1공학관 3층 \n3)4공학관 5층\n:"))

    # if patrol_select == 1:
    #     BOTTOM_LEFT = [-2,0.5]; BOTTOM_RIGHT = [-2,-0.5]; TOP_LEFT = [0.5,0.5]; TOP_RIGHT = [0.5,-0.5] # Simulation
    #     ORIENT = [90,180,270,360]; CALLIBRATE_ORIENT = [270,360,90,180]
    # elif patrol_select == 2:
    #     BOTTOM_LEFT = [-2,3]; BOTTOM_RIGHT = [0,0]; TOP_LEFT = [-5,-3]; TOP_RIGHT = [4,-2] # 1공학관 3층
    #     ORIENT = [135,45,315,315]; CALLIBRATE_ORIENT = [315,225,135,135]
    # elif patrol_select == 3:
    #     BOTTOM_LEFT = [-1,-3]; BOTTOM_RIGHT = [-1,0]; TOP_LEFT = [2,-3]; TOP_RIGHT = [2,0] # 4공학관 5층
    #     ORIENT = [360,270,180,90];CALLIBRATE_ORIENT = [90,360,270,180]
    # else:
    #     print(color.RED + "잘못 입력하셨습니다. 프로그램을 종료합니다" + color.END)
    #     sys.exit()

    # print("\n=======================")
    # print("BOTTOM_LEFT:",BOTTOM_LEFT)
    # print("BOTTOM_RIGHT:",BOTTOM_RIGHT)
    # print("TOP_LEFT:",TOP_LEFT)
    # print("TOP_RIGHT:",TOP_RIGHT)
    # print("ORIENT:",ORIENT)
    # print("CALLIBRATE_ORIENT:",CALLIBRATE_ORIENT)
    # print("=======================")
    

    # confirm = raw_input("입력값이 정확한지 확인해주세요.(y/n)")
    # if confirm == 'y':
    #     print(color.GREEN + "입력이 확인되었습니다. 순찰모드를 실행합니다." + color.END)
    # else:
    #     print(color.RED +"입력 확인이 올바르지 않습니다. 프로그램을 종료합니다." + color.END)
    #     sys.exit()

#----------------------------------------------Main(검증완료)---------------------------------------------
if __name__ == '__main__':
    try:
        #--------------------Initialize node ---------------------
        rospy.init_node('Patrol', anonymous=False)
        #------------------Define global variables-----------------
        global POSITION_TIME
        global ROTATE_MARGIN
        global DISTANCE_MARGIN
        global ORIENT; global CALLIBRATE_ORIENT
        global BOTTOM_LEFT; global BOTTOM_RIGHT; global TOP_LEFT; global TOP_RIGHT# 로봇의 Patrol point 좌표지정

        global robot_start
        global robot_status
        global switch_patrol
        global global_box_count
        global current_pose; global twist                      # 로봇의 움직임 제어에 필요한 객체
        #---------------------Define variables--------------------
        POSITION_TIME = 0.5               # 출발 전 현재위치 업로드 시간[sec]
        YAW_MARGIN = 0.3                  # 회전 멈춤위치에 대한 yaw값 기준
        DISTANCE_MARGIN = 0.1             # 현재 위치와 Patrol point 사이의 허용 오차
        RATE = rospy.Rate(10)
        ERROR_THRESHEHOLD = 100 # int(input("ERROR_THRESHEHOLD값 입력(Default = 150): "))

        twist = Twist()                  # 로봇의 제자리 회전을 위해 필요
        current_pose = PoseStamped()     # 현재 로봇의 위치 실시간 update
        robot_start = False
        robot_status = False
        global_box_count = 0
        is_reached_position.error_stack = 0
        #---------------------Set publisher & subscriber----------
        # 3 Publisher: 
        #   1) Twist:turtlebot 제자리 회전을 위해 위해 필요
        #   2) Navigation: Patrol point 위치로 이동하기 위해 필요
        #   3) Stop Navigation: 정지 위치 Navigationing을 하기 위해 필요
        # 2 Subscriber:
        #   1) current_pose: 로봇의 현재 위치를 알기 위해 필요
        #   2) status_callback: 도착여부를 알기위해 필요
        pub_twist = rospy.Publisher('cmd_vel', Twist, queue_size=10)
        pub_destination = rospy.Publisher('set_robot_destination', PoseStamped, queue_size=10)

        rospy.Subscriber('/real_pose', PoseStamped, current_pose_callback)
        rospy.Subscriber('/move_base/result',MoveBaseActionResult,status_callback)
        rospy.Subscriber('/darknet_ros/found_object',ObjectCount,box_count_callback)

        # ------------------Configuration varaibles------------------
        angular_velocity = -0.1
        rotate_time_second = 5.0
# ---------------------------------------------------------------------------- #
#                     Setup variables & main function call                     #
# ---------------------------------------------------------------------------- #
        set_patrol_coordinate() 
        set_switch_patrol()     # 초기 Patrol point 위치 지정
        patrol_mode()           # Patrol mode initiate

    except rospy.ROSInterruptException:
        print(color.RED + "[Patrol_mode] Fail & system exit" + color.END)
        sys.exit()