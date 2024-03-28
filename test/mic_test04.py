import speech_recognition as sr
import socket
import threading
import sys
import time
import pygame
import re

# Pygame 초기화 및 사운드 관리 클래스 정의
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

sound_manager = SoundManager()

HOST = "10.10.14.69"
PORT = 5000
ADDR = (HOST, PORT)
recvFlag = False
rsplit = []
lock=threading.Lock()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

recognizer = sr.Recognizer()

# 단어와 사운드 파일 매핑
word_to_sound_mapping = {
    '데었어': 'data/화상.wav',
    '데었네': 'data/화상.wav',
    '데었다': 'data/화상.wav',
    '화상': 'data/화상.wav',
    '뜨거워': 'data/화상.wav',
    '뜨겁네': 'data/화상.wav',
    '뜨겁다': 'data/화상.wav',
    '피나': 'data/출혈.wav',
    '베었어': 'data/출혈.wav',
    '베었네': 'data/출혈.wav',
    '베었다': 'data/출혈.wav',
    '찔렸어': 'data/출혈.wav',
    '물렸어': 'data/벌레.wav',
    '가려워': 'data/벌레.wav',
    '모기': 'data/벌레.wav'
    # 다른 단어와 사운드 파일 매핑을 여기에 추가
    # 단어: 사운드 파일 경로
}

# 서버 연결
try:
	s.connect((HOST, PORT)) 
	def sendingMsg(): 
		s.send('[14:PASSWD]'.encode()) 
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
     
print('Connection successful.')
ledFlag = False



def send_led_command(command):
    global s
    try:
        s.send(command)
    except (BrokenPipeError, OSError):
        print("Connection lost... Reconnecting")
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(ADDR)
            s.send(command)  # 재연결 후 명령 재전송
        except Exception as e:
            print(f"Reconnection failed: {e}")


def process_speech_input():
    while True:
        with sr.Microphone() as source:
            print("Please speak...")
            audio_data = recognizer.listen(source)
            print("Recognizing...")
            try:
                text = recognizer.recognize_google(audio_data, language='ko-KR')
                print(f"Recognized: {text}")
                
                # 여기에서 인식된 텍스트를 처리합니다.
                for word, sound_path in word_to_sound_mapping.items():
                    if word in text:
                        sound_manager.play_sound(sound_path)
                        print(f"Playing sound for word: {word}")
                        if word in ['켜']:
                            send_led_command(b"[LYJ_ARD]LED@ON\n")
                            data = bytes(data+'\n', "utf-8") 
                        elif word in ['꺼']:
                            send_led_command(b"[LYJ_ARD]LED@OFF\n")
                            data = bytes(data+'\n', "utf-8") 
                        break  # 첫 번째 일치하는 단어에 대해 처리 후 루프 탈출

            except sr.UnknownValueError:
                print("Could not understand audio.")
            except sr.RequestError as e:
                print(f"Could not request results; {e}")


# 음성 처리 스레드 시작
threading.Thread(target=process_speech_input).start()

while True:
    time.sleep(1)
