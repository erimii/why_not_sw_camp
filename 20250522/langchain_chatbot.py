# pip install langchain
# pip install langchain-openai
from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
model = ChatOpenAI(model="gpt-4o-mini")

from langchain_core.messages import HumanMessage
print(model.invoke([HumanMessage(content="안녕? 나는 홍길동이야.")]))

print(model.invoke([HumanMessage(content="내 이름이 뭐지?")]))
