# pip install PyMuPDF pypdf langchain langchain_community

from langchain_community.document_loaders import PyPDFLoader

# PDF 파일을 읽어서 텍스트 데이터를 추출합니다.
loader = PyPDFLoader('../data/OneNYC_2050_Strategic_Plan.pdf')
data_nyc = loader.load()
print(data_nyc)


#--------------------------------------------------------------------#
for i, split in enumerate(all_splits):
    print(f"Split {i+1}:------------------------------------\n")
    print(split)



#--------------------------------------------------------------------#
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 텍스트 데이터를 1000자 단위로 나눕니다. overlap은 100자로 설정합니다.
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
all_splits = text_splitter.split_documents(data_nyc)


#--------------------------------------------------------------------#
for i, split in enumerate(all_splits):
    print(f"Split {i+1}:------------------------------------\n")
    print(split)



#--------------------------------------------------------------------#
print(type(all_splits[0]))


#--------------------------------------------------------------------#
loader_seoul = PyPDFLoader('data/2040_seoul_plan.pdf')
data_seoul = loader_seoul.load()
seoul_splits = text_splitter.split_documents(data_seoul)
for i, split in enumerate(seoul_splits):
    print(f"Split {i+1}:------------------------------------")
    print(split)


#--------------------------------------------------------------------#
print(seoul_splits[50].page_content)
print('----------------------')
print(seoul_splits[51].page_content)



#--------------------------------------------------------------------#
for i in range(len(seoul_splits) - 1):
    seoul_splits[i].page_content += "\n"+ seoul_splits[i + 1].page_content[:100]

print(seoul_splits[50].page_content)
print('----------------------')
print(seoul_splits[51].page_content)


#--------------------------------------------------------------------#
print(len(all_splits))
all_splits.extend(seoul_splits)
print(len(all_splits))



#--------------------------------------------------------------------#
# pip install langchain_chroma langchain_openai
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

embedding = OpenAIEmbeddings(model='text-embedding-3-large', api_key=OPENAI_API_KEY)
v = embedding.embed_query("뉴욕의 온실가스 저감 정책은 뭐야?")
print(v)
print(len(v))


#--------------------------------------------------------------------#
from langchain_chroma import Chroma
import os

persist_directory = '../chroma_store'

# 저장된 크로마 DB가 없다면 새로 만들기
if not os.path.exists(persist_directory):
    print("Creating new Chroma store")
    vectorstore = Chroma.from_documents(
        documents=all_splits,
        embedding=embedding,
        persist_directory=persist_directory
    )

else:
    print("Loading existing Chroma store")
    vectorstore = Chroma(
        persist_directory=persist_directory,
        embedding_function=embedding
    )



#--------------------------------------------------------------------#
retriever = vectorstore.as_retriever(k=3)
docs = retriever.invoke("서울시의 환경 정책에 대해 궁금해")

for d in docs:
    print(d)
    print('------')



#--------------------------------------------------------------------#
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder # ①
from langchain.chains.combine_documents import create_stuff_documents_chain # ②
from langchain_openai import ChatOpenAI # ③

chat = ChatOpenAI(model="gpt-4o-mini") # ③

# ④
question_answering_prompt = ChatPromptTemplate.from_messages(
    [
        ( # ⑤
            "system",
            "사용자의 질문에 대해 아래 context에 기반하여 답변하라.:\n\n{context}",
        ),
        MessagesPlaceholder(variable_name="messages"), # ⑥
    ]
)

document_chain = create_stuff_documents_chain(chat, question_answering_prompt) # ⑦


#--------------------------------------------------------------------#
from langchain.memory import ChatMessageHistory

# 채팅 메시지 저장할 메모리 객체 생성
chat_history = ChatMessageHistory()
# 사용자 질문을 메모리에 저장
chat_history.add_user_message("서울시의 온실가스 저감 정책에 대해 알려줘.")

# 문서 검색하고 답변 생성
answer = document_chain.invoke(
    {
        "messages": chat_history.messages,
        "context": docs,
    }
)

# 생성된 답변 메모리에 저장
chat_history.add_ai_message(answer)

print(answer)


#--------------------------------------------------------------------#
for m in chat_history.messages:
    print(m)


#--------------------------------------------------------------------#
# 문자열 출력 파서를 불러온다.
from langchain_core.output_parsers import StrOutputParser

query_for_nyc = "뉴욕은?"

# query augmentation
# 기존 대화 내용을 활용해 query_augmentation 수행
query_augmentation_prompt = ChatPromptTemplate.from_messages(
    [
        MessagesPlaceholder(variable_name="messages"), # 기존 대화 내용
        (
            "system",
            "기존의 대화 내용을 활용하여 사용자의 아래 질문의 의도를 파악하여 명료한 한 문장의 질문으로 변환하라. 대명사나 이, 저, 그와 같은 표현을 명확한 명사로 표현하라. :\n\n{query}",
        ),
    ]
)

#--------------------------------------------------------------------#
query_augmentation_chain = query_augmentation_prompt | chat | StrOutputParser()


#--------------------------------------------------------------------#
augmented_query = query_augmentation_chain.invoke({
    "messages": chat_history.messages,
    "query": query_for_nyc
})

print(augmented_query)



#--------------------------------------------------------------------#
docs = retriever.invoke(augmented_query)

for d in docs:
    print(d)
    print('------')


#--------------------------------------------------------------------#
chat_history.add_user_message(query_for_nyc) # query_for_nyc에 "뉴욕은?" 추가

answer = document_chain.invoke(
    {
        "messages": chat_history.messages,
        "context": docs,
    }
)

# 생성된 답변 메모리에 저장
chat_history.add_ai_message(answer)

print(answer)

