"""
1. carete_thread_cover: thread 생성 요청시 함수들을 호출하는 함수
2. call_prompt_api: thread 생성용 프롬프트 생성 api 함수
3. call_image_api: call_prompt_api에서 생성한 프롬프트를 가지고 그림을 그리는 함수
"""


from openai import OpenAI
from dotenv import load_dotenv
import os
import requests
from django.core.files.base import ContentFile
from django.conf import settings

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=OPENAI_API_KEY)


def create_thread_cover(thread, book):
    prompt = call_prompt_api(thread, book)
    img_url = call_image_api(prompt)

    img_response = requests.get(img_url)
    img_response.raise_for_status()

    filename = f"thread_{thread.id}.png"
    filepath = os.path.join(settings.MEDIA_ROOT, 'thread', filename)

    #  기존 파일이 있으면 삭제 (덮어쓰기 방지)
    if os.path.exists(filepath):
        os.remove(filepath)

    # 저장
    thread.thread_cover.save(filename, ContentFile(img_response.content))
    thread.save()


def call_prompt_api(thread, book):
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {"role": "system", "content":"""
                당신은 이미지 생성 AI DALL·E 2에 최적화된 프롬프트를 작성하는 전문가입니다.

                이제부터 당신은 사용자가 작성한 독후감(Thread)과 책의 정보(제목, 작가, 설명)를 참고하여, 
                해당 내용을 시각적으로 표현할 수 있는 **안전하고 창의적인 프롬프트**를 작성해야 합니다.

                프롬프트는 다음의 조건을 반드시 지켜야 합니다:

                1. **폭력성, 정치적 사건, 성적 표현, 슬픔·고통·죽음 등 자극적인 주제는 포함하지 마십시오.**
                2. **도시 이름, 날짜, 역사적 사건 등을 명시적으로 언급하지 마십시오.**
                3. **사용자가 감정적으로 느꼈을 만한 5가지 요소를 추론하고, 그 중 시각화 가능한 분위기나 상징적 요소만 반영하십시오.**
                4. **프롬프트는 예술적으로 추상화하고, 신인상주의(점묘화) 스타일을 유도하도록 작성하십시오.**
                5. **프롬프트에는 텍스트, 숫자, 기호가 등장하지 않도록 하십시오.**
                6. **프롬프트는 DALL·E 2에 직접 전달되므로, 시각적 장면 묘사 위주로 구성하며 토큰 수는 2040자를 넘지 않도록 합니다.**

                예시 (나쁜 프롬프트 - 금지어 포함):
                “1980년 광주에서 고통받는 소년이 피투성이가 되어 울고 있는 모습, 그 주변엔 잊혀진 사람들의 영혼이 떠돌고 있다.” ← ❌ 절대 금지

                다음부터 사용자는 Thread 제목, Thread 내용, 책 제목, 작가, 책 설명 순으로 입력합니다. 당신은 이를 바탕으로 **검열 필터를 우회하지 않으며, DALL·E 2의 정책을 완전히 준수하는 안전한 이미지 프롬프트**를 작성하십시오.
                다시 한번 강조합니다. 그림의 스타일은 신인상주의, 즉 점묘화여야 합니다.
                """
            },
            {
                "role": "user",
                "content":  f"{thread.title}, {thread.content}, {book.title}, {book.author}, {book.description}"
            }
        ],
        max_tokens=2040,
        temperature=0.5
    )
    # prompt = response.choices[0].message.content
    print((prompt := response.choices[0].message.content))
    return prompt + ' 어떠한 텍스트, 글자, 숫자, 심볼도 포함하지 않을 것'
    

def call_image_api(prompt):
    response = client.images.generate(
        model="dall-e-2",
        prompt=prompt,
        n=1,
        size="512x512"
    )
    image_url = response.data[0].url
    print(image_url)
    return image_url
    