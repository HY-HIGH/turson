#  HOW TO RUN
```
작성자 : 황인재
작성일 : 2020.03.05
```
---
## 0. Time Sync 

|요약|코드|설명|
|-----|-----|-----|      
|직접 연결|ntpdate 192.168.0.7 ||  
|동기화 시작|sudo /etc/init.d/ntp start||  
|동기화 중단|sudo /etc/init.d/ntp stop||  
|동기화 확인|ntpq -p||  
  
---
## 1. Robot
### Turson (TurtleBot + Jetson)
- 터미널 4개 
- 4개 모두 모니터링 불필요함
    >ssh nvidia@192.168.0.8 

    > passwd : 9090

    |요약|코드|설명|  
    |-----|-----|-----|
    |로봇|roslaunch turtlebot3_bringup turtlebot3_robot.launch||  
    |네비게이션|roslaunch turtlebot3_navigation turtlebot3_navigation.launch map_file:=$HOME/map.yaml||  
    |카메라 노드|rosrun usb_cam usb_cam_node||  
    |YOLO|roslaunch darknet_ros darknet_ros.launch||  



---
## 2. Remote PC
- 터미널 6개
- 모티터링 항목 5개
    |check|요약|코드|설명|  
    |-----|-----|-----|-----|
    |+|Rviz|roslaunch turson rviz_navigation.launch||  
    ||백 노드|roslaunch turson turson.launch||  
    |+|모드 컨트롤|rosrun turson mode_control||  
    |+|순찰 모드|rosrun turson patrol_mode||  
    |+|네비게이션 모드|rosrun turson navigation_mode||  
    |+|파라미터|rosrun turson parameter_monitor||  



---

## 3.그 외
- 특수 상황
    |요약|코드|설명|  
    |-----|-----|-----|
    |구동|roslaunch turtlebot3_teleop turtlebot3_teleop_key.launch||  
    |GMAPPING|roslaunch turtlebot3_slam turtlebot3_slam.launch slam_methods:=gmapping||  
    |맵 저장|rrosrun map_server map_saver -f ~/map||  
<!-- |YOLO|roslaunch darknet_ros darknet_ros.launch||   -->

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

