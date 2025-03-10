'''
텍스트 전처리(text preprocessing): 텍스트를 사전에 처리하는 작업

1. 토큰화(tokenization)
2. 정제(cleaning) and 정규화(normalization)
3. 어간 추출 and 표재어 추출
4. 불용어(stopword)
'''

'''
1. 토큰화(tokenization): token 단위로 나누는 작업.
단어 토큰화(word tokenization)
문장 토큰화(sentence tokenization)

고려사항
- 구두점이나 특수 문자를 단순 제외해서는 안된다
    - . ? ! 등 은 문장의 경계를 알 수 있는데 도움이 됨
    - Ph.D, hooe-based 등...
    - 3$, 2025-03-03, 10,000 등...
    
- 줄임말, 단어 내에 띄어쓰기가 있는 경우
    - don't
    - new york, rock n roll
'''

### 단어 토큰화(word tokenization)
from nltk.tokenize import word_tokenize
from nltk.tokenize import WordPunctTokenizer
from tensorflow.keras.preprocessing.text import text_to_word_sequence
from nltk.tokenize import TreebankWordTokenizer
import nltk

nltk.download('punkt_tab')

text_kor = """나는 데이터 분석을 공부하면서 불필요한 정보를 제거하고 정제하는 것이 중요하다고 느꼈다. 
            또한, 2025-03-03까지 10,000개의 데이터를 처리해야 한다. 
            Ph.D 연구자들은 hooe-based 접근 방식을 선호하지만, Mr. Jone’s 의견은 다르다."""


text_eng = """I realized that cleaning and removing unnecessary information is crucial while studying data analysis. 
            Also, 10,000 data points must be processed by 2025-03-03. 
            Ph.D researchers prefer a hooe-based approach, but Mr. Jone’s opinion is different."""

text1="Ph.D researchers prefer a home-based approach, but Mr. Jone’s opinion is different."
# word_tokenize
print(word_tokenize(text1))
'''
['I', 'realized', 'that', 'cleaning', 'and', 'removing', 'unnecessary', 'information', 'is', 'crucial', 
 'while', 'studying', 'data', 'analysis', '.', 'Also', ',', '10,000', 'data', 'points', 'must', 'be', 'processed', 'by', '2025-03-03', '.', 
 'Ph.D', 'researchers', 'prefer', 'a', 'hooe-based', 'approach', ',', 'but', 'Mr.', 'Jone', '’', 's', 'opinion', 'is', 'different', '.']
'''

# WordPunctTokenizer
print(WordPunctTokenizer().tokenize(text1))
'''
['I', 'realized', 'that', 'cleaning', 'and', 'removing', 'unnecessary', 'information', 'is', 'crucial', 
 'while', 'studying', 'data', 'analysis', '.', 'Also', ',', '10', ',', '000', 'data', 'points', 'must', 'be', 'processed', 'by', '2025', '-', '03', '-', '03', '.', 
 'Ph', '.', 'D', 'researchers', 'prefer', 'a', 'hooe', '-', 'based', 'approach', ',', 'but', 'Mr', '.', 'Jone', '’', 's', 'opinion', 'is', 'different', '.']
'''

# text_to_word_sequence
print(text_to_word_sequence(text1))
'''
['i', 'realized', 'that', 'cleaning', 'and', 'removing', 'unnecessary', 'information', 'is', 'crucial', 
 'while', 'studying', 'data', 'analysis', 'also', '10', '000', 'data', 'points', 'must', 'be', 'processed', 'by', '2025', '03', '03', 
 'ph', 'd', 'researchers', 'prefer', 'a', 'hooe', 'based', 'approach', 'but', 'mr', 'jone’s', 'opinion', 'is', 'different']
'''

tokenizer = TreebankWordTokenizer()
print(tokenizer.tokenize(text1))
'''
['I', 'realized', 'that', 'cleaning', 'and', 'removing', 'unnecessary', 'information', 'is', 'crucial', 
 'while', 'studying', 'data', 'analysis.', 'Also', ',', '10,000', 'data', 'points', 'must', 'be', 'processed', 'by', '2025-03-03.', 
 'Ph.D', 'researchers', 'prefer', 'a', 'hooe-based', 'approach', ',', 'but', 'Mr.', 'Jone’s', 'opinion', 'is', 'different', '.']
'''


### 문장 토큰화(sentence tokenization)
from nltk.tokenize import sent_tokenize
text = "I love programming. NLP is fascinating!"
print(sent_tokenize(text))
'''
['I realized that cleaning and removing unnecessary information is crucial while studying data analysis.', 
 'Also, 10,000 data points must be processed by 2025-03-03.', 
 'Ph.D researchers prefer a hooe-based approach, but Mr. Jone’s opinion is different.']
'''


'''
한국어 토근화 어려움
형태소(뜻을 가진 가장 작은 말의 단위)란 개념 이해 필요
- 자립 형태소: 명사, 대명사, 수사, 관형사, 부사, 감탄사 등
- 의존 형태소: 다른 형태소와 결합돼서 사용됨. 접사, 어미, 조사, 어간

예) 루비가 책을 읽었다
['루비가', '책을', '읽었다']

형태소 단위로 분해
    자립 형태소: 루비, 책
    의존 형태소: -가, -을, 읽-, -었-, -다
'''

