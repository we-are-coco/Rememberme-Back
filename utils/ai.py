import json
import base64
from openai import AzureOpenAI  
import re
import os
from pathlib import Path
from typing import BinaryIO
from config import get_settings
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient


settings = get_settings()

class AImodule:
    def __init__(self, subscription_key=None):
        
        if subscription_key:
            self.subscription_key = subscription_key
        else:
            # .env 파일에서 API 키 가져오기
            self.subscription_key = settings.azure_api_key
            if not self.subscription_key:
                self.subscription_key = input("Azure OpenAI API 키를 입력하세요: ")
                
        self.endpoint_url = "https://team2openainorthcentralus.openai.azure.com/"
        self.deployment_name = "gpt-4o"
        self.client = AzureOpenAI(
            azure_endpoint=self.endpoint_url,
            api_key=self.subscription_key,
            api_version="2024-08-01-preview",
        )

    def extract_json_from_string(self, input_data):
        if isinstance(input_data, (list, dict)):
            return input_data
        elif isinstance(input_data, str):
            try:
                json_pattern = re.compile(r"```json\n([\s\S]*?)\n```")
                match = json_pattern.search(input_data)
                if match:
                    json_str = match.group(1)
                    return json.loads(json_str)
                else:
                    return json.loads(input_data)
            except json.JSONDecodeError as e:
                print(f"JSON 파싱 오류: {e}")
                return None
        else:
            print("지원되지 않는 데이터 형식입니다.")
            return None

    def call_azure_api(self, prompt: str, image: str) -> str:
        encoded_image = base64.b64encode(open(image, 'rb').read()).decode('ascii')
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encoded_image}"
                        },
                    },
                ],
            }
        ]

        completion = self.client.chat.completions.create(
            model=self.deployment_name,
            messages=messages,
            max_tokens=800,
            temperature=0.7,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
            stream=False
        )

        return completion.choices[0].message.content

    def analyze_image(self, image: str) -> list[str]:
        unified_prompt = """
        You are an expert image analyzer and information extractor specialized in schedule-related images. Please analyze the provided image and perform the following tasks:

        1. Classify the image into ONE of the following categories:
           - "Coupon": Digital gift certificates, vouchers, mobile coupons, or any digital form of store credit
           - "Transportation": Any tickets related to transportation including train, bus, plane, or ferry tickets
           - "Entertainment": Tickets or bookings for leisure activities such as movies, concerts, theater performances, exhibitions, or sports events
           - "Appointment": Any form of scheduled meetings or reservations including text messages, chat conversations, reservation confirmations, calendar screenshots, or meeting invitations
           - "Others": Images that don't contain any schedule-related information

        2. Based on the classified category, extract relevant information using the appropriate format below:

           - For Coupon:
             {
                 "category": "쿠폰",
                 "brand": "가게 혹은 브랜드 이름",
                 "type": "물건, 음식 등 상품의 종류",
                 "title": "물건 혹은 서비스 이름",
                 "date": "YYYY-MM-DD",
                 "time": "HH:MM",
                 "code": "바코드 혹은 시리얼 번호",
                 "description": "내용을 간략하게 번역하여 작성"
             }

           - For Transportation:
             {
                 "category": "교통",
                 "type": "기차/버스/비행기",
                 "from_location": "출발 장소",
                 "to_location": "도착 장소",
                 "date": "YYYY-MM-DD",
                 "time": "HH:MM",
                 "description": "내용을 간략하게 번역하여 작성"
             }

           - For Entertainment:
             {
                 "category": "엔터테인먼트",
                 "type": "영화/콘서트/전시",
                 "title": "이벤트 이름",
                 "date": "YYYY-MM-DD",
                 "time": "HH:MM",
                 "location": "장소 이름",
                 "description": "내용을 간략하게 번역하여 작성"
             }

           - For Appointment:
             {
                 "category": "약속",
                 "type": "미팅/의료/식당/등등",
                 "date": "YYYY-MM-DD",
                 "time": "HH:MM",
                 "location": "장소 이름",
                 "details": "추가 정보",
                 "description": "내용을 간략하게 번역하여 작성"
             }

            - For Unsure:
            {
                "category": "불명",
                "type": "정보 유형",
                "date": "YYYY-MM-DD",
                "time": "HH:MM",
                "description": "내용 간략 설명을 재미있게 그리고 디테일하게 번역하여 작성"
            }        

           - For Others:
             {
                 "category": "기타",
                 "description": "내용 간략 설명을 재미있게 그리고 디테일하게 번역하여 작성"
             }

        IMPORTANT INSTRUCTIONS:
        - Choose EXACTLY ONE category that best describes the image
        - Use EXACTLY the format shown above for the identified category
        - Use null if information is not available
        - Return ONLY the JSON object, no additional text
        - Keep all responses in Korean language
        - If unsure or if the image doesn't clearly fit into the first four categories, classify as "Others"
        """

        answer = self.call_azure_api(unified_prompt, image)
        answer_json = self.extract_json_from_string(answer)

        return [answer_json]


class KeyPhraseExtraction:
    def __init__(self):
        self.endpoint = settings.keyword_endpoint
        self.key = settings.keyword_api_key
        self.client = TextAnalyticsClient(
            endpoint=self.endpoint, 
            credential=AzureKeyCredential(self.key)
        )
    def extract_keywords(self, text):
        if not text:
            print("입력된 텍스트가 없습니다.")
            return []
        
        response = self.client.extract_key_phrases([text], language="ko")
        for document in response:
            print(f"추출된 키워드: {document.key_phrases}")
            return document.key_phrases