# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 08:57:12 2025

@author: Admin
"""

import urllib.request
from soynlp import DoublespaceLineCorpus
from soynlp.word import WordExtractor

urllib.request.urlretrieve("https://raw.githubusercontent.com/lovit/soynlp/master/tutorials/2016-10-20.txt", filename="2016-10-20.txt")

# 훈련 데이터를 다수의 문서로 분리
corpus = DoublespaceLineCorpus("2016-10-20.txt")
len(corpus) # 30091

# 상위 3개의 문서만 출력
i=0
for document in corpus:
    if len(document) > 0:
        print(document)
        i += 1
    if i==3:
        break
    
# WordExtraactor.extract()를 통해 전체 코퍼스에 대해 단어 점수표를 계산
# 응집 확률: 내부 문자열이 얼마나 응집하여 자주 등장하는지 판단하는 척도
#            문자열을 문자 단위로 분리하여 내부 문자열을 만드는 과정
#            왼쪽 부터 순서대로 문자를 추가하면서 각 문자열이 주어졌을 때
#            그 다음 문자가 나올 확률을 계산하여 누적곱을 한 값

# WordExtractor를 사용하여 단어 학습
word_extractor = WordExtractor()
word_extractor.train(corpus)
word_score_table = word_extractor.extract()
'''
all cohesion probabilities was computed. # words = 223348
all branching entropies was computed # words = 361598
all accessor variety was computed # words = 361598
'''

# '반포한'의 응집확률 계산
word_score_table['반포한'].cohesion_forward
# 0.08838002913645132
word_score_table['반포한강'].cohesion_forward
# 0.19841268168224552
word_score_table['반포한강공'].cohesion_forward
# 0.2972877884078849
word_score_table['반포한강공원'].cohesion_forward
# 0.37891487632839754
word_score_table['반포한강공원에'].cohesion_forward
# 0.33492963377557666-> 오히려 떨어짐. 즉 반포한강공원이 한 단어일 가능성이 제일 높음.

'''
soynlp의 브랜칭 엔트로피
확률 분포의 엔트로피값을 사용
주어진 문자열에서 얼마나 다음 문자가 등장할 수 있는지 판단하는 척도

브렌칭 엔트로피의 값은 하나의 완성된 단어에 가까워질수록 해당 값이 줄어듬
'''
word_score_table['디스'].right_branching_entropy
# 1.6371694761537934
word_score_table['디스플'].right_branching_entropy
# -0.0 -> 다음에 어떤 문자가 올지 문맥상으로 유추하기 명확하기 때문
word_score_table['디스플레이'].right_branching_entropy
# 3.1400392861792916 ->  디스플레이 다음에 조사나 다른 단어와 같은 다양한 경우가 있기 때문
# 하나의 단어가 끝나면 그 경계부터 다시 브랜칭 엔트로피 값이 증가하게 됨. 
# 이 값으로 단어를 판단하는 것이 가능

'''
soynlp의 L tokenizer
'''
from soynlp.tokenizer import LTokenizer

scores = {word:score.cohesion_forward for word, score in word_score_table.items()}
l_tokenizer = LTokenizer(scores=scores)
l_tokenizer.tokenize("국제사회와 우리의 노력들로 범죄를 척결하자", flatten=False)
'''
[('국제사회', '와'), ('우리', '의'), ('노력', '들로'), ('범죄', '를'), ('척결', '하자')]
'''

'''
최대 점수 토크나이저: MaxScoreTokenizer
띄어쓰기가 되지 않는 문장엣 ㅓ점수가 높은 글자 시퀀스를 순차적으로 찾아내는 토크나이저
'''
from soynlp.tokenizer import MaxScoreTokenizer

maxscore_tokenizer = MaxScoreTokenizer(scores=scores)
maxscore_tokenizer.tokenize("국제사회와우리의노력들로범죄를척결하자")
'''
['국제사회', '와', '우리', '의', '노력', '들로', '범죄', '를', '척결', '하자']
'''

'''
반복되는 문자 정제
ㅋㅋ,ㅎㅎ 등의 이모티콘의 경우
'''
from soynlp.normalizer import *

print(emoticon_normalize('앜ㅋㅋㅋㅋ이영화존잼쓰ㅠㅠㅠㅠㅠ', num_repeats=2))
# 아ㅋㅋ영화존잼쓰ㅠㅠ

print(repeat_normalize('와하하하하하하하하하핫', num_repeats=2))
# 와하하핫

'''
Customized KoNLPy
'은경이는 사무실로 갔습니다.'
['은', '경이', '는', '사무실', '로', '갔습니다', '.']
 -> '은경이'는 하나의 단어이므로 분리하지 말라고 분석기에게 알려주는 것
pip install customized_konlpy
'''

from ckonlpy.tag import Twitter
twitter = Twitter() ## 트위터라는 이름의 분석기 생성
twitter.morphs('은경이는 사무실로 갔습니다.')
# ['은', '경이', '는', '사무실', '로', '갔습니다', '.']
twitter.add_dictionary('은경이', 'Noun')
twitter.morphs('은경이는 사무실로 갔습니다.')
# ['은경이', '는', '사무실', '로', '갔습니다', '.']
# add_dictionary()를 활용해 사전을 커스터마이즈 할 수 있음









































