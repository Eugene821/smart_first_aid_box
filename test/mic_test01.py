import speech_recognition as sr

# 음성 인식기 인스턴스 생성
recognizer = sr.Recognizer()

# 마이크로부터 오디오 데이터 캡처
with sr.Microphone() as source:
    print("말을 하세요...")
    audio_data = recognizer.listen(source)
    print("인식 중...")

    try:
        # Google Web Speech API를 사용하여 오디오를 텍스트로 변환
        text = recognizer.recognize_google(audio_data, language='ko-KR')
        print("인식된 내용: " + text)
    except sr.UnknownValueError:
        # 음성 인식 실패
        print("음성을 인식할 수 없습니다.")
    except sr.RequestError as e:
        # API 요청 실패
        print(f"음성 인식 서비스 요청에 실패했습니다; {e}")