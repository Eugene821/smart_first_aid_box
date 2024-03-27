#client program 
#kcci iot/embedded 
import socket 
import threading 
import time
import re
HOST = "127.0.0.1" 
PORT = 5000 
ADDR = (HOST,PORT)
recvFlag = False
rsplit = []
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
try:
	s.connect((HOST, PORT)) 
	def sendingMsg(): 
		s.send('[LYJ_PYT:PASSWD]'.encode()) 
		time.sleep(0.5)
		while True: 
			data = input() 
#			data = bytes(data, "utf-8") 
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
			recvFlag = True;
			#print('recv :',rsplit) 

		s.close() 
	threading._start_new_thread(sendingMsg,()) 
	threading._start_new_thread(gettingMsg,()) 
except Exception as e:
	print('%s:%s'%ADDR)
	sys.exit()
print('connect is success')
while True: 
	if recvFlag:
		print('recv :',rsplit) 
		recvFlag = False
	pass

