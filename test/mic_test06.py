import speech_recognition as sr
import threading
import sys
import time
import pygame

pygame.init()

class SoundManager:
    def __init__(self):
        self.current_sound = None

    def play_sound(self, file_path):
        try:
            if self.current_sound is not None:
                self.current_sound.stop()
            self.current_sound = pygame.mixer.Sound(file_path)
            self.current_sound.play()
        except FileNotFoundError:
            print(f"File not found: {file_path}. Skipping sound playback.")

# 사운드 매니저 인스턴스 생성
sound_manager = SoundManager()

# 음성 인식기 및 마이크 초기화
recognizer = sr.Recognizer()

# 핫워드 감지 후 재생할 사운드 파일명
intro_sound_path = 'data/인트로.wav'
retry_sound_path = 'data/다시.wav'

# 사운드 파일을 여러 키워드에 매핑
sound_to_words_mapping = {
    'data/화상.wav': ['데었', '화상', '뜨거워', '뜨겁'],
    'data/출혈.wav': ['출혈', '피', '베었', '찔렸'],
    'data/벌레.wav': ['물렸', '가렵', '모기'],
    'data/두통.wav': ['두통', '머리', '열', '어지러워', '어지럼증'],
    'data/감기.wav': ['감기', '기침', '콧물', '몸살', '목', '재채기', '칼칼']
}

def find_sound_path(text):
    for sound_path, keywords in sound_to_words_mapping.items():
        if any(keyword in text for keyword in keywords):
            return sound_path
    return None

def process_speech_input():
    with sr.Microphone() as source:
        print("주변 소음 조정 중...")
        recognizer.adjust_for_ambient_noise(source, duration=1)  # 주변 소음 조정
        print("아파!를 말하면 음성 인식이 시작됩니다.")

        while True:
            try:
                print("듣고 있습니다...")
                audio_data = recognizer.listen(source, timeout=10, phrase_time_limit=5)
                text = recognizer.recognize_google(audio_data, language='ko-KR')
                print(f"인식된 명령: {text}")

                if "아파" in text:
                    sound_manager.play_sound(intro_sound_path)
                    print("추가 명령을 말하세요.")
                else:
                    sound_path = find_sound_path(text)
                    if sound_path:
                        sound_manager.play_sound(sound_path)
                        print(f"재생: {sound_path}")
                    else:
                        sound_manager.play_sound(retry_sound_path)
                        print("아파!라고 다시 말해주세요.")
            except sr.UnknownValueError:
                print("불분명한 음성입니다. 다시 말해주세요.")
            except sr.WaitTimeoutError:
                print("말하기를 시작하지 않아 시간이 초과되었습니다.")
            except sr.RequestError as e:
                print(f"음성 인식 서비스 요청 중 문제 발생: {e}")

threading.Thread(target=process_speech_input).start()

while True:
    time.sleep(1)
