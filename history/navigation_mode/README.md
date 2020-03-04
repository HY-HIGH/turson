<img src= https://img.shields.io/badge/build-passing-green > <img src= https://img.shields.io/badge/language-python-blue >  

# ROS Navigation Node
2019~2020 캡스톤 디자인 프로젝트 '자율 안전보조로봇'의 네비게이션 모드 입니다.
<!-- ## 실행 -->
<!-- >roslaunch turson_navigation navigation.launch -->
## 1. Develop environment summary
|Develop environment||
|------|------|
|OS|Ubuntu 16.04|
|ROS|kinetic|
|Languae|python|
|MCU|OpenCR, Nvidia Jetson Tx2|
|Robot|Turtlebot3 기반|
  
## 2. Packages 
    "Turson" 은  로봇의 이름입니다.
|ROS Package|summary|
|------|------|
|navigation_mode.py|핵심 노드, 최종 목적지 퍼블리시|
|move_turson.py|로봇의 동작 노드|
|turson_box_data.py|박스 정보 퍼블리시|


## 3. Details 
### rqt_graph
<!-- <img src = ./img/rosgraph.png>  -->
<img src = ./img/rosgraph_color.png>
### navigation_mode.py

|Parameter|0|1|2|
|------|------|------|------|
|/mode|patrol mode|navigation mode|centrallize mode|
|/navigation_status|navigation deactivate|navigation activate||

    Parameter /mode 와 /navigation_status 가 모두 1이 되었을때 목적지 좌표를 계산하여 퍼블리시 한다.
  
---  


### move_turson.py
    위의 노드에서 받은 토픽으로 목적지를 찍어 네비게이션 한다.  
  
---

### turson_box_data.py
    박스가 여러개 일때 가장 큰 박스 사이즈를 가지는 것을 퍼블리시 한다.
> 다음 커스텀 메시지가 필요합니다.
```msg
    float32 x_mid
    float32 y_mid
    float32 box_size
    int32 box_count

``` 
---
 
### status 정보
```
status

uint8 PENDING         = 0    The goal has yet to be processed by the action server
uint8 ACTIVE          = 1    The goal is currently being processed by the action server
uint8 PREEMPTED       = 2    The goal received a cancel request after it started executing
                               and has since completed its execution (Terminal State)
uint8 SUCCEEDED       = 3    The goal was achieved successfully by the action server (Terminal State)
uint8 ABORTED         = 4    The goal was aborted during execution by the action server due
                                to some failure (Terminal State)
uint8 REJECTED        = 5    The goal was rejected by the action server without being processed,
                                because the goal was unattainable or invalid (Terminal State)
uint8 PREEMPTING      = 6    The goal received a cancel request after it started executing
                                and has not yet completed execution
uint8 RECALLING       = 7    The goal received a cancel request before it started executing,
                                but the action server has not yet confirmed that the goal is canceled
uint8 RECALLED        = 8    The goal received a cancel request before it started executing
                                and was successfully cancelled (Terminal State)
uint8 LOST            = 9    An action client can determine that a goal is LOST. This should not be
                                sent over the wire by an action server
