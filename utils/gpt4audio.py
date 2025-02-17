import audioop
import pyaudio
import speech_recognition as sr
import base64
import os
import time
from openai import AzureOpenAI
from dotenv import load_dotenv
from pathlib import Path

def record_audio():
    # 녹음 설정 (파라미터는 그대로 유지)
    FORMAT = pyaudio.paInt16  # 16비트 포맷
    CHANNELS = 1  # 모노
    RATE = 44100     # 샘플링 레이트 (44.1kHz)
    CHUNK = 1024     # 버퍼 크기
    SILENCE_THRESHOLD = 300  # 무음 임계값
    INITIAL_SILENCE_DURATION = 7  # 초기 무음 시간 (초)
    SILENCE_DURATION = 1          # 음성 입력 후 무음 대기 시간 (초)

    # PyAudio 객체 생성 및 스트림 열기
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    print("녹음 시작... 말씀해주세요.")
    frames = []
    silence_count = 0
    is_recording = True
    voice_detected = False

    # 녹음 진행 (파일 I/O 없이 메모리 내 데이터로 처리)
    while is_recording:
        data = stream.read(CHUNK)
        frames.append(data)
        rms = audioop.rms(data, 2)
        if rms >= SILENCE_THRESHOLD:
            voice_detected = True
            silence_count = 0
        else:
            silence_count += 1

        if not voice_detected:
            if silence_count > INITIAL_SILENCE_DURATION * (RATE / CHUNK):
                print("음성이 감지되지 않아 녹음을 종료합니다.")
                is_recording = False
        else:
            if silence_count > SILENCE_DURATION * (RATE / CHUNK):
                is_recording = False

    print("녹음 완료.")
    stream.stop_stream()
    stream.close()
    sample_width = audio.get_sample_size(FORMAT)
    audio.terminate()

    audio_bytes = b''.join(frames)
    # sr.AudioData 객체로 생성하면 메모리 내 처리가 가능하여 파일 I/O 시간을 절감함
    return sr.AudioData(audio_bytes, RATE, sample_width)


def azure_audio_request(audio_data):
    env_path = Path(__file__).parent / '.env'
    load_dotenv(env_path)
    import time, base64
    start_request = time.time()

    # AudioData를 WAV 형식의 바이트 데이터로 변환
    wav_bytes = audio_data.get_wav_data()
    encoded_string = base64.b64encode(wav_bytes).decode('utf-8')

    # Azure OpenAI 설정
    endpoint = "https://team2-openai-eastus2.openai.azure.com/openai/deployments/gpt-4o-audio-preview/chat/completions?api-version=2025-01-01-preview"
    api_key = os.getenv('GPT_AUDIO_KEY')
    client = AzureOpenAI(
        api_version="2025-01-01-preview",
        api_key=api_key,
        azure_endpoint=endpoint
    )

    completion = client.chat.completions.create(
        model="gpt-4o-mini-audio-preview",
        modalities=["text", "audio"],
        audio={"voice": "alloy", "format": "wav"},
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

    elapsed_request = time.time() - start_request
    print(f"애저 요청 실행 시간: {elapsed_request:.2f}초")
    return completion