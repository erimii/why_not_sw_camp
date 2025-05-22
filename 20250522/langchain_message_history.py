from dotenv import load_dotenv
load_dotenv()

# 메모리에 대화 기록을 저장하는 클래스
from langchain_core.chat_history import InMemoryChatMessageHistory

# 메시지 기록을 활용해 실행 가능한 래퍼wrapper 클래스
from langchain_core.runnables.history import RunnableWithMessageHistory

# 오픈AI 모델을 사용하는 랭체인 챗봇 클래스
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

model = ChatOpenAI(model="gpt-4o-mini")

# 세션별 대화 기록을 저장할 딕셔너리
store = {}

# 세션 ID에 따라 대화 기록을 가져오는 함수
def get_session_history(session_id: str):

    # 만약 해당 세션 ID가 store에 없으면, 새로 생성해 추가함
    if session_id not in store:
        # 메모리에 대화 기록을 저장하는 객체 생성
        store[session_id] = InMemoryChatMessageHistory()

    return store[session_id]  # 해당 세션의 대화 기록을 반환

# 모델 실행 시 대화 기록을 함께 전달하는 래퍼 객체 생성
with_message_history = RunnableWithMessageHistory(model, get_session_history)

#-------------------------------------------------------------#
# 세션 ID를 설정하는 config 객체 생성
config = {"configurable": {"session_id": "abc2"}}


response = with_message_history.invoke(
    [HumanMessage(content="안녕? 난 홍길동이야.")],
    config=config,
)
print(response.content)

#-------------------------------------------------------------#
response = with_message_history.invoke(
    [HumanMessage(content="내 이름이 뭐지?")],
    config=config,
)
print(response.content)


#-------------------------------------------------------------#
config = {"configurable": {"session_id": "abc2"}}

response = with_message_history.invoke(
    [HumanMessage(content="아까 우리가 무슨 얘기 했지?")],
    config=config,
)
print(response.content)

#-------------------------------------------------------------#
### 스트림 방식으로 출력하기 ###
config = {"configurable": {"session_id": "abc2"}}
for r in with_message_history.stream(
    [HumanMessage(content = "내가 어느 나라 사람인지 맞춰보고, 그 나라의 문화에 대해 말해봐")],
    config=config,
):
    print(r.content, end="|")
