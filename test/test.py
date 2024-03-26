import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer
import cv2

class WebcamApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Webcam Feed Integration")
        self.setGeometry(100, 100, 640, 480)
        
        # QLabel 생성 및 설정
        self.imageLabel = QLabel(self)
        self.imageLabel.resize(640, 480)
        
        # 카메라 설정
        self.cap = cv2.VideoCapture(0)
        
        # 타이머 설정
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateFrame)
        self.timer.start(20)  # 20ms마다 updateFrame 함수를 호출하여 비디오 프레임을 업데이트
        
    def updateFrame(self):
        ret, frame = self.cap.read()
        if ret:
            # OpenCV에서 가져온 이미지를 QLabel에 표시 가능한 형태로 변환
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytesPerLine = ch * w
            convertToQtFormat = QImage(frame.data, w, h, bytesPerLine, QImage.Format_RGB888)
            p = convertToQtFormat.scaled(self.imageLabel.size(), aspectRatioMode=Qt.KeepAspectRatio)
            self.imageLabel.setPixmap(QPixmap.fromImage(p))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = WebcamApp()
    mainWindow.show()
    sys.exit(app.exec_())
