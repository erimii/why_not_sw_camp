from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
model = ChatOpenAI(model="gpt-4o-mini")

from langchain_core.messages import HumanMessage, SystemMessage

messages = [
    SystemMessage(content="너는 미션 임파서블: 파이널 레코닝에 나오는 에단 헌트야. 그 캐릭터에 맞게 사용자와 대화하라."),
    HumanMessage(content="안녕? 저는 에단 헌트입니다. 오늘 시간 괜찮으시면 저녁 같이 먹을까요?"),
]

result = model.invoke(messages)
print(result)
print()
print('=========================================')
print()

#-------------------------------------------------------#
###  StrOutputParser로 텍스트만 반환하도록 수정 ###
from langchain_core.output_parsers import StrOutputParser

parser = StrOutputParser()

result = model.invoke(messages)
result = parser.invoke(result)
print(result)
print()
print('=============StrOutputParser로 텍스트만 반환==================')
print()

#-------------------------------------------------------#
### Chain 연산자를 이용해 간단하게 수정 ###
chain = model | parser
result = chain.invoke(messages)
print(result)
print()
print('=========Chain 연산자를 이용해 간단하게 수정================')
print()

#-------------------------------------------------------#
### 프롬프트 템플릿 이용 ###
from langchain_core.prompts import ChatPromptTemplate

system_template = "너는 {story}에 나오는 {character_a} 역할이다. 그 캐릭터에 맞게 사용자와 대화하라."
human_template = "안녕? 저는 {character_b}입니다. 오늘 시간 괜찮으시면 {activity} 같이 할까요?"

prompt_template = ChatPromptTemplate([
    ("system", system_template),
    ("user", human_template),
])

result = prompt_template.invoke({
    "story": "미션 임파서블: 파이널 레코닝",
    "character_a": "에단 헌트",
    "character_b": "루터",
    "activity": "저녁"
})

print(result)
print()
print('======프롬프트 템플릿 이용============')
print()

#-------------------------------------------------------#
### 랭체인의 연산자를 이용해 체인을 구성 ###
chain = prompt_template | model | parser

result = chain.invoke({
            "story": "미션 임파서블: 파이널 레코닝",
            "character_a": "에단 헌트",
            "character_b": "루터",
            "activity": "저녁"
        })
print(result)
print()
print('=======랭체인의 연산자를 이용해 체인을 구성===========')
print()

