# SLAM Navigation
## Cartographer compile
- 참고 http://emanual.robotis.com/docs/en/platform/turtlebot3/slam/#ros-1-slam  

> sudo apt-get install ninja-build libceres-dev libprotobuf-dev protobuf-compiler libprotoc-dev  

>cd ~/catkin_ws/src  

> git clone https://github.com/googlecartographer/cartographer.git  


> git clone https://github.com/googlecartographer/cartographer_ros.git  

> cd ~/catkin_ws    

> src/cartographer/scripts/install_proto3.sh    

> rm -rf protobuf/  

> rosdep install --from-paths src --ignore-src -r -y --os=ubuntu:xenial  

> catkin_make_isolated --install --use-ninja  


## turtlebot3_lds_2d 수정
- turtlebot3 패키지의 turtlebot3_lds_2d.lua 파일 
- tracking_frame = 'base_footprint' 로 수정
- 원래는 "imu_link"
```lua
    options = {
  map_builder = MAP_BUILDER,
  trajectory_builder = TRAJECTORY_BUILDER,
  map_frame = "map",
  tracking_frame = 'base_footprint', -- imu_link, If you are using gazebo, use 'base_footprint' (libgazebo_ros_imu's bug)s
  published_frame = "odom",
  odom_frame = "odom",
  provide_odom_frame = false,
  publish_frame_projected_to_2d = false,
  use_odometry = true,
  use_nav_sat = false,
  use_landmarks = false,
  num_laser_scans = 1,
  num_multi_echo_laser_scans = 0,
  num_subdivisions_per_laser_scan = 1,
  num_point_clouds = 0,
  lookup_transform_timeout_sec = 0.2,
  submap_publish_period_sec = 0.3,
  pose_publish_period_sec = 5e-3,
  trajectory_publish_period_sec = 30e-3,
  rangefinder_sampling_ratio = 1.,
  odometry_sampling_ratio = 0.1,
  fixed_frame_pose_sampling_ratio = 1.,
  imu_sampling_ratio = 0.1,
  landmarks_sampling_ratio = 1.,
}

```

## Move base 노드 추가
- turtlebot3_slam 패키지의 turtlebot3_slam.launch 파일
```xml
<include file="$(find turtlebot3_navigation)/launch/move_base.launch">
    <arg name="model" value="$(arg model)" />
  </include>

```

## 실행방법

>roslaunch turtlebot3_gazebo turtlebot3_world.launch  
>roslaunch turtlebot3_gazebo turtlebot3_house.launch

> roslaunch turtlebot3_slam turtlebot3_slam.launch slam_methods:=cartographer  

>roslaunch turtlebot3_teleop turtlebot3_teleop_key.launch    

>rosrun map_server map_saver -f ~/map


## ISSUE
[ WARN] [1585087556.049474980, 262.236000000]: The robot's start position is off the global costmap. Planning will always fail, are you sure the robot has been properly localized?