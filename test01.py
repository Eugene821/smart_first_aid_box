import tkinter as tk
import cv2
from ultralytics import YOLO
from PIL import Image, ImageTk
import datetime

CONFIDENCE_THRESHOLD = 0.4

model = YOLO('/srv/samba/project/smart_aid_box/best_h2.pt')
class_names = ['bites', 'burns', 'cuts']


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

box_colors = {
    'bites': (0, 255, 0),    # Green
    'burns': (0, 0, 255),  # Red
    'cuts': (255, 0, 0), # Blue
}

# Function to perform object detection
def detect_objects(panel):
    #start = datetime.datetime.now()

    ret, frame = cap.read()
    if ret:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame_rgb)    
        detection = model(image)[0]

        for data in detection.boxes.data.tolist(): # data : [xmin, ymin, xmax, ymax, confidence_score, class_id]
            confidence = float(data[4])
            if confidence < CONFIDENCE_THRESHOLD:
                continue

            xmin, ymin, xmax, ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3])
            label = int(data[5])  # 클래스 ID
            class_name = class_names[label]  # 클래스 이름 조회
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), box_colors[class_name], 2)
            cv2.putText(frame, f'{class_name}: {confidence:.2f}', (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, box_colors[class_name], 2)

        #end = datetime.datetime.now()

        #total = (end - start).total_seconds()
        #print(f'Time to process 1 frame: {total * 1000:.0f} milliseconds')

        #fps = f'FPS: {1 / total:.2f}'
        #cv2.putText(frame, fps, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        
       # Show frame
        frame = cv2.resize(frame, (480, 480))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        panel.config(image=photo)
        panel.image = photo
        
    if not paused:
        panel.after(10, detect_objects, panel)
        
# Stop function
paused = True
def toggle_pause():
    global paused
    paused = not paused
    if paused:
        Pause_button_text.set("Resume")
    else:
        Pause_button_text.set("Pause")
        detect_objects(panel)
        
# Initialize GUI
window = tk.Tk()
window.title("Injury Detection Application")

# 비디오 피드를 표시할 패널
bin = tk.PhotoImage(file="/srv/samba/project/smart_aid_box/hurtlogo4.png")
bin_label = tk.Label(window, image=bin)
bin_label.grid(row=0, column=2, padx=10, pady=10,  rowspan=4)

panel = tk.Label(window)
panel.grid(row=0, column=2, padx=10, pady=10,  rowspan=4)  # column=1로 설정하여 오른쪽에 위치하도록 합니다.
        
# Add logo or icon
logo = tk.PhotoImage(file="/srv/samba/project/smart_aid_box/hurtlogo2.png")
logo_label = tk.Label(window, image=logo)
logo_label.grid(row=0, column=0, columnspan=2)  # columnspan=2로 설정하여 로고가 두 열을 차지하도록 합니다.

# 제목 라벨
title_label = tk.Label(window, text="Please recognize the injury on camera", font=("Helvetica", 20))
title_label.grid(row=1, column=0, columnspan=2, pady=3)  # columnspan=2로 설정

# 시작/일시정지 버튼
Pause_button_text = tk.StringVar()
Pause_button_text.set("Resume")
Pause_button = tk.Button(window, textvariable=Pause_button_text, command=toggle_pause, width=15, height=3, font=("Helvetica", 15))
Pause_button.grid(row=2, column=0, padx=5, pady=3)

# 종료 버튼
exit_button = tk.Button(window, text="Exit", command=window.quit, width=15, height=3, font=("Helvetica", 15))
exit_button.grid(row=2, column=1, padx=5, pady=3)

# 종료 버튼
exit_button = tk.Button(window, text="Exit1", command=window.quit, width=15, height=3, font=("Helvetica", 15))
exit_button.grid(row=3, column=0, padx=5, pady=3)

# 종료 버튼 2
exit_button = tk.Button(window, text="Exit2", command=window.quit, width=15, height=3, font=("Helvetica", 15))
exit_button.grid(row=3, column=1, padx=5, pady=3)

window.mainloop()

cap.release()
cv2.destroyAllWindows()