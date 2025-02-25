import base64
import time
import json
from openai import AzureOpenAI
from config import get_settings

settings = get_settings()


def azure_audio_request(file_path):
    with open(file_path, "rb") as audio_data:
        #wav_bytes = sr.Recognizer().record(audio_data)
        wav_bytes = audio_data.read()
        encoded_string = base64.b64encode(wav_bytes).decode('utf-8')

        # Azure OpenAI 설정
        endpoint = settings.gpt_audio_api
        api_key = settings.gpt_audio_key
        client = AzureOpenAI(
            api_version="2025-01-01-preview",
            api_key=api_key,
            azure_endpoint=endpoint
        )

        completion = client.chat.completions.create(
            model="gpt-4o-audio-preview",
            modalities=["text", "audio"],
            audio={"voice": "alloy", "format": "wav"},
            timeout=50,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"""입력된 오디오의 중요 단어를 출력하세요. 
                            현재 시간은 [{time.strftime('%Y-%m-%d %H:%M:%S')}] 입니다. 
                            명확한 시간이나 날짜가 아닌 불특정 시간이나 날짜 전체가 포함되는 검색이 필요할 경우 현재 시간을 참고해서 변환하세요. 
                            (만료 시간이라면 해당 시간이나 날짜보다 이전 이어야하고 티켓이나 콘서트처럼 시작 시간이 있는 경우는 해당 날짜나 시간보다 이후여야 합니다.)
                            (따라서 불특정 검색의 경우, 날짜나 시간에 이전이어야 하면 "이전", 이후여야 하면 "이후"을 넣어줘야 합니다.)
                            (Important) "큼", "작음" 같은 조건이 필요한 경우 리스트 맨 처음에만 작성하고 그 이후의 키워드는 날짜와 시간 포함, 최대 3개까지만 작성해줘야 합니다.
                            
                            ex) 
                            input: 부산으로 가는 티켓 찾아줘. 
                            Output: ["부산", "티켓"], 

                            input: 15일에 뉴욕으로 가는 비행기 티켓 찾아줘
                            Output: ["15일", "뉴욕", "티켓"], 

                            input: 다음 주에 만료되는 쿠폰 찾아줘. 
                            *현재시간 2025-02-06-14:00:00 
                            output: ["이전", "2025-02-13", "쿠폰"]

                            input: 내년 6월 이후에 있는 티켓이 뭐가 있지?
                            *현재시간 2025-02-06-14:00:00 
                            output: ["이후", "2026-06-01", "티켓"]

                            input: 오늘 오후 10시까지 써야하는 티켓 찾아줘.
                            *현재시간 2025-02-06-14:00:00 
                            output: ["이전", "2025-02-06 22:00:00", "티켓"]

                            input: 다음 주 오후 6시 이후 강남에서 약속 찾아줘.
                            *현재시간 2025-02-06-14:00:00 
                            output: ["이후", "2025-02-13 18:00:00", "강남", "약속"]

                            """
                        },
                        {
                            "type": "input_audio",
                            "input_audio": {
                                "data": encoded_string,
                                "format": "wav"
                            }
                        }
                    ]
                }
            ]
        )
        return json.loads(completion.choices[0].message.audio.transcript)