# NTP 이용 서버 시간 동기화 방법 (off line)
참고 : http://bahndal.egloos.com/589083
## 1. NTP 설치 및 설정
- Server : 192.168.0.7 (pc)
- Client : 192.168.0.8 (robot)
> sudo apt-get update  
> sudo apt-get install ntp
### 루트 권한 
> sudo -s   
### 파일 수정
> gedit /etc/ntp.conf  
- Server의 경우 ntp.cof 폴더 내의 server.conf 참조    
- Client의 경우 ntp.cof 폴더 내의 server.conf 참조  

## 2. 실행 방법
### PC로 직접 연결
> ntpdate 192.168.0.7 
### 서버와 동기화
> sudo /etc/init.d/ntp start
### 서버와 동기화 중단
> sudo /etc/init.d/ntp stop

### 동기화 확인
> ntpq -p   

|항목|설명|
|-----|-----|  
|remote|NTP 서버 주소|
|refid|NTP 서버가 시간를 가져오는 NTP 서버 주소|
|st|Stratum: NTP 서버의 계층, 최상위 계층인 원자시계는 0, 2는 최상위 계층으로부터 2단계 거친 NTP 서버라는 뜻|
|when|	마지막으로 시간을 조회한 시간(second)|
|poll	|시간 조회 주기(second)|
|reach	|NTP 서버와 통신 성공 여부를 최근 8회까지 저장된 값(8진수). 377은 8회 모두 성공|
|delay|NTP 서버와 통신 지연 시간(millisecond)|
|offset|NTP 서버와의 시간차(millisecond)|
|jitter|NTP 서버와의 시간차간의 차이(millisecond)|



## 3. 수정 부분 설명
> 주석 처리 : 로컬 서버를 이용하기 때문에 인터넷 서버는 모두 주석 처리  
```conf
#pool 0.ubuntu.pool.ntp.org iburst  
#pool 1.ubuntu.pool.ntp.org iburst  
#pool 2.ubuntu.pool.ntp.org iburst  
#pool 3.ubuntu.pool.ntp.org iburst  
#pool ntp.ubuntu.com
```

