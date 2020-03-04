
















    # robot_stop_destination_check_cnt = 0      # mode 전환 시 즉각 정지 실패시 추가 추가 정지위치 publish를 위해 선언
    # stop_check_cnt = False

# def stop_check(robot_stop_destination_check_cnt,robot_stop_destination):

# # ---------------------------------------------------------------------------- #
# #                                 Stop checking                                #
# # 모드 전환 후 5회 정상적인 정지가 되었는지 확인
# # 정상적으로 정지가 이루어지지 않는다면 True를 반환
# # 정상적인 정지가 이루어졌거나 stop check 주기가 아닌 경우 False 반환
# # True반환 시 현재위치를 받아들여 재정지 신호 publish
# # ---------------------------------------------------------------------------- #
#     global current_pose
#     global distance_margin
#     if ((robot_stop_destination_check_cnt % 2) == 0 and (robot_stop_destination_check_cnt <= 10)):
#         if(abs(robot_stop_destination.pose.position.x - current_pose.pose.position.x ) > distance_margin or \
#             abs(robot_stop_destination.pose.position.y - current_pose.pose.position.y ) > distance_margin or \
#                 abs(robot_stop_destination.pose.orientation.x - current_pose.pose.orientation.x ) > distance_margin or \
#                     abs(robot_stop_destination.pose.orientation.y - current_pose.pose.orientation.y ) > distance_margin or \
#                         abs(robot_stop_destination.pose.orientation.z - current_pose.pose.orientation.z ) > distance_margin or \
#                             abs(robot_stop_destination.pose.orientation.w - current_pose.pose.orientation.w ) > distance_margin ):
                                    
#             return True
        
#         else:
#             return False
#     else:
#         return False


        # Mode 전환시 이뤄져야 할 작업 설정
        # 0(Patrol 모드) -> 1(Navigation 모드)
        # 1) 현재위치를 robot정지 위치로 지정
        # 2) 즉각 정지를 못할 시 추가 정지 신호 5회 송출을 위해  stop_check_cnt 활성화   
        # if((past_get_param == 0) and (rospy.get_param('mode') == 1)):
        #     # robot_stop_destination = copy.deepcopy(current_pose)
        #     # pub_stop_destination.publish(robot_stop_destination)
        #     # stop_check_cnt = True
        #     for i in range(2)
        #         print("Stop!",i)
        #         twist.linear.x = 0.0; twist.linear.y = 0.0; twist.linear.z = 0.0
        #         twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = 0.0
        #         pub_twist.publish(twist)
        # # # 1(Navigation 모드)가 지속될 때 stop_check_cnt 활성화
        # elif((past_get_param == 1) and (rospy.get_param('mode') == 1)):
        #     stop_check_cnt = True
        # # 1(Navigation 모드)-> 0(Patrol 모드) 전환 시
        # # 1)정지 신호 5회 송출이 필요 없으므로  stop_check_cnt 비활성화
        # # 2)robot_stop_destination는 stop_check_cnt 활성화 이후 몇 번 loop가 실행되었는지 확인
        # else:
        #     stop_check_cnt = False
        #     robot_stop_destination_check_cnt = 0

        # past_get_param = rospy.get_param('mode')
        # pub_mode.publish(rospy.get_param('mode'))

        # # 정지 여부 확인 
        # if(stop_check_cnt == True):
        #     if stop_check(robot_stop_destination_check_cnt,robot_stop_destination) == True:
        #         pub_stop_destination.publish(current_pose)
        #         print("Stop again navigation Finished!!")
        #     else:
        #         pass

        #     robot_stop_destination_check_cnt = robot_stop_destination_check_cnt + 1