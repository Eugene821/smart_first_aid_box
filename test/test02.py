import tkinter as tk
import cv2
from ultralytics import YOLO
from PIL import Image, ImageTk

CONFIDENCE_THRESHOLD = 0.4

model = YOLO('best_h2.pt')
class_names = ['bites', 'burns', 'cuts']

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

box_colors = {
    'bites': (0, 255, 0),   # Green
    'burns': (0, 0, 255),   # Red
    'cuts': (255, 0, 0),    # Blue
}

paused = True

def toggle_pause():
    global paused
    paused = not paused
    if paused:
        Pause_button_text.set("Resume")
    else:
        Pause_button_text.set("Pause")
        detect_objects(panel)

def show_info():
    ret, frame = cap.read()
    if ret:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame_rgb)    
        detection = model(image)[0]
        
        class_detected = []
        for data in detection.boxes.data.tolist(): 
            confidence = float(data[4])
            if confidence < CONFIDENCE_THRESHOLD:
                continue

            label = int(data[5])  
            class_name = class_names[label]  
            class_detected.append(class_name)
        
        if class_detected:
            info_label.config(text="Class Currently Recognized: " + ', '.join(class_detected))
        else:
            info_label.config(text="No classes detected")

def detect_objects(panel):
    ret, frame = cap.read()
    if ret:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame_rgb)    
        detection = model(image)[0]

        for data in detection.boxes.data.tolist(): 
            confidence = float(data[4])
            if confidence < CONFIDENCE_THRESHOLD:
                continue

            xmin, ymin, xmax, ymax = map(int, data[:4])
            label = int(data[5])  
            class_name = class_names[label]  
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), box_colors[class_name], 2)
            cv2.putText(frame, f'{class_name}: {confidence:.2f}', (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, box_colors[class_name], 2)

            print(f'Detected: {class_name} with confidence {confidence:.2f}')


        frame = cv2.resize(frame, (480, 480))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
        panel.config(image=photo)
        panel.image = photo
        
    if not paused:
        panel.after(10, detect_objects, panel)

window = tk.Tk()
window.title("Injury Detection Application")

bin = tk.PhotoImage(file="hurtlogo4.png")
bin_label = tk.Label(window, image=bin)
bin_label.grid(row=0, column=2, padx=10, pady=10,  rowspan=4)

panel = tk.Label(window)
panel.grid(row=0, column=2, padx=10, pady=10,  rowspan=4)

logo = tk.PhotoImage(file="hurtlogo2.png")
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


window.mainloop()

cap.release()
cv2.destroyAllWindows()
