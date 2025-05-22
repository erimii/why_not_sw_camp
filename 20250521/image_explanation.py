from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")  # 환경 변수에서 API 키를 가져오기

client = OpenAI(api_key=api_key)  # 오픈AI 클라이언트의 인스턴스 생성

#------------------------------------------------------------------------------------#
"""
# GPT 비전을 이용해 인터넷상의 이미지 설명 받기
messages = [
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "이 이미지에 대해 설명해주세요."},
            {
                "type": "image_url",
                "image_url": {
                    "url": "https://images.unsplash.com/photo-1736264335247-8ec5664c8328?q=80&w=1887&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
                },
            },
        ],
    }
]

response = client.chat.completions.create(
    model="gpt-4o",  # 응답 생성에 사용할 모델 지정
    messages=messages # 대화 기록을 입력으로 전달
)

print(response)
"""

#------------------------------------------------------------------------------------#
import base64


# 이미지를 인코딩하는 함수
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


image_path = "../data/images/mangwon_bakery.jpg"

# 이미지를 base64로 인코딩
base64_image = encode_image(image_path)

"""
print(base64_image)

#------------------------------------------------------------------------------------#
# base64로 변환한 이미지 설명 요청하기
messages = [
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "이 이미지에 대해 설명해주세요."},
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}",
                },
            },
        ],
    }
]

response = client.chat.completions.create(
    model="gpt-4o",  # 응답 생성에 사용할 모델 지정
    messages=messages # 대화 기록을 입력으로 전달
)

print(response.choices[0].message.content)
"""

#------------------------------------------------------------------------------------#
# 여러 이미지 비교 분석 요청하기
"""
seolleung_terrarosa_base64 = encode_image("../data/images/seolleung_terrarosa.jpg")
local_stitch_terrarosa_base64 = encode_image("../data/images/local_stitch_terrarosa.jpg")

messages = [
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "두 카페의 차이점을 설명해주세요."},
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{seolleung_terrarosa_base64}",
                },
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{local_stitch_terrarosa_base64}",
                },
            },
        ],
    }
]

response = client.chat.completions.create(
    model="gpt-4o",  # 응답 생성에 사용할 모델 지정
    messages=messages # 대화 기록을 입력으로 전달
)

print(response.choices[0].message.content)
"""

#----------------------------------------------------------------------------
# GPT 비전을 사용해 2021년과 2022년 그래프를 비교 분석
# 해상도가 다른 이미지 2개를 사용해 각각 어떤 결과가 나오는지 확인
"""
oecd_rnd_2021_base64 = encode_image("../data/images/oecd_rnd_2021_large.png")
oecd_rnd_2022_base64 = encode_image("../data/images/oecd_rnd_2022_large.png")

messages = [
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "첫번째는 2021년 데이터이고, 두번째는 2022년 데이터입니다. 이 데이터에 대해 설명해주세요. 어떤 변화가 있었나요? 한국 중심으로 설명해주세요."},
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{oecd_rnd_2021_base64}",
                },
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{oecd_rnd_2022_base64}",
                },
            },
        ],
    }
]

response = client.chat.completions.create(
    model="gpt-4o",  # 응답 생성에 사용할 모델 지정
    messages=messages # 대화 기록을 입력으로 전달
)

print(response.choices[0].message.content)
"""

#----------------------------------------------------------------------------
# oecd_rnd_2021_large.png 대신 해상도가 조금 낮은 oecd_rnd_2021_medium.png 파일을 사용.
# 이 이미지는 895*538 픽셀입.
# 이전 코드에서 oecd_rnd_ 2021_large.png를 oecd_rnd_2021_medium.png로 바꿔서 실행.

oecd_rnd_2021_base64 = encode_image("../data/images/oecd_rnd_2021_medium.png")
oecd_rnd_2022_base64 = encode_image("../data/images/oecd_rnd_2022.png")

messages = [
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "첫번째는 2021년 데이터이고, 두번째는 2022년 데이터입니다. 이 데이터에 대해 설명해주세요. 어떤 변화가 있었나요? 한국 중심으로 설명해주세요."},
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{oecd_rnd_2021_base64}",
                },
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{oecd_rnd_2022_base64}",
                },
            },
        ],
    }
]

response = client.chat.completions.create(
    model="gpt-4o",  # 응답 생성에 사용할 모델 지정
    messages=messages # 대화 기록을 입력으로 전달
)

print(response.choices[0].message.content)