# -*- coding: utf-8 -*-
"""
Created on Thu Mar  6 11:21:08 2025

@author: Admin
"""

'''
텍스트 전처리(text preprocessing): 텍스트를 사전에 처리하는 작업

1. 토큰화(tokenization)
2. 정제(cleaning) and 정규화(normalization)
3. 어간 추출 and 표재어 추출
4. 불용어(stopword)
6. 정수 인코딩(integer encoding)
7. 패딩(padding)
8. 원 핫 인코딩(one-hot encoding)
9. 데이터의 분리(splitting data)
10. 한국어 전처리 패키지(texy preprocessing tools for korean text)
'''

'''
1. 토큰화(tokenization): token 단위로 나누는 작업.
단어 토큰화(word tokenization): 단어 외에도 단어구, 의미를 갖는 문자열 포함됨
구두점: 마침표, 쉽표, 물음표, 새미콜론, 느낌표 등과 같은 기호
토큰화 기준을 생각해야됨.

고려사항
1. 구두점이나 특수 문자를 단순 제외해서는 안된다
    - 마침표와 같은 경우는 문장의 경계를 알 수 있는데 도움이 됨
    - 단어 자체에 구두점을 갖고 있는 경우가 있음
    - 특수문자의 달러나 슬래시(날짜)
    - 숫자 사이에 콤마가 들어가는 경우
    
2. 줄임말과 단어 내에 띄어쓰기가 있는 경우
    - 영어권 언어의 '는 압축된 단어
    - new york, rock n roll 이라는 단어
'''
from nltk.tokenize import word_tokenize
from nltk.tokenize import WordPunctTokenizer
from tensorflow.keras.preprocessing.text import text_to_word_sequence
import nltk

nltk.download('punkt_tab')

text1="Don't be fooled by the dark sounding name, Mr. Jone's Orphanage is as cheery as cheery goes for a pastry shop."

# word_tokenize
print(f'word tokenization: {word_tokenize(text1)}')
'''
word tokenization: ['Do', "n't", 'be', 'fooled', 'by', 'the', 'dark', 'sounding', 'name', ',', 'Mr.', 'Jone', "'s", 'Orphanage', 'is', 'as', 'cheery', 'as', 'cheery', 'goes', 'for', 'a', 'pastry', 'shop', '.']
'''

# WordPunctTokenizer
print(f'word tokenization2: {WordPunctTokenizer().tokenize(text1)}')
'''
word tokenization2: ['Don', "'", 't', 'be', 'fooled', 'by', 'the', 'dark', 'sounding', 'name', ',', 'Mr', '.', 'Jone', "'", 's', 'Orphanage', 'is', 'as', 'cheery', 'as', 'cheery', 'goes', 'for', 'a', 'pastry', 'shop', '.']
'''

# text_to_word_sequence
print(f'word tokenization3: {text_to_word_sequence(text1)}')
'''
word tokenization3: ["don't", 'be', 'fooled', 'by', 'the', 'dark', 'sounding', 'name', 'mr', "jone's", 'orphanage', 'is', 'as', 'cheery', 'as', 'cheery', 'goes', 'for', 'a', 'pastry', 'shop']
'''

# 표준 토근화 예제 : penn treebank tokenization
# 1. 하이픈으로 구성된 단어는 하나로 유지
# 2. dont't와 같이 '로 접어가 함께하는 단어는 분리
from nltk.tokenize import TreebankWordTokenizer
tokenizer = TreebankWordTokenizer()
text2 = "Starting a hooe-based restaurant may be on ideal. it doesn't have a food chain or restaurant of their own."
print(f'TreebankWordTokenizer: {tokenizer.tokenize(text2)}')
'''
TreebankWordTokenizer: ['Starting', 'a', 'hooe-based', 'restaurant', 'may', 'be', 'on', 'ideal.', 'it', 'does', "n't", 'have', 'a', 'food', 'chain', 'or', 'restaurant', 'of', 'their', 'own', '.']
'''


# 문장 토큰화(sentence tokenization)
from nltk.tokenize import sent_tokenize

text3 = "His barber kept his word. But keeping such a huge secret to himself was driving him crazy. Finally, the barber went up a mountain and almost to the edge of a cliff. He dug a hole in the midst of some reeds. He looked about, to make sure no one was near."
print(f'sentence tokenization1: {sent_tokenize(text3)}')
'''
sentence tokenization1: ['His barber kept his word.', 'But keeping such a huge secret to himself was driving him crazy.', 'Finally, the barber went up a mountain and almost to the edge of a cliff.', 'He dug a hole in the midst of some reeds.', 'He looked about, to make sure no one was near.']
'''

