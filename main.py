import cv2
import torch

# 모델 로드 (예: YOLOv5)
model = torch.hub.load('ultralytics/yolov8', 'custom', path_or_model='/srv/samba/project/smart_aid_box/test/hurtproject.v95i.yolov8')  # `best.pt`는 Roboflow에서 Export한 모델 파일

# 이미지 로드
img = cv2.imread('path/to/your/image.jpg')

# 객체 인식 수행
results = model(img)

# 결과 시각화
results.show()  # YOLOv5의 경우, `.show()` 메서드를 사용하여 결과를 직접 시각화할 수 있습니다.

# 또는 OpenCV를 사용하여 바운딩 박스와 라벨을 이미지에 직접 그릴 수 있습니다.
for *xyxy, conf, cls in results.xyxy[0]:
    x1, y1, x2, y2 = map(int, xyxy)
    label = f'{results.names[int(cls)]} {conf:.2f}'
    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.putText(img, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

cv2.imshow('img', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
