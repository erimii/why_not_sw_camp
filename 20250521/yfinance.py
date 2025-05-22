# pip install yfinance

import yfinance as yf

# Microsoft (MSFT)에 대한 Ticker 객체 생성
msft = yf.Ticker("MSFT")

# Ticker 객체에 대한 정보 출력
print(msft.info)


hist = msft.history(period="5d") # 5일간의 주가 데이터를 가져옴
print(hist) # 데이터 출력

msft.recommendations # 추천 정보 출력

