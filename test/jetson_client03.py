import cv2
import torch
import socket
import threading
import time
import sys
import numpy as np




model = torch.load('model/best_h3.pt', map_location=torch.device('cpu'))  # GPU가 없는 경우 CPU 사용
#model = torch.load('model/best_h3.pt')  # 모델 파일 경로를 지정하세요.
model.eval()  # 모델을 평가 모드로 설정합니다.

class_names =  ['bites', 'burns', 'cuts']

HOST = "10.10.14.69"
PORT = 5000
ADDR = (HOST, PORT)
recvFlag = False
lock = threading.Lock()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
try:
    s.connect((HOST, PORT))
    print('Connection to server established')

    def send_command(data):
        """Send command to the server."""
        data = bytes(data+'\n', "utf-8")
        s.send(data)

    
    def video_processing():
        """Process video and detect changes, display video."""
        global ledFlag
        cap = cv2.VideoCapture(0)  # Start video capture
        _, frame1 = cap.read()
        _, frame2 = cap.read()

        while cap.isOpened():
            _, frame = cap.read()  # Read the current frame
            diff = cv2.absdiff(frame1, frame2)
            gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5, 5), 0)
            _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
            dilated = cv2.dilate(thresh, None, iterations=3)
            contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            # If contours are detected, there's a change in the frame (object movement)
            if len(contours) > 0:
                ledFlag = True
            else:
                ledFlag = False

            # Control LED based on detection
            if ledFlag:
                send_command("[LYJ_ARD]LED@ON")
            else:
                send_command("[LYJ_ARD]LED@OFF")

            # Display the resulting frame
            cv2.imshow('Frame', frame)

            # Update frame1 and frame2 for next iteration
            frame1 = frame2
            frame2 = frame

            # Break the loop when 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            time.sleep(0.5)  # Adjust for frame processing rate

        # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()

    threading.Thread(target=video_processing, args=()).start()

except Exception as e:
    print(f'Error connecting to {HOST}:{PORT}', e)
    sys.exit()

print('Client is running. Press CTRL+C to exit.')
