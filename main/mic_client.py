import speech_recognition as sr
import socket
import threading
import sys
import time
import re
import pygame

pygame.init()

HOST = "10.10.14.69"
PORT = 5000
ADDR = (HOST,PORT)

recvId = "MIC_PYT"
recvFlag = False
rsplit = []
lock=threading.Lock()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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


try:
	s.connect((HOST, PORT)) 
	def sendingMsg(): 
		s.send('[MIC_PYT:PASSWD]'.encode()) 
		time.sleep(0.5)
		while True: 
			data = input() 
			data = bytes(data+'\n', "utf-8") 
			s.send(data) 
			s.close() 
	def gettingMsg(): 
		global rsplit
		global recvFlag
		while True: 
			data = s.recv(1024) 
			rstr = data.decode("utf-8")
			rsplit = re.split('[\]|\[@]|\n',rstr)  #'[',']','@' 분리
			recvFlag = True

		s.close() 
	threading._start_new_thread(sendingMsg,()) 
	threading._start_new_thread(gettingMsg,()) 
except Exception as e:
	print('%s:%s'%ADDR)
	sys.exit()
print('connect is success')
ledFlag = False




def find_sound_path(text):
    for sound_path, keywords in sound_to_words_mapping.items():
        if any(keyword in text for keyword in keywords):
            return sound_path
    return None

# 음성 입력 처리 함수
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

                    # 추가 명령에 대한 음성 입력 기다림
                    audio_data = recognizer.listen(source, timeout=10, phrase_time_limit=5)
                    text = recognizer.recognize_google(audio_data, language='ko-KR')
                    print(f"인식된 추가 명령: {text}")

                    # 추가 명령에 따라 사운드 재생 및 명령 전송
                    sound_path = find_sound_path(text)
                    if sound_path:
                        sound_manager.play_sound(sound_path)
                        print(f"재생: {sound_path}")

                        # 특정 키워드에 따른 명령 전송
                        if any(keyword in text for keyword in ['두통', '머리', '열', '어지러워', '어지럼증']):
                            s.send(b'[LYJ_ARD]LED@ON\n')  # LED 켜는 명령 전송
                            print("LED 켜는 명령을 전송했습니다.")
                        elif "꺼" in text:
                            s.send(b'[LYJ_ARD]LED@OFF\n')  # LED 끄는 명령 전송
                            print("LED 끄는 명령을 전송했습니다.")

                    else:
                        sound_manager.play_sound(retry_sound_path)
                        print("알아듣지 못했습니다. 다시 말해주세요.")

            except sr.UnknownValueError:
                print("불분명한 음성입니다. 다시 말해주세요.")
            except sr.WaitTimeoutError:
                print("시간 초과입니다. 다시 시도해주세요.")
            except sr.RequestError as e:
                print(f"음성 인식 서비스 요청 중 문제 발생: {e}")


threading.Thread(target=process_speech_input).start()

while True:
    time.sleep(1)
