import cv2
import requests
import torch
import numpy as np
from PIL import Image
from io import BytesIO

from ultralytics import YOLO
from roboflow import Roboflow


# Roboflow API 설정
API_KEY = "rzoW7LjDV7RKGEjv6YaA"
MODEL_ID = "hurtproject"
VERSION_ID = "95"
API_URL = f"https://detect.roboflow.com/{MODEL_ID}/{VERSION_ID}?api_key={API_KEY}&format=image"

# 웹캠 설정
cap = cv2.VideoCapture(0)

while True:
    # 영상 프레임 캡쳐
    ret, frame = cap.read()
    if not ret:
        break

    # 프레임을 Roboflow API로 보내기 위해 인코딩
    _, img_encoded = cv2.imencode('.jpg', frame)
    files = {'file': ('image.jpg', img_encoded.tobytes(), 'image/jpeg', {'Expires': '0'})}

    # Roboflow API에 요청 보내기
    response = requests.post(API_URL, files=files)

    # 상태 코드 확인
    if response.status_code != 200:
        print(f"Error: {response.status_code}, Message: {response.text}")
        continue

    # API로부터 받은 이미지 데이터를 OpenCV에서 사용할 수 있도록 변환
    try:
        image = Image.open(BytesIO(response.content))
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # PIL 이미지를 OpenCV 포맷으로 변환
    except Exception as e:
        print(f"Error loading image: {e}")
        continue

    # 결과 시각화
    cv2.imshow('Object Detection', image)

    # q를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 자원 해제
cap.release()
cv2.destroyAllWindows()