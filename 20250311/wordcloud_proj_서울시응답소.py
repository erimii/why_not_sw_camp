# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 15:11:37 2025

@author: Admin
"""
# 비정형 데이터를 분석 후 word cloud로 분석하기

# -------------------------------------------------
# 서울시 응답소 페이지 분석하기
# -------------------------------------------------

from konlpy.tag import Okt
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
    

# 파일 불러오기
file_path = "data/서울시 응답소.txt"

with open(file_path, "r", encoding="cp949") as file:
    text = file.read()

# 형태소 분석기 선언
okt = Okt()

# 형태소 분석 실행
tokens = okt.morphs(text)  # 명사만 추출하려면 okt.nouns(text)
print(tokens[:50])  # 앞부분 50개만 출력

# 명사 추출
nouns = okt.nouns(text)

# 불용어 제거
filtered_nouns = [word for word in nouns if word not in ['관련', '대한', '시장님', '서울시'] and len(word) > 1]

# 빈도수 계산
word_counts = Counter(filtered_nouns)

from matplotlib import font_manager, rc
import platform

if platform.system() == 'Darwin':
    rc('font', family = 'AppleGothic')
elif platform.system() == 'Windows':
    path = 'c:/Windows/Fonts/malgun.ttf'
    font_name = font_manager.FontProperties(fname=path).get_name()
    rc('font', family=font_name)
else:
    print("sorry")
    
font_path = "c:/Windows/Fonts/malgun.ttf"

# 워드클라우드 생성
wordcloud = WordCloud(
    font_path=font_path,
    background_color="white",
    width=800,
    height=600,
    max_words = 150
).generate_from_frequencies(word_counts)

# 시각화
plt.figure(figsize=(10, 6))
plt.title('서울시 응답소', fontsize=15)
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()
