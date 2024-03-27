import cv2
import tkinter as tk
import socket
import threading
import sys
import time
import re

from tkinter import messagebox
from ultralytics import YOLO
from PIL import Image, ImageTk


HOST = "10.10.14.69"
PORT = 5000
ADDR = (HOST,PORT)
CONFIDENCE_THRESHOLD = 0.4
recvId = "LYJ_PYT"
recvFlag = False
rsplit = []
lock=threading.Lock()
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

#모델 로드
model = YOLO('/srv/samba/project/smart_aid_box/model/best_h3.pt')
class_names = ['bites', 'burns', 'cuts']

# 웹캠 설정
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    messagebox.showerror("Camera Error", "Could not open the camera.")
    sys.exit()
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


box_colors = {
    'bites': (0, 255, 0),    # Green
    'burns': (0, 0, 255),  # Red
    'cuts': (255, 0, 0), # Blue
}

paused = True

#GUI 설정
window = tk.Tk()
window.title("Injury Detection Application")


def toggle_pause():
    global paused
    paused = not paused
    if paused:
        Pause_button_text.set("Resume")
    else:
        Pause_button_text.set("Pause")
        detect_objects(panel)



def show_info(class_detected):
    if class_detected:
        detected_classes = ', '.join(class_detected)
        info_label.config(text=f"Class Currently Recognized: {detected_classes}")
        for class_name in class_detected:
            # 여기에서는 각 클래스에 대해 LED를 켜는 명령을 전송합니다.
            send_command(f"[{recvId}]LED@ON")
            data = "[LYJ_ARD]LED@ON"
    else:
        info_label.config(text="No classes detected")


def detect_objects(panel):
    if not paused:
        ret, frame = cap.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame_rgb)
            detection = model(image)[0]

            class_detected = []
            for data in detection.boxes.data.tolist():
                confidence = float(data[4])
                if confidence >= CONFIDENCE_THRESHOLD:
                    label = int(data[5])
                    class_name = class_names[label]
                    class_detected.append(class_name)
                    # 여기에서 각 인식된 객체에 대해 사각형을 그리고 텍스트를 더합니다.

            # 인식된 클래스 정보를 바탕으로 정보를 표시하고 서버에 명령을 전송합니다.
            show_info(class_detected)  # show_info2로 변경

            frame = cv2.resize(frame, (480, 480))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            panel.config(image=photo)
            panel.image = photo

    panel.after(10, lambda: detect_objects(panel))

def send_command(command_str):
    """서버에 명령을 전송합니다. 문자열을 인코딩하여 바이트로 변환합니다."""
    command_bytes = command_str.encode()  # 문자열을 바이트로 인코딩
    s.send(command_bytes)



bin = tk.PhotoImage(file="/srv/samba/project/smart_aid_box/data/hurtlogo4.png")
bin_label = tk.Label(window, image=bin)
bin_label.grid(row=0, column=2, padx=10, pady=10,  rowspan=4)

panel = tk.Label(window)
panel.grid(row=0, column=2, padx=10, pady=10,  rowspan=4)

logo = tk.PhotoImage(file="/srv/samba/project/smart_aid_box/data/hurtlogo2.png")
logo_label = tk.Label(window, image=logo)
logo_label.grid(row=0, column=0, columnspan=2)

title_label = tk.Label(window, text="Please recognize the injury on camera", font=("Helvetica", 20))
title_label.grid(row=1, column=0, columnspan=2, pady=3)

Pause_button_text = tk.StringVar()
Pause_button_text.set("Resume")
Pause_button = tk.Button(window, textvariable=Pause_button_text, command=toggle_pause, width=15, height=3, font=("Helvetica", 15))
Pause_button.grid(row=2, column=0, padx=5, pady=3)

exit_button = tk.Button(window, text="Exit", command=window.quit, width=15, height=3, font=("Helvetica", 15))
exit_button.grid(row=2, column=1, padx=5, pady=3)

info_button = tk.Button(window, text="Info", command=show_info, width=15, height=3, font=("Helvetica", 15))
info_button.grid(row=3, column=0, padx=5, pady=3)

info_label = tk.Label(window, text="", font=("Helvetica", 12))
info_label.grid(row=3, column=1, padx=5, pady=3)

#exit_button2 = tk.Button(window, text="Exit2", command=window.quit, width=15, height=3, font=("Helvetica", 15))
#exit_button2.grid(row=3, column=1, padx=5, pady=3)

window.mainloop()

cap.release()
s.close()
cv2.destroyAllWindows()