text4 = "I am actively looking for Ph.D. students. and you are a Ph.D student."
print(f'sentence tokenization2: {sent_tokenize(text4)}')
'''
sentence tokenization2: ['I am actively looking for Ph.D. students.', 'and you are a Ph.D student.']
'''

'''
한국어 토근화 어려움
띄어쓰기 단위가 되는 단위를 '어절'
같은 단어임에도 다른 조사가 같어 다른 단어로 인식될 수 있음.
그, 그에게, 그를, 그와, 그는 등등

한국어 토큰화에서는 형태소(뜻을 가진 가장 작은 말의 단위)란 개념 이해 필요
자립 형태소: 명사, 대명사, 수사, 관형사, 부사, 감탄사 등
의존 형태소: 다른 형태소와 결합돼서 사용됨. 접사, 어미, 조사, 어간

예) 루비가 책을 읽었다
['루비가', '책을', '읽었다']

형태소 단위로 분해
    자립 형태소: 루비, 책
    의존 형태소: -가, -을, 읽-, -었-, -다

한국어는 수많은 코퍼스에서 띄어쓰기가 무시되는 경우가 많아 자연어 처리가 어려워짐
'''

'''
품사 태깅 (part-of-speech tagging)
- 표기는 같지만 품사에 따라 단어의 의미가 달라짐
- '못': 명사로는 screw 의미, 부사로서는 '못 먹는다' 등 동작 동사 할 수 없다는 의미

따라서 단어의 의미를 제대로 파악하기 위해서는
해당 단어가 어떤 품사로 쓰였는지 보는 것이 중요

결론: 단어 토큰화 과정에서 각 단어가 어떤 품사로 쓰였는지 구분해놓는 작업
'''

# KLTK와 KoNLPy를 이용한 영어, 한국어 토큰화
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
text4 = "I am actively looking for Ph.D. students. and you are a Ph.D student."
tokenized_sentence = word_tokenize(text4)
print(f'word tokenization: {tokenized_sentence}')
'''
word tokenization: ['I', 'am', 'actively', 'looking', 'for', 'Ph.D.', 'students', '.', 'and', 'you', 'are', 'a', 'Ph.D', 'student', '.']
'''

from konlpy.tag import Okt
from konlpy.tag import Kkma

okt = Okt()
kkma = Kkma()

text5='열심히 코딩한 당신, 연휴에는 여행을 가라'
# okt
print(f'okt 형태소 분석: {okt.morphs(text5)}')
'''
okt 형태소 분석: ['열심히', '코딩', '한', '당신', ',', '연휴', '에는', '여행', '을', '가라']
'''
print(f'okt 품사 태깅: {okt.pos(text5)}')
'''
okt 품사 태깅: [('열심히', 'Adverb'), ('코딩', 'Noun'), ('한', 'Josa'), ('당신', 'Noun'), (',', 'Punctuation'), ('연휴', 'Noun'), ('에는', 'Josa'), ('여행', 'Noun'), ('을', 'Josa'), ('가라', 'Noun')]
'''
print(f'okt 명사 추출: {okt.nouns(text5)}')
'''
okt 명사 추출: ['코딩', '당신', '연휴', '여행', '가라'] -> '가라'는 명사 아닌데?
'''
# kkma
print(f'kkma 형태소 분석: {kkma.morphs(text5)}')
'''
kkma 형태소 분석: ['열심히', '코딩', '하', 'ㄴ', '당신', ',', '연휴', '에', '는', '여행', '을', '가라']
'''
print(f'kkma 품사 태깅: {kkma.pos(text5)}')
'''
kkma 품사 태깅: [('열심히', 'MAG'), ('코딩', 'NNG'), ('하', 'XSV'), ('ㄴ', 'ETD'), ('당신', 'NP'), (',', 'SP'), ('연휴', 'NNG'), ('에', 'JKM'), ('는', 'JX'), ('여행', 'NNG'), ('을', 'JKO'), ('가라', 'VV')]
'''
print(f'kkma 명사 추출: {kkma.nouns(text5)}')
'''
kkma 명사 추출: ['코딩', '당신', '연휴', '여행'] ->kkma는 명사 추출 잘 됨!
'''


