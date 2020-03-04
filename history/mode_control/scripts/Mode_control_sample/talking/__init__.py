#-*- coding: utf-8 -*-
# 한글 주석을 사용하기 위해서는 위의 주석이 반드시 필요합니다.

# 스크립트의 효율적인 관리를 위해 디렉토리를 구분할 필요가 있습니다.
# 디렉토리 혹은 폴더를 파이썬에서는 패키지라고 부르며, 각각의 파이썬 파일(.py)을 모듈이라고 부릅니다.
# 어떤 디렉토리가 패키지로 인식되기 위해서는 __init__.py가 패키지 내부에 반드시 존재해야 하며
# __init__.py에서는 각 모듈에서 import되어야 하는 함수나 클래스를 정의해주는 작업을 해야 합니다.
# 이후 외부 스크립트에서 이 패키지를 import하고 싶다면 해당 스크립트에서 "import 패키지명" 을 입력해주시면 됩니다.
# 예를 들어 from .listener import listener 을 보면, 
# from .listener  = 현재디렉토리(talking/)에서 listener.py로 부터
# import listener = 함수 listener를 import하겠다는 뜻이 됩니다.

#from .talker import talker
#from .talker2 import talker2

from .listener import listener 

