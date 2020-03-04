# ISSUE : TF /odom 의 뒤틀림으로 인한 현재 위치 오차   
![Rqt_graph](/image/frames.png)

## DWA (dynamic window approach)_

## AMCL(adaptive monte carlo localiztion
로봇의 위치 추정 방법
## /tf
로봇의 센서는 로봇의 하드웨어적 구성에 따라 위치가 상대적으로 바뀌기 때문에  
transformation 상대 좌표 변환을 해준다.  

즉 로봇의 위치로부터 좌표상 센서가 얼마만큼 떨어져있는지 알려준다.  
ex) odom -> base_footprint -> base_link -> base_scan
## /map

## /base_link


## /odom
로봇의 오도메트리 정보는 local path planning 에서 사용
장애물 회피나 local path planning생성

## /scan
센서로 부터 측정된 거릿값 


