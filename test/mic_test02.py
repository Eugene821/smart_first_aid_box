import speech_recognition as sr
import socket 
import threading 
import time
import sys
import re

HOST = "10.10.14.69" 
PORT = 5000 
ADDR = (HOST,PORT)
recvFlag = False
rsplit = []
lock=threading.Lock()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

try:

	s.connect((HOST, PORT)) 
	def sendingMsg(): 
		s.send('[4:PASSWD]'.encode()) 
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

	threading._start_new_thread(sendingMsg,()) 
	threading._start_new_thread(gettingMsg,())
except Exception as e:
	print('%s:%s'%ADDR)
	sys.exit()
print('connect is success')

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
		
        words = text.split()
        found = 0  # 특정 문자열이 발견되면 1로 설정될 변수
        for word in words:
            if word == '켜':  # 찾고자 하는 특정 문자열
                data = "[LYJ_ARD]LED@ON"
                data = bytes(data+'\n', "utf-8") 
                found = 1
            elif word == '꺼':
                data = "[LYJ_ARD]LED@OFF"
                data = bytes(data+'\n', "utf-8") 
                found = 1

        if found == 1:
            print("'테스트' 문자열을 찾았습니다.")
        else:
            print("'테스트' 문자열을 찾지 못했습니다.")
			

    except sr.UnknownValueError:
        # 음성 인식 실패
        print("음성을 인식할 수 없습니다.")
    except sr.RequestError as e:
        # API 요청 실패
        print(f"음성 인식 서비스 요청에 실패했습니다; {e}")