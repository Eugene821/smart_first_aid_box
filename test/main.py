import cv2

def main():
    # 카메라 인덱스 0으로 카메라 캡처 객체 생성
    cap = cv2.VideoCapture(0)

    # 캡처가 오픈되었는지 확인
    if not cap.isOpened():
        print("카메라를 열 수 없습니다.")
        exit()

    while True:
        # 현재 프레임 캡처
        ret, frame = cap.read()

        # 캡처가 성공적이지 않은 경우 루프 종료
        if not ret:
            print("프레임을 캡처할 수 없습니다. 종료합니다.")
            break

        # 프레임을 그레이스케일로 변환
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 변환된 프레임을 화면에 표시
        cv2.imshow('frame', gray)

        # 사용자가 'q'를 누르면 루프에서 빠져나옴
        if cv2.waitKey(1) == ord('q'):
            break

    # 작업 완료 후 캡처 객체와 모든 창 해제
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