'''
2. 정제(cleaning) and 정규화(normalization)
토큰화(코퍼스에서 용도에 맞게 토큰 분류하는 작업) 작업 전, 후로 진행

정제: 코퍼스로부터 노이즈 데이터를 제거
정규화: 표현 방법이 다른 단어들을 통합시켜 같은 단어로 만드는 작업

정제 작업
    1. 토큰화 작업 전에 토큰화 작업에 방해되는 부분들 배제 시킴
    2. 토큰화 작업 이후에는 여전히 남아있는 노이즈 제거하기위해 지속적으로 이루어짐
    3. 완벽한 정제는 어려움. 실무에서는 합의점을...

1. 규칙에 기반한 표기가 다른 단어들의 통합
    예) USA, US 는 같은 의미. 하나의 단어로 정규화
2. 대, 소문자 통합. 대소문자가 구분되어야 하는 경우(US-미국/us-우리, 회사명, 사람이름) 주의
3. 불필요한 단어((노이즈 데이터))의 제거
    방법:
        1. 불용어 제거
        2. 등장빈도가 적은 단어
        3. 길이가 짧은 단어
'''

'''
3. 어간 추출 and 표재어 추출
- 정규화 기법 중 코퍼스에 있는 단어의 개수를 줄일 수 있는 기법
-BoW(bag of Words) 표현을 사용하는 자연어 처리 문제에서 주로 사용

1. 표제어 추출: 기본 사전형 단어
    - 단어들이 다른 형태를 가지더라도, 그 뿌리 단어를 찾아서 단어의 개수를 줄일 수 있는지 판단
    - 단어의 형태학적 파싱(어간과 접사를 분리하는 작업)을 먼저 진행하는 것
    - 형태소의 종류: 어간(stem)과 접사(affix)
        어간: 단어의 의미를 담고 있는 단어의 핵심 부분
        접사: 단어에 추가적인 의미를 주는 부분
        예) cats: cat(어간)와 -s(접사)로 이루어짐
'''
# NLTK에서는 표제어 추출을 위한 도구 지원.
nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
words = ['policy', 'doing', 'organization', 'have', 'going', 'love', 'lives', 'fly', 'dies', 'watched', 'has', 'starting']
print(f'표제어 추출 전: {words}')
print(f'표제어 추출 후: {[lemmatizer.lemmatize(word) for word in words]}')
'''
표제어 추출 후: ['policy', 'doing', 'organization', 'have', 'going', 'love', 'life', 'fly', 'dy', 'watched', 'ha', 'starting']
'''

'''
dy ha 나온 이유?
본래 단어의 품사 정보를 알아야 정확한 결과 얻을 수 있음
품사 정보를 알려주면 정확하게 출력해줌
'''
lemmatizer.lemmatize('dies', 'v')
lemmatizer.lemmatize('watched', 'v')
lemmatizer.lemmatize('has', 'v')

'''
표제어 추출: 문맥을 고려하여 수행했을 때의 결과는 해당 단어의 품사 정보를 보존
어간 추출: 수행한 결과는 품사 정보가 보존되지 않기 때문에 사전에 존재하지 않는 단어일 경우가 많음
'''

'''
어간 추출 -> 어근/어간/어미/단어/어절
어근:실질적 의미를 나타내는 중심이 되는 부분
    '사랑스럽다'의 '사랑'

어간: 활용어가활용할 때에 변하지 않는 부분
    '가는'의 가-
    '보다', '보니', '보고' 의 보-
어미: 서술격 조사가 활용하여 변하는 부분
    '먹다'의 -다
    '점잖다', '점잖으며', '점잖고' 에서의 -다, -으며, -고
    
단어: 자립적으로 쓸 수 있는 말
    '철수', '일기', '읽은', '같다'
    
어절: 문장을 구성하고 있는 각각의 마디. 띄어쓰기의 단위
    '영희의 일기를' -> 두 개의 어절
'''
# 어간 추출 알고리즘 중 하나인 Porter 알고리즘
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

