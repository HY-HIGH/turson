#  구동 방법 정리
```
작성자 : 황인재
작성일 : 2020.01.10
```

## 0. roscore
> roscore

---
## 1. Jetson 에 접속 
robot
>ssh nvidia@192.168.0.8 

> passwd : 9090
## 2. Bringup 노드 실행
>roslaunch turtlebot3_bringup turtlebot3_robot.launch

---

## 3.Slam 및 Navigation
* 구동 확인 (teleop-key)
    >roslaunch turtlebot3_teleop turtlebot3_teleop_key.launch
* Slam Gmapping 맵 만들기
    >roslaunch turtlebot3_slam turtlebot3_slam.launch slam_methods:=gmapping
* 맵 저장
    >rosrun map_server map_saver -f ~/map
* 네비게이션
    >roslaunch turtlebot3_navigation turtlebot3_navigation.launch map_file:=$HOME/map.yaml 
---
## 4. Tunning
>http://emanual.robotis.com/docs/en/platform/turtlebot3/navigation/#run-navigation-nodes 
* inflation_radius
    >turtlebot3_navigation/param/costmap_common_param_$(model).yaml
* cost_scaling_factor
    >turtlebot3_navigation/param/costmap_common_param_$(model).yaml
* max_vel_x
* min_vel_x
* max_trans_vel
* min_trans_vel
* max_rot_vel
* min_rot_vel
* acc_lim_x
* acc_lim_theta
* xy_goal_tolerance
* yaw_goal_tolerance
* sim_time