'''
품사 태깅 (part-of-speech tagging)
- 표기는 같지만 품사에 따라 단어의 의미가 달라질 수 있음
    예) '못': 명사로는 screw 의미, 부사로서는 '못 먹는다' 등 동작 동사 할 수 없다는 의미

- 단어 토큰화 과정에서 각 단어가 어떤 품사로 쓰였는지 구분해놓는 작업
'''

from konlpy.tag import Okt
from konlpy.tag import Kkma
okt = Okt()
kkma = Kkma()

text='열심히 코딩한 당신, 연휴에는 여행을 가라'
# okt
print(f'okt 형태소 분석: {okt.morphs(text)}')
'''
okt 형태소 분석: ['열심히', '코딩', '한', '당신', ',', '연휴', '에는', '여행', '을', '가라']
'''
print(f'okt 품사 태깅: {okt.pos(text)}')
'''
okt 품사 태깅: [('열심히', 'Adverb'), ('코딩', 'Noun'), ('한', 'Josa'), ('당신', 'Noun'), (',', 'Punctuation'), ('연휴', 'Noun'), ('에는', 'Josa'), ('여행', 'Noun'), ('을', 'Josa'), ('가라', 'Noun')]
'''
print(f'okt 명사 추출: {okt.nouns(text)}')
'''
okt 명사 추출: ['코딩', '당신', '연휴', '여행', '가라'] -> '가라'는 명사 아닌데?
'''
# kkma
print(f'kkma 형태소 분석: {kkma.morphs(text)}')
'''
kkma 형태소 분석: ['열심히', '코딩', '하', 'ㄴ', '당신', ',', '연휴', '에', '는', '여행', '을', '가라']
'''
print(f'kkma 품사 태깅: {kkma.pos(text)}')
'''
kkma 품사 태깅: [('열심히', 'MAG'), ('코딩', 'NNG'), ('하', 'XSV'), ('ㄴ', 'ETD'), ('당신', 'NP'), (',', 'SP'), ('연휴', 'NNG'), ('에', 'JKM'), ('는', 'JX'), ('여행', 'NNG'), ('을', 'JKO'), ('가라', 'VV')]
'''
print(f'kkma 명사 추출: {kkma.nouns(text)}')
'''
kkma 명사 추출: ['코딩', '당신', '연휴', '여행']
'''


'''
2. 정제(cleaning) and 정규화(normalization)
정제: 코퍼스로부터 노이즈 데이터를 제거
정규화: 표현 방법이 다른 단어들을 통합시켜 같은 단어로 만드는 작업

정제 작업
    1. 토큰화 작업 전에 토큰화 작업에 방해되는 부분들 배제 시킴
    2. 토큰화 작업 이후에는 여전히 남아있는 노이즈 제거하기위해 지속적으로 이루어짐
    3. 완벽한 정제는 어려움.

고려 사항
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
3. 표재어 추출 and 어간 추출
- 정규화 기법 중 코퍼스에 있는 단어의 개수를 줄일 수 있는 기법

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
print([lemmatizer.lemmatize(word) for word in words])
# ['policy', 'doing', 'organization', 'have', 'going', 'love', 'life', 'fly', 'dy', 'watched', 'ha', 'starting']

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
예) "루비가 학교에 가서 친구들과 함께 공부를 열심히 했다."
- 어근:
    - '학교' (장소를 나타내는 중심 부분)
    - '공부' (행동을 나타내는 중심 부분)
- 어간:
    - '가' (동사 '가다'의 어간)
    - '하' (동사 '하다'의 어간)
- 어미:
    - '서' (동사 ‘가다’의 연결 어미)
    - '였' (과거 시제 선어말 어미)
    - '다' (어말 어미)
- 단어:
    - '루비', '학교', '가서', '친구들', '공부', '열심히', '했다'
- 어절:
    - '루비가', '학교에', '가서', '친구들과', '함께', '공부를', '열심히', '했다' (띄어쓰기 단위)
'''
# 어간 추출 알고리즘: Porter 알고리즘과 lancaster stemmer 알고리즘
from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer
from nltk.tokenize import word_tokenize

por = PorterStemmer()
lan = LancasterStemmer()
tokenized_sentence = word_tokenize(text1)
print([por.stem(word) for word in tokenized_sentence])
'''
['i', 'realiz', 'that', 'clean', 'and', 'remov', 'unnecessari', 'inform', 'is', 'crucial', 
 'while', 'studi', 'data', 'analysi', '.', 'also', ',', '10,000', 'data', 'point', 'must', 'be', 'process', 'by', '2025-03-03', '.', 
 'ph.d', 'research', 'prefer', 'a', 'hooe-bas', 'approach', ',', 'but', 'mr.', 'jone', '’', 's', 'opinion', 'is', 'differ', '.']
'''

print([lan.stem(word) for word in tokenized_sentence])
'''
['i', 'real', 'that', 'cle', 'and', 'remov', 'unnecess', 'inform', 'is', 'cruc', 
 'whil', 'study', 'dat', 'analys', '.', 'also', ',', '10,000', 'dat', 'point', 'must', 'be', 'process', 'by', '2025-03-03', '.', 
 'ph.d', 'research', 'pref', 'a', 'hooe-based', 'approach', ',', 'but', 'mr.', 'jon', '’', 's', 'opin', 'is', 'diff', '.']
'''


'''
한국어에서의 어간 추출
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

