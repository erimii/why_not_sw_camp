# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 15:30:44 2025

@author: Admin
"""
# 비정형 데이터를 분석 후 word cloud로 분석하기

# -------------------------------------------------
# 성형 수술 부작용 관련 키워드
# -------------------------------------------------
from konlpy.tag import Okt
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
import re


# 텍스트 파일 불러오기
file_path = "data/성형부작용.txt"
with open(file_path, "r", encoding="cp949") as file:
    text = file.read()

# 불용어 리스트 불러오기
stopword_path = "data/불용어 사전의 예/성형부작용gsub.txt"
with open(stopword_path, "r", encoding="cp949") as file:
    stopwords = file.read().split("\n")  # 불용어를 리스트로 변환

# 텍스트 전처리
text = re.sub(r"[^가-힣\s]", "", text)  # 한글과 공백 제외 삭제
text = text.strip()  # 앞뒤 공백 제거
# 형태소 분석기 설정
okt = Okt()

# 명사 추출
nouns = okt.nouns(text)

# 불용어 제거
filtered_nouns = [word for word in nouns if word not in stopwords and len(word) > 1]  # 불용어 제외 & 한 글자 단어 제거

# 빈도수 계산
word_counts = Counter(filtered_nouns)

# 상위 50개 단어 확인
print(word_counts.most_common(50))

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
    max_words = 100
).generate_from_frequencies(word_counts)

# 시각화
plt.figure(figsize=(10, 6))
plt.title('성형 부작용', fontsize=15)
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()