stemmer = PorterStemmer()
sentence = "This was not the map we found in Billy Bones's chest, but an accurate copy, complete in all things--names and heights and soundings--with the single exception of the red crosses and the written notes."
tokenized_sentence = word_tokenize(sentence)
print(f'어간 추출 후: {[stemmer.stem(word) for word in tokenized_sentence]}')
'''
어간 추출 후: ['thi', 'wa', 'not', 'the', 'map', 'we', 'found', 'in', 'billi', 'bone', "'s", 'chest', ',', 'but', 'an', 'accur', 'copi', ',', 'complet', 'in', 'all', 'thing', '--', 'name', 'and', 'height', 'and', 'sound', '--', 'with', 'the', 'singl', 'except', 'of', 'the', 'red', 'cross', 'and', 'the', 'written', 'note', '.']
어간 추출 수행한 결과는 품사 정보가 보존되지 않기 때문에 사전에 존재하지 않는 단어들도 포함됨

어간 추출 규칙
ALIZE -> AL
ANCE -> 제거
ICAL -> IC

formalize -> formal
allowwance -> allow
electricical -> electric
'''
words=['formalize', 'allowwance','electricical']
print([stemmer.stem(word) for word in words])
'''
['formal', 'alloww', 'electric']
'''

# 어간 추출 알고리즘 중 하나인 lancaster stemmer 알고리즘
from nltk.stem import LancasterStemmer
por = PorterStemmer()
lan = LancasterStemmer()
words = ['policy', 'doing', 'organization', 'have', 'going', 'love', 'lives', 'fly', 'dies', 'watched', 'has', 'starting']
print([por.stem(word) for word in words])
# ['polici', 'do', 'organ', 'have', 'go', 'love', 'live', 'fli', 'die', 'watch', 'ha', 'start']
print([lan.stem(word) for word in words])
# ['policy', 'doing', 'org', 'hav', 'going', 'lov', 'liv', 'fly', 'die', 'watch', 'has', 'start']


'''
한국에서의 어간 추출
체언: 명사, 대명사, 수사
수식언: 관형사, 부사
관계언: 조사
독립언: 감탄사
용언: 동사, 형용사 -> 어간과 어미의 결합임

규칙 활용: 어간이 어미를 취할때 어간의 모습이 일정.
            예) '잡다':'잡-'(어간) + '-다'(어미)
불규칙 활용 : 어간이 어미를 취할때 어간의 모습이 바뀌거나 취하는 어미가 특수한 경우
            예) '듣-, 돕, 곱-, 잇-, 오르-, 노랗-' 등이
                '듣/들-, 돕/도우-, 곱/고우-, 잇/이-, 오르/올-, 노랗/노라-
'''


'''
4. 불용어(stopword)
분석에 도움이 되지 않는 단어 토큰을 제거하는 작업이 필요
'''
from nltk.corpus import stopwords
from nilt.tokenize import word_tokenize
from konlpy.tag import Okt

nltk.download('stopwords')
nltk.download('punkt')

# NLTK에서 불용어 사전 확인 198개
stopword_list = stopwords.words('english')
print(stopword_list[:10])
# ['a', 'about', 'above', 'after', 'again', 'against', 'ain', 'all', 'am', 'an']

example = "Family is not an important thing. It's everything."
stopwords = set(stopwords.words('english'))
word_tokens = word_tokenize(example)
print(word_tokens)
# ['Family', 'is', 'not', 'an', 'important', 'thing', '.', 'It', "'s", 'everything', '.']

result = []
for word in word_tokens:
    if word not in stopwords:
        result.append(word)
print(result)
# ['Family', 'important', 'thing', '.', 'It', "'s", 'everything', '.']

okt = Okt()
example = "고기를 아무렇게나 구우려고 하면 안 돼. 고기라고 다 같은 게 아니거든. 예컨대 삼겹살을 구울 때는 중요한 게 있지."
# 임의의 불용어 사전 만들기
stop_words = "를 아무렇게나 구 우려 고 안 돼 같은 게 구울 때 는"
stop_words = set(stop_words.split(' '))

word_list = okt.morphs(example)
result = []
for word in word_list:
    if word not in stop_words:
        result.append(word)
print(result)
# ['고기', '하면', '.', '고기', '라고', '다', '아니거든', '.', '예컨대', '삼겹살', '을', '중요한', '있지', '.']

'''
5. 정규 표현식(regular expression)
'''



'''
6. 정수 인코딩(integer encoding)
'''



'''
7. 패딩(padding)
'''



'''
8. 원 핫 인코딩(one-hot encoding)
'''


'''
9. 데이터의 분리(splitting data)
'''