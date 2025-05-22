from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
llm = ChatOpenAI(model="gpt-4o-mini")

llm.invoke([HumanMessage("잘 지냈어?")])



#-----------------------------------------------------------------#
from langchain_core.tools import tool
from datetime import datetime
import pytz

@tool # @tool 데코레이터를 사용하여 함수를 도구로 등록
def get_current_time(timezone: str, location: str) -> str:
    """ 현재 시각을 반환하는 함수

    Args:
        timezone (str): 타임존 (예: 'Asia/Seoul') 실제 존재하는 타임존이어야 함
        location (str): 지역명. 타임존이 모든 지명에 대응되지 않기 때문에 이후 llm 답변 생성에 사용됨
    """
    tz = pytz.timezone(timezone)
    now = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
    location_and_local_time = f'{timezone} ({location}) 현재시각 {now} ' # 타임존, 지역명, 현재시각을 문자열로 반환
    print(location_and_local_time)
    return location_and_local_time


#-----------------------------------------------------------------#
# 도구를 tools 리스트에 추가하고, tool_dict에도 추가
tools = [get_current_time,]
tool_dict = {"get_current_time": get_current_time,}

# 도구를 모델에 바인딩: 모델에 도구를 바인딩하면, 도구를 사용하여 llm 답변을 생성할 수 있음
llm_with_tools = llm.bind_tools(tools)


#-----------------------------------------------------------------#
from langchain_core.messages import SystemMessage

# (4) 사용자의 질문과 tools 사용하여 llm 답변 생성
messages = [
    SystemMessage("너는 사용자의 질문에 답변을 하기 위해 tools를 사용할 수 있다."),
    HumanMessage("부산은 지금 몇시야?"),
]

# (5) llm_with_tools를 사용하여 사용자의 질문에 대한 llm 답변 생성
response = llm_with_tools.invoke(messages)
messages.append(response)

# (6) 생성된 llm 답변 출력
print(messages)


#-----------------------------------------------------------------#
for tool_call in response.tool_calls:
    selected_tool = tool_dict[tool_call["name"]] # (7) tool_dict를 사용하여 도구 함수를 선택
    print(tool_call["args"]) # (8) 도구 호출 시 전달된 인자 출력
    tool_msg = selected_tool.invoke(tool_call) # (9) 도구 함수를 호출하여 결과를 반환
    messages.append(tool_msg)

messages



#-----------------------------------------------------------------#
llm_with_tools.invoke(messages)


#======================================================================#
### pydantic으로 함수 입력값 형식 표현 ###
from pydantic import BaseModel, Field

class StockHistoryInput(BaseModel):
    ticker: str = Field(..., title="주식 코드", description="주식 코드 (예: AAPL)")
    period: str = Field(..., title="기간", description="주식 데이터 조회 기간 (예: 1d, 1mo, 1y)")



#-----------------------------------------------------------------#
###  pydantic으로 함수 입력값 형식 표현 ###
import yfinance as yf

##  get_yf_stock_history 함수에서 이 클래스 형식으로 매개변수를 받도록 수정
@tool
def get_yf_stock_history(stock_history_input: StockHistoryInput) -> str:
    """ 주식 종목의 가격 데이터를 조회하는 함수"""
    stock = yf.Ticker(stock_history_input.ticker)
    history = stock.history(period=stock_history_input.period)
    history_md = history.to_markdown()

    return history_md

##  tools와 tool_dict는 새로 만든 get_yf_stock_history 함수를 추가해서 다시 선언
tools = [get_current_time, get_yf_stock_history]
tool_dict = {"get_current_time": get_current_time, "get_yf_stock_history": get_yf_stock_history}

llm_with_tools = llm.bind_tools(tools)



#-----------------------------------------------------------------#
messages.append(HumanMessage("테슬라는 한달 전에 비해 주가가 올랐나 내렸나?"))

response = llm_with_tools.invoke(messages)
print(response)
messages.append(response)



#-----------------------------------------------------------------#
### 결과를 메시지로 추가 ###
for tool_call in response.tool_calls:
    selected_tool = tool_dict[tool_call["name"]]
    print(tool_call["args"])
    tool_msg = selected_tool.invoke(tool_call)
    messages.append(tool_msg)
    print(tool_msg)
    print()



#-----------------------------------------------------------------#
### 자연어로 함수 결과 처리 ###
llm_with_tools.invoke(messages)
