import speech_recognition as sr
import socket
import threading
import sys
import time
import pygame
import re

HOST = "10.10.14.69"
PORT = 5000
ADDR = (HOST,PORT)

recvId = "MIC_PYT"
recvFlag = False
rsplit = []
lock=threading.Lock()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 음성 인식기 인스턴스 생성
recognizer = sr.Recognizer()

words = ['켜', '꺼', '다른 단어1', '다른 단어2']

#모든 키 초기화
played_sounds = {word: False for word in words}

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
	#			print('recv :',rsplit) 

		s.close() 
	threading._start_new_thread(sendingMsg,()) 
	threading._start_new_thread(gettingMsg,()) 
except Exception as e:
	print('%s:%s'%ADDR)
	sys.exit()
print('connect is success')
ledFlag = False


def reset_played_sounds():
    for key in played_sounds.keys():
        played_sounds[key] = False

def play_sound(word):
    
    global played_sounds
    pygame.mixer.init()
    if not played_sounds[word]:  # 사운드가 아직 재생되지 않았다면
        if word == "켜":
            sound = pygame.mixer.Sound('data/출혈.wav')
        elif word == "꺼":
            sound = pygame.mixer.Sound('data/화상.wav')
        sound.play(1)
        played_sounds[word] = True  # 사운드 재생 플래그 업데이트

# 마이크로부터 오디오 데이터 캡처
def process_speech_input():
    while True:
        with sr.Microphone() as source:
            print("말을 하세요...")
            audio_data = recognizer.listen(source)
            print("인식 중...")

        try:
            text = recognizer.recognize_google(audio_data, language='ko-KR')
            print("인식된 내용: " + text)

            # "다음" 단어가 인식될 경우 played_sounds 리셋
            if '다음' in text:
                reset_played_sounds()
                print("모든 사운드 상태가 리셋되었습니다.")
                continue  # 다음 음성 입력을 기다림

            words = text.split()
            found = False  # Use a boolean flag for simplicity
            for word in words:
                if word == '켜':
                    play_sound(word)
                    data = "[LYJ_ARD]LED@ON"
                    data = bytes(data+'\n', "utf-8")
                    s.send(data) 
                    found = True
                elif word == '꺼':
                    play_sound(word)
                    data = "[LYJ_ARD]LED@ON"
                    data = bytes(data+'\n', "utf-8")
                    s.send(data) 
                    found = True
                elif word == '마':
                    data = "[LYJ_ARD]LED@OFF"
                    data = bytes(data+'\n', "utf-8")
                    s.send(data) 
                    found = True

            if found:
                print("'켜' 또는 '꺼' 문자열을 찾았습니다.")
                # Send data to the server

        except sr.UnknownValueError:
            print("음성을 인식할 수 없습니다.")
        except sr.RequestError as e:
            print(f"음성 인식 서비스 요청에 실패했습니다; {e}")

# Start a separate thread to continuously process speech input
threading._start_new_thread(process_speech_input,())

# Keep the main thread running indefinitely
while True:
    time.sleep(1)  # Keep the main thread alive