# do_it.py

import game.sound.echo
game.sound.echo.echo_test()

from game.sound.echo import echo_test

import game.sound.echo as ec
ec.echo_test()

import game
print(game.VERSION)
game.print_version_info()

game.render_test()

from game.sound import *
echo.echo_test()



'''
예외처리
-> 오류가 발생했을 경우,
-> 방지
-> 특히 사용자 화면에서 오류 처리

try :
    할 일들
except:
    할 일들 중 오류 발생시

try :
    할 일들
except 오류클래스명 as 변수명:
    할 일들 중 오류 발생시
    변수를 통해 사용자에게 오류 전달 가능
  
try :
    할 일들
finally:
    try가 일을 마치면..
    
try: 
    할 일들(0으로 나누기, index오류)
except 0으로 나누기:
except index 오류:
except:
    
try: 
    할일들
except:
    오류가 발생했을 경우
else:
    오류가 발생하지 않았을 경우
'''


try:
    f = open('new.txt', 'r')

finally:
    f.close()

# ------------------------------
try:
    f = open('new.txt', 'r')
except:
    print('file not found,,,')

# ------------------------------
try:
    a = [1,2,3,4]
    print(a[3])
    4/0
except ZeroDivisionError as e:
    print(e)
except IndexError as e:
    print(e)

# ------------------------------
try:
    age = int(input('나이를 입력하세요: '))
except:
    print('정수 입력해')
else:
    if age <= 18:
        print('미성년자는 안돼요')
    else:
        print('환영')
# ------------------------------

class Bird:
    def fly(self):
        raise NotImplementedError
        # 꼭 작성해야하는 부분이 구현되지 않았을경우 일부로 오류 발생

class Eagle(Bird):
    def fly(self):
        print('very fast')

eagle = Eagle()
eagel.fly()

# ------------------------------
class MyError(Exception):
    def __str__(self):
        return '허용되지 않는 별명'

def say_nick(nick):
    if nick == '바보':
        raise MyError()
    print(nick)

try:
    say_nick('천사')
    say_nick('바보')
except MyError as e:
    print(e)













