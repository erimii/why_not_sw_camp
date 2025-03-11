# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 15:57:26 2025

@author: Admin
"""

# 비정형 데이터를 분석 후 word cloud로 분석하기

# -------------------------------------------------
# 대통령 신년 연설문 분석하기 2013~2015
# -------------------------------------------------
from konlpy.tag import Okt
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
import re


# 텍스트 파일 불러오기
file_path1 = "data/박근혜대통령취임사_2013.txt"
with open(file_path1, "r", encoding="cp949") as file:
    text1 = file.read()
    
file_path2 = "data/박근혜대통령신년연설문_2014_01_06.txt"
with open(file_path2, "r", encoding="cp949") as file:
    text2 = file.read()
    
file_path3 = "data/박근혜대통령신년연설문_2015_01_12.txt"
with open(file_path3, "r", encoding="cp949") as file:
    text3 = file.read()

# 불용어 리스트 불러오기
stopword_path = "data/불용어 사전의 예/박근혜대통령gsub.txt"
with open(stopword_path, "r", encoding="cp949") as file:
    stopwords = file.read().split("\n")  # 불용어를 리스트로 변환

# 텍스트 전처리
text1 = re.sub(r"[^가-힣\s]", "", text1).strip()
text2 = re.sub(r"[^가-힣\s]", "", text2).strip()
text3 = re.sub(r"[^가-힣\s]", "", text3).strip()

# 형태소 분석기 설정
okt = Okt()

# 명사 추출
nouns1 = okt.nouns(text1)
nouns2 = okt.nouns(text2)
nouns3 = okt.nouns(text3)

# 불용어 제거
filtered_nouns1 = [word for word in nouns1 if word not in stopwords and len(word) > 1]  # 불용어 제외 & 한 글자 단어 제거
filtered_nouns2 = [word for word in nouns2 if word not in stopwords and len(word) > 1]
filtered_nouns3 = [word for word in nouns3 if word not in stopwords and len(word) > 1]

# 빈도수 계산
word_counts1 = Counter(filtered_nouns1)
word_counts2 = Counter(filtered_nouns2)
word_counts3 = Counter(filtered_nouns3)

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

# 시각화
fig = plt.figure(figsize = (5,12))
ax1 = fig.add_subplot(3,1,1) # 1행 2열의 1
ax2 = fig.add_subplot(3,1,2) # 1행 2열의 2
ax3 = fig.add_subplot(3,1,3)
# 워드클라우드 생성
wordcloud1 = WordCloud(
    font_path=font_path,
    background_color="white",
    width=800,
    height=600,
    max_words = 100,
).generate_from_frequencies(word_counts1)

wordcloud2 = WordCloud(
    font_path=font_path,
    background_color="white",
    width=800,
    height=600,
    max_words = 100,
).generate_from_frequencies(word_counts2)

wordcloud3 = WordCloud(
    font_path=font_path,
    background_color="white",
    width=800,
    height=600,
    max_words = 100,
).generate_from_frequencies(word_counts3)

ax1.imshow(wordcloud1, interpolation="bilinear")
ax1.axis("off")  # 축 없애기
ax1.set_title("2013",fontsize=8)

ax2.imshow(wordcloud2, interpolation="bilinear")
ax2.axis("off")  # 축 없애기
ax2.set_title("2014", fontsize=8)

ax3.imshow(wordcloud3, interpolation="bilinear")
ax3.axis("off")  # 축 없애기
ax3.set_title("2015", fontsize=8)

plt.show()
