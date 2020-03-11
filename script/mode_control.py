#!/usr/bin/env python
#-*- coding: utf-8 -*-

#--------------------------------------import section--------------------------------------
import sys                                          # system shutdown
import rospy                                        # ROS python 모듈
from text_color import color                        # 텍스트 색깔 표시 모듈
from turson.msg  import Box_data                    # 박스 데이터 커스텀 메시지
from geometry_msgs.msg import PoseStamped           # 로봇의 각종 움직임 제어
from darknet_ros_msgs.msg import ObjectCount        # 박스 유무(=사람유무) 수신
from move_base_msgs.msg import MoveBaseActionResult # 로봇의 Navigation goal 도착여부 수신

# ---------------------------------------------------------------------------- #
#                                로봇의 현재 위치를 수신                            #
# ---------------------------------------------------------------------------- #
def current_pose_callback(real_pose):
    global current_pose
    current_pose = real_pose

# ---------------------------------------------------------------------------- #
#                                로봇의 정지여부 수신                              #
# ---------------------------------------------------------------------------- #
def cb_result(result):
    global robot_status
    if result.status.status == 3:
        robot_status = True
    else :
        robot_status = False

# ---------------------------------------------------------------------------- #
#                                   BOX 정보 수신                                #
# BOX의 중심 x좌표 및 사이즈 수신
# ---------------------------------------------------------------------------- #
def cb_bounding_box(image_data):
    global global_x_mid
    global global_box_size

    global_x_mid        =  image_data.x_mid
    global_box_size     =  image_data.box_size
    #print ('box_size :rospy.set_param('nav_once',0)5000 #1.5m

# ---------------------------------------------------------------------------- #
#                             BOX 유무(=사람유무) 수신                             #
# 0 = 사람 없음
# 0 > 사람 있음
# ---------------------------------------------------------------------------- #
def box_count_callback(box_count):
    global global_box_count     
    global_box_count = box_count.count
    # print ("count :" + str(global_box_count))

# ---------------------------------------------------------------------------- #
#                                   로봇 현위치 정지                              #
# ---------------------------------------------------------------------------- #
def stop():
    global robot_status
    while True :
        if robot_status == True:
            break
        else :
            pub_stop_destination.publish(current_pose)
            print(color.PURPLE + "Try to stop!" + color.END)
        # stop 과정 중 사람이 없어진다면: 현재 하던 작업을 멈추고
        if global_box_count == 0 :
            break
        RATE_10.sleep()

def mode_converter():
    # 사람이 검출
    if global_box_count > 0: 
        # 사람이 검출되었다면, 그 사람이 로봇으로 부터 얼마만큼 떨어져 있는지를 확인
        print('Person Detected | Size :{}'.format(global_box_size))
        # 사람이 가까이 있을 때: 갑자기 사람이 로봇에게 가까이 등장했을 때를 의미, 경고음만 내며 Navigation 모드로 전환하지 않는다.
        if  global_box_size > enough_distance: 
            print(color.GREEN + "[Patrol Mode]"+'Too Close, Warning'+ color.END)
        # 사람이 멀리 있을 때: 범위 밖에 존재하므로 순찰임무 계속 수행, 네비게이션을 하지 않는다    
        elif global_box_size < too_far_distance:
            print(color.GREEN + "[Patrol Mode]"+'Too Far, Safe'+ color.END)
        # 사람이 제한범위 이내로 들어왔을 때: 포착된 위치로 가기 위해 Navigation 모드로 전환
        elif (too_far_distance <= global_box_size <= enough_distance) : 
            
            # 현재 위치 정지 작업 실시
            stop()
            # 정지 작업을 마쳤고 여전히 사람이 존재한다면: Navigation mode로 전환
            if global_box_count > 0:
                # 정지완료
                print(color.RED + "="*10 + color.END)
                print(color.RED + "Robot stop!" + color.END)
                print(color.RED + 'Start Approach To Person' + color.END)
                print(color.RED + "="*10 + color.END)
 
                # 위의 과정을 정상적으로 마쳤다면 Navigation 모드 실행           
                rospy.set_param('mode',1) 
                print(color.YELLOW + '[Navigation Mode]: Start'+ color.END)
                while True:
                    print(color.YELLOW + '[Navigation Mode]'+ color.END)
                    if rospy.get_param('mode') == 0 :
                        break
                    else: 
                        pass
                    RATE_10.sleep()
            # 정지 작업 중 사람이 사라진 경우: 70번째 if로 돌아가 모드 전환여부 재확인
            else:
                pass
        # 실행이 되면 안되는 상황[ERROR]
        else:
            print(color.RED + color.BOLD +'[ERROR]' + color.END + 'global_box_size')
            sys.exit()
    # 사람이 검출되지 않음
    else :
        print(color.GREEN + '[Patrol Mode]'+ color.END)

#-------------------------Main------------------------
if __name__ == '__main__':
    try:
    #----Initialize node & Define publisher/subscriber---
        rospy.init_node('mode_controller', anonymous=False)

        rospy.Subscriber('/box_data',Box_data,cb_bounding_box)                      # Person detection 데이터 수신
        rospy.Subscriber('/real_pose', PoseStamped, current_pose_callback)          # 로봇의 현재위치 확인
        rospy.Subscriber('/move_base/result',MoveBaseActionResult,cb_result)        # 목적지 도착 여부 계속 서브스크라이브
        rospy.Subscriber('/darknet_ros/found_object',ObjectCount,box_count_callback)# 박스 유무(=사람유무) 수신    

        pub_stop_destination = rospy.Publisher('set_robot_destination', PoseStamped, queue_size=10)
    #--------------------Setup parameter-----------------
        rospy.set_param('mode',0) # 로봇의 모드값 변환
    #-------------------Define variables-----------------
        global current_pose       # 현재 robot의 위치
        global robot_status
        global DISTANCE_MARGIN    # 정지를 위한 여유 거리
        enough_distance = 75000
        too_far_distance = 25000
        global_x_mid = 0          # Person detection box의 x 좌표의 중앙값
        global_box_size = 0       # Person detection box의 크기값
        robot_status = False      # 로봇의 현재지점 도착여부 수신
        global_box_count = 0      # 박스 유무(=사람유무) 수신
        DISTANCE_MARGIN = 0.1     # 로봇의 목표값과 센서값 오차범위
        RATE_1 = rospy.Rate(1)    # while 반복 속도 제어, 10hz 
        RATE_10 = rospy.Rate(10)  # while 반복 속도 제어, 10hz 
    #----------------Initiate main statement-------------
        print(color.GREEN +'[ok] ' + color.END + 'Mode control initiate' )
        while not rospy.is_shutdown():
            mode_converter()
            RATE_10.sleep()

    except rospy.ROSInterruptException:
        pass
