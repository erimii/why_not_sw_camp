# -*- coding: utf-8 -*-

'''
game -> __init__.py

__init__.py 용도
해당 디렉터리(폴더) -> 패키지의 일부임을 명시
패키지의 버전 설정: VERSION = 3.5
패키지의 초기화 코드 작성
'''

from .graphic.render import render_test

VERSION = 3.5

def print_version_info():
    print("print_version_info {VERSION}")
    

# 패키지 초기화 작업
print('game 패키지 초기화 중...')
